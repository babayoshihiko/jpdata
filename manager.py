# -*- coding: utf-8 -*-
import os, posixpath, tempfile
from qgis.PyQt.QtCore import Qt, QSettings, QUrl
from qgis.PyQt.QtGui import QDesktopServices
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView, QLineEdit
from qgis.core import (
    QgsProject,
    QgsSettings,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsPointXY,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
)

from .ui_handler import JPDataUIHandler
from . import jpDataDownloader
from . import jpDataUtils
from . import jpDataLNI
from . import jpDataCensus
from . import jpDataMuni
from . import jpDataMesh
from . import jpDataAddr

class JPDataManager:
    def __init__(self, iface):
        self._iface = iface
        self._plugin_dir = os.path.dirname(__file__)
        self._dw = None
        self._ui = None
        
        self._folderPath = QSettings().value("jpdata/FolderPath", "~")
        self._proxyServer = QSettings().value("jpdata/ProxyServer", "http://")
        self._land_info = jpDataUtils.getMapsFromCsv2()
        self._GSI = jpDataUtils.getTilesFromCsv()
        
        self._downloader = jpDataDownloader.DownloadThread()
        
        self._name_map_prev = ""

        self._dl_status = ""
        self._dl_url_zip = []
        self._dl_iter = 0

        self._verbose = True

    def run(self):
        if not self._dw:
            from .jpdata_dockwidget import jpdataDockWidget
            self._dw = jpdataDockWidget()
            self._ui = JPDataUIHandler(self._dw)
            self.connect_signals()
            self.setup_initial_ui_state()

        if self._ui:
            self._ui.init_tabs(self._land_info, self._folderPath)
            jpDataCensus.set_year_items(self._dw.myComboBox31, 2000)

        # QGIS 4 compatible
        dock_area = Qt.DockWidgetArea.LeftDockWidgetArea if hasattr(Qt, 'DockWidgetArea') else Qt.LeftDockWidgetArea
        self._iface.addDockWidget(dock_area, self._dw)
        self._dw.show()

    def setup_initial_ui_state(self):
        if self._folderPath != "~":
            self._dw.myLabel1.setText(self._folderPath)
            self._dw.myTabWidget.setCurrentIndex(0)
        else:
            self._dw.myLabel1.setText("Choose folder for zip/shp files")
            self._dw.myTabWidget.setCurrentIndex(4)

        if self._proxyServer:
            self._dw.myLineEditSetting1.setText(self._proxyServer)
        
        self._dw.myLineEditSetting3.setEchoMode(QLineEdit.EchoMode.Password if hasattr(QLineEdit, 'EchoMode') else QLineEdit.Password)
        
        for row in self._GSI:
            self._dw.myListWidget23.addItem(row["name_j"])

    def connect_signals(self):
        dw = self._dw
        # Tab 1
        dw.myPushButton2.clicked.connect(self.chooseFolder)
        dw.myPushButton11.clicked.connect(self.tab1DownloadAll)
        dw.myPushButton14.clicked.connect(self.tab1AddMap)
        dw.myPushButton15.clicked.connect(self.tab1Web)
        dw.myListWidget11.itemSelectionChanged.connect(self.LW11_itemSelectionChanged)
        dw.myListWidget12.itemSelectionChanged.connect(self.LW12_itemSelectionChanged)
        dw.myComboBox11.currentIndexChanged.connect(self._cb11_changed)
        
        # Tab 2
        dw.myPushButton25.clicked.connect(self.addTile)

        # Tab 3
        dw.myPushButton32.clicked.connect(self.tab3AddMap)
        dw.myPushButton31.clicked.connect(self.tab3DownloadAll2)
        dw.myListWidget31.currentItemChanged.connect(
            self._LW31_currentItemChanged
        )  ## NEEDS REFACTORING to itemSelectionChanged
        dw.myListWidget32.itemSelectionChanged.connect(
            self._LW32_itemSelectionChanged
        )
        
        # Tab 4 / Settings
        dw.myTabWidget.currentChanged.connect(self._tab_changed)
        dw.myCB_Addr_1.currentIndexChanged.connect(
            self._myCB_Addr_1_changed
        )
        dw.myCB_Addr_2.currentIndexChanged.connect(
            lambda: jpDataAddr.set_cb_towns(
                dw.myCB_Addr_3,
                self._folderPath,
                dw.myCB_Addr_1.currentText(),
                dw.myCB_Addr_2.currentText(),
            )
        )
        dw.myCB_Addr_3.currentIndexChanged.connect(
            lambda: jpDataAddr.set_cb_details(
                dw.myCB_Addr_4,
                self._folderPath,
                dw.myCB_Addr_1.currentText(),
                dw.myCB_Addr_2.currentText(),
                dw.myCB_Addr_3.currentText(),
            )
        )
        dw.myPB_Addr_1.clicked.connect(self.myPB_Addr_1_clicked)


        # For local testing purpose
        if self._verbose:
            dw.myPushButtonTest.clicked.connect(self._test_verbose)
        else:
            dw.myPushButtonTest.hide()

        # Downloader
        self._downloader.setProxyServer(self._proxyServer)
        self._downloader.progress.connect(self._dw.progressBar.setValue)
        self._downloader.finished.connect(self.download_finished)

    def setLabel(self, message):
        self._dw.myLabelStatus.setText(message)
        if self._verbose:
            jpDataUtils.printLog(message)

    def unload(self):
        if self._dw:
            self._iface.removeDockWidget(self._dw)
            self._dw.deleteLater()
            self._dw = None
            self._ui = None

    def _test_verbose(self):
        pass
        # This is a method for local testing purpose.

    def _add_map(self, shpFileFullPath, layerName, qmlFileName, encoding="CP932"):
        tempLayer = QgsVectorLayer(shpFileFullPath, layerName, "ogr")
        tempLayer.setProviderEncoding(encoding)
        if self._dw.myCheckBox2.isChecked() == False:
            count_invalid_geom = jpDataUtils.count_invalid_geometry(tempLayer)
            if count_invalid_geom > 0:
                tempLayer.setName(layerName + " [invalid]")
                self.setLabel(
                    self._ui.tr("The layer has invalid geometries: ") + str(count_invalid_geom)
                )

        if os.path.isfile(posixpath.join(self._plugin_dir, "qml", qmlFileName)):
            # For the qml files that use SVG images in the plugin folder
            with tempfile.TemporaryDirectory() as temp_dir:
                with open(
                    posixpath.join(self._plugin_dir, "qml", qmlFileName),
                    "r",
                ) as file:
                    file_contents = file.read()
                new_contents = file_contents.replace("PLUGIN_DIR", self._plugin_dir)
                with open(posixpath.join(temp_dir, qmlFileName), "w") as file:
                    file.write(new_contents)
                if tempLayer.loadNamedStyle(posixpath.join(temp_dir, qmlFileName)):
                    tempLayer.triggerRepaint()
        QgsProject.instance().addMapLayer(tempLayer)
        return tempLayer
















    def LW11_itemSelectionChanged(self):
        if len(self._dw.myListWidget11.selectedItems()) == 0:
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()

        prevLandNum = self._land_info.get(self._name_map_prev, {})
        thisLandNum = self._land_info[name_map]
        
        self._dw.myLabelStatus.setText(thisLandNum.get("code_map", ""))

        str_current_LW12_selected = [item.text() for item in self._dw.myListWidget12.selectedItems()]
        str_new_LW12_text = []
        bol_redraw_LW12 = True
        bol_show_LW13 = False
        muni_type = thisLandNum.get("type_muni", "").lower()

        def all_prefs():
            return [jpDataUtils.getPrefNameByCode(code) for code in range(1, 48)]

        if muni_type in ("", "allprefs"):
            if not self._name_map_prev or prevLandNum.get("type_muni", "").lower() not in ("", "allprefs", "mesh1"):
                str_new_LW12_text = all_prefs()
            else:
                bol_redraw_LW12 = False
                self._dw.myListWidget13.hide()
        elif muni_type == "single":
            str_new_LW12_text = ["Nation-wide"]
        elif muni_type in ("regional", "detail"):
            if muni_type == "detail": bol_show_LW13 = True
            str_new_LW12_text = jpDataLNI.getPrefsOrRegionsByMapCode(thisLandNum["code_map"], thisLandNum["year"])
        elif muni_type == "mesh1":
            bol_show_LW13 = True
            str_new_LW12_text = all_prefs()

        if bol_redraw_LW12:
            self._tab1_clear(bol_show_LW13)
            for new_text in str_new_LW12_text:
                item = QListWidgetItem(new_text)
                self._dw.myListWidget12.addItem(item)
                if new_text in str_current_LW12_selected:
                    item.setSelected(True)

        self._tab1_check_year(name_map)
        self._name_map_prev = name_map

    def _tab1_clear(self, bol_show_LW13):
        self._dw.myListWidget12.clear()
        mode = QAbstractItemView.SelectionMode.SingleSelection if bol_show_LW13 else QAbstractItemView.SelectionMode.ExtendedSelection
        # QGIS 3/4 compatible
        if not hasattr(QAbstractItemView, 'SelectionMode'):
            mode = QAbstractItemView.SingleSelection if bol_show_LW13 else QAbstractItemView.ExtendedSelection
        
        self._dw.myListWidget12.setSelectionMode(mode)
        if bol_show_LW13:
            self._dw.myListWidget13.show()
        else:
            self._dw.myListWidget13.hide()

    def LW12_itemSelectionChanged(self):
        if len(self._dw.myListWidget11.selectedItems()) == 0 or len(self._dw.myListWidget12.selectedItems()) == 0:
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()
        name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        self._tab1_check_year(name_map)
        thisLandNum = self._land_info[name_map]
        if thisLandNum["type_muni"].lower() in ("detail", "mesh1"):
            self._tab1_set_LW13(name_pref)

    def _tab1_check_year(self, name_map=None):
        thisLandNum = self._land_info[name_map]
        name_pref = None
        self._dw.myComboBox11.clear()
        if thisLandNum["year"].upper()[-3:] != "CSV":
            self._dw.myComboBox11.addItem(thisLandNum["year"])
        else:
            if len(self._dw.myListWidget12.selectedItems()) > 0:
                if thisLandNum["type_muni"].lower() != "mesh1":
                    name_pref = self._dw.myListWidget12.selectedItems()[0].text()
            years = jpDataLNI.getYearsByMapCode(thisLandNum["code_map"], name_pref, thisLandNum["year"])
            for year in years:
                if year: self._dw.myComboBox11.addItem(year)
        self._tab1_set_LW13()

    def _cb11_changed(self, index):
        self._tab1_set_LW13()

    def _tab1_set_LW13(self, name_pref=None):
        if len(self._dw.myListWidget11.selectedItems()) == 0: return
        if name_pref is None:
            if len(self._dw.myListWidget12.selectedItems()) == 0: return
            name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        
        str_name_j = self._dw.myListWidget11.selectedItems()[0].text()
        str_year = self._dw.myComboBox11.currentText()
        if not str_year.strip(): return

        thisLandNum = self._land_info[str_name_j]
        if thisLandNum["type_muni"].lower() not in ("detail", "mesh1"): return

        self._dw.myListWidget13.clear()
        self._dw.myListWidget13.show()
        
        if thisLandNum["type_muni"].lower() == "detail":
            details = jpDataLNI.getDetailsByMapCodePrefNameYear(thisLandNum["code_map"], name_pref, str_year)
        else:
            details = jpDataMesh.getMesh1ByPrefName(name_pref)

        for detail in details:
            self._dw.myListWidget13.addItem(QListWidgetItem(detail))

    def tab1Web(self):
        items = self._dw.myListWidget11.selectedItems()
        if items:
            thisLandNum = self._land_info[items[0].text()]
            QDesktopServices.openUrl(QUrl(thisLandNum["source"]))

    def chooseFolder(self):
        from qgis.PyQt.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(
            self._iface.mainWindow(), self._ui.tr("Select Directory"), self._folderPath
        )
        if folder:
            self._folderPath = folder
            QSettings().setValue("jpdata/FolderPath", folder)
            self._dw.myLabel1.setText(folder)

    def tab1AddMap(self):
        if not self.tab1CheckSelected():
            return
            
        thisLandNum = self._land_info[self._dw.myListWidget11.selectedItems()[0].text()]
        year = self._dw.myComboBox11.currentText()
        pref_names = self._dw.myListWidget12.selectedItems()
        pref_code = []

        if thisLandNum["type_muni"].lower() == "mesh1":
            for code_mesh1 in self._dw.myListWidget13.selectedItems():
                pref_code.append(code_mesh1.text())
        else:
            for pref_name in pref_names:
                pref_code.append(jpDataUtils.getPrefCodeByName(pref_name.text()))

        detail = None
        if thisLandNum["type_muni"].lower() == "detail" and self._dw.myListWidget13.selectedItems():
            detail = self._dw.myListWidget13.selectedItems()[0].text()
            
        if thisLandNum["type_muni"] == "single":
            pref_code = [""]

        for x in range(len(pref_code)):
            (zip_filename, shp_filename, altdir, qml_file, epsg, encoding, subfolder, layer_name) = \
                jpDataLNI.getZip(year, thisLandNum, pref_names[x].text() if x < len(pref_names) else "", 
                                 pref_code[x], "full", detail=detail)

            shp_full_path = jpDataUtils.unzipAndGetShp(
                os.path.join(self._folderPath, subfolder),
                zip_filename, shp_filename, altdir, pref_code[x],
                epsg=epsg, encoding=encoding
            )

            if shp_full_path:
                from qgis.core import QgsVectorLayer, QgsProject
                layer = QgsVectorLayer(shp_full_path, layer_name, "ogr")
                if layer.isValid():
                    QgsProject.instance().addMapLayer(layer)
            else:
                self._dw.myLabelStatus.setText(self._ui.tr("Cannot find .shp file"))

    def addTile(self):
        from qgis.core import QgsRasterLayer, QgsProject
        selected_items = self._dw.myListWidget23.selectedItems()
        if not selected_items:
            return

        tile_name = selected_items[0].text()
        tile_url_base = ""
        zoom_min = ""
        zoom_max = ""

        for current_gsi in self._GSI:
            if current_gsi["name_j"] == tile_name:
                tile_url_base = current_gsi["url"]
                zoom_min = current_gsi["zoom_min"]
                zoom_max = current_gsi["zoom_max"]
                break

        tile_url = (
            "type=xyz&url=" + tile_url_base +
            "&zmax=" + zoom_max +
            "&zmin=" + zoom_min +
            "&crs=EPSG3857"
        )
        layer = QgsRasterLayer(tile_url, tile_name, "wms")
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)

    def tab1CheckSelected(self):
        if not self._dw.myListWidget11.selectedItems():
            self._dw.myLabelStatus.setText(self._ui.tr("Please choose a map."))
            return False
        if not self._dw.myListWidget12.selectedItems():
            self._dw.myLabelStatus.setText(self._ui.tr("Please choose a prefecture or region."))
            return False
        return True

    def _tab_changed(self, index):
        """Called whenever the current tab changes."""
        if index == 3:  # tab #3 (4th tab)
            self._dw.myCB_Addr_1.setCurrentIndex(12)

    def tab1DownloadAll(self):
        if not self.tab1CheckSelected():
            return
        if self._dw.myPushButton11.text() == self._ui.tr("Cancel"):
            self.cancel_download()
            return

        self._dl_url_zip = []
        self._dl_iter = 0
        year = str(self._dw.myComboBox11.currentText())
        pref_names = self._dw.myListWidget12.selectedItems()

        thisLandNum = self._land_info[
            str(self._dw.myListWidget11.selectedItems()[0].text())
        ]

        for pref_name in pref_names:
            if thisLandNum["type_muni"].lower() == "mesh1":
                str_replace_after = str(
                    self._dw.myListWidget13.selectedItems()[0].text()
                )
            else:
                str_replace_after = jpDataUtils.getPrefCodeByName(str(pref_name.text()))

            tempUrl, tempZip, tempSubFolder = jpDataLNI.getZip(
                year, thisLandNum, str(pref_name.text()), str_replace_after, "urlzip"
            )
            if tempZip is not None:
                self._dl_url_zip.append(
                    {
                        "year": year,
                        "url": tempUrl,
                        "zip": tempZip,
                        "subfolder": tempSubFolder,
                    }
                )
        self._download_iter_2()

    # year = 2023 and so on
    # type must be one of ["regional","detail","single","","census"]
    # selection_code is a dictionary of codes
    #     (prefectural codes, municipal codes and so on)
    # a list of "code_pref"s (type = "" or "region")
    # or a list of "code_muni"s (type = "census")
    def _download_iter_2(self):
        _start_download = False

        for x in range(self._dl_iter, len(self._dl_url_zip)):
            self.setLabel("Fetching " + str(x) + " in " + str(len(self._dl_url_zip)))
            tempUrl = self._dl_url_zip[x]["url"]
            tempZipFileName = self._dl_url_zip[x]["zip"]
            tempSubFolder = self._dl_url_zip[x]["subfolder"]
            self.setLabel(self._folderPath)
            self.setLabel(tempZipFileName)
            if not os.path.exists(
                posixpath.join(
                    self._folderPath,
                    tempSubFolder,
                    tempZipFileName,
                )
            ):
                _start_download = True
                break
            else:
                self.setLabel(self._ui.tr("The zip file exists: ") + tempZipFileName)
        if _start_download:
            self._dw.progressBar.setValue(0)
            self.enable_download(False)
            self._dl_iter = x + 1
            self.start_download(tempUrl, tempSubFolder, tempZipFileName)
        else:
            self.enable_download()
            self._dl_iter = 0

    def enable_download(self, enable=True):
        if enable:
            self._dw.myPushButton11.setText(self._ui.tr("Download"))
            self._dw.myPushButton31.setText(self._ui.tr("Download"))
            self._dw.myPushButton14.setEnabled(True)
            self._dw.myPushButton32.setEnabled(True)
        else:
            self._dw.myPushButton11.setText(self._ui.tr("Cancel"))
            self._dw.myPushButton31.setText(self._ui.tr("Cancel"))
            self._dw.myPushButton14.setEnabled(False)
            self._dw.myPushButton32.setEnabled(False)


    def start_download(self, url, subFolder, zipFileName):
        if not os.path.exists(posixpath.join(self._folderPath, subFolder)):
            os.mkdir(posixpath.join(self._folderPath, subFolder))

        if not os.path.exists(posixpath.join(self._folderPath, subFolder, zipFileName)):
            self.set_proxy()
            self.setLabel(self._ui.tr("Downloading: ") + zipFileName)
            self._downloader.setUrl(url)
            self._downloader.setFilePath(
                posixpath.join(self._folderPath, subFolder, zipFileName)
            )
            self.enable_download(False)
            if self._dw.myCheckBox1.isChecked():
                self._downloader.download_wo_thread()
                self.enable_download()
            else:
                self._downloader.start()
        else:
            self.setLabel(self._ui.tr("The zip file exists: ") + zipFileName)
            self.enable_download()

    def download_finished(self, success):
        current_text = self._dw.myLabelStatus.text()
        self.setLabel(current_text + self._ui.tr("...Done"))
        self.enable_download()
        self._dw.progressBar.setValue(100)

        if len(self._dl_url_zip) > 0 and self._dl_iter < len(self._dl_url_zip):
            # Download next
            self._download_iter_2()
        else:
            # All downloads finished
            self._dl_iter = 0
            self._dl_url_zip = []
            if self._dl_status == "ADDRESS":
                self._dw.myPB_Addr_1.setText(self._ui.tr("Jump"))
                self._myCB_Addr_1_changed()

    def cancel_download(self):
        self._dl_url_zip = []
        if self._downloader is not None:
            current_text = self._dw.myLabelStatus.text()
            self.setLabel(current_text + self._ui.tr("...Cancelled"))
            self._downloader.stop()
        else:
            self._downloader = jpDataDownloader.DownloadThread()
        self.enable_download()

    def set_proxy(self):
        _proxyServer = self._dw.myLineEditSetting1.text()
        if len(_proxyServer) > 10:
            if self._proxyServer != _proxyServer:
                self._proxyServer = _proxyServer
                QgsSettings().setValue("jpdata/ProxyServer", self._proxyServer)
                self._downloader.setProxyServer(self._proxyServer)
            self._downloader.setProxyUser(self._dw.myLineEditSetting2.text())
            self._downloader.setProxyPassword(self._dw.myLineEditSetting3.text())
        else:
            self._downloader.setProxyServer("")
            QgsSettings().setValue("jpdata/ProxyServer", "http://")
            self._proxyServer = "http://"








    def _LW31_currentItemChanged(self, current, previous):
        if not current or current == previous or isinstance(current, int):
            return
            
        name_pref = current.text()
        year = self._dw.myComboBox31.currentText()
        
        designated_cities = jpDataMuni.get_all_designated_cities(year)
        
        rows = jpDataMuni.getMuniFromPrefName(name_pref)
        self._dw.myListWidget32.clear()
        
        for row in rows:
            name = row["name_muni"]
            if not name:
                continue
                
            item = QListWidgetItem(name)
            
            if name in designated_cities:
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                item.setForeground(Qt.gray)
                
            self._dw.myListWidget32.addItem(item)
            
        self._tab3_set_mesh()


    def _LW32_itemSelectionChanged(self):
        self._tab3_set_mesh()

    def _tab3_set_mesh(self):
        if len(self._dw.myListWidget31.selectedItems()) == 0:
            return
        name_pref = str(self._dw.myListWidget31.selectedItems()[0].text())

        if self._dw.myComboBox32.currentIndex() == 0:
            self._dw.myListWidget33.clear()
            self._dw.myListWidget33.hide()
            jpDataCensus.set_year_items(self._dw.myComboBox31, 2000)
            return
        elif (
            self._dw.myComboBox32.currentIndex() == 1
            or self._dw.myComboBox32.currentIndex() == 2
        ):
            jpDataCensus.set_year_items(self._dw.myComboBox31, 1995)
        else:
            jpDataCensus.set_year_items(self._dw.myComboBox31, 2005)

        self._dw.myListWidget33.clear()
        self._dw.myListWidget33.show()

        if len(self._dw.myListWidget32.selectedItems()) == 0:
            details = jpDataMesh.getMesh1ByPrefName(name_pref)
        else:
            name_munis = []
            for name_muni in self._dw.myListWidget32.selectedItems():
                name_munis.append(name_muni.text())
            jpDataUtils.printLog(name_munis)
            details = jpDataMesh.getMesh1ByPrefMuniName(name_pref, name_munis)

        for detail in details:
            self._dw.myListWidget33.addItem(detail)

    def tab3CheckSelected(self):
        if len(self._dw.myListWidget31.selectedItems()) == 0:
            self.setLabel(self._ui.tr("Please choose a prefecture."))
            return False
        if self._dw.myComboBox32.currentIndex() == 0:
            if len(self._dw.myListWidget32.selectedItems()) == 0:
                self.setLabel(self._ui.tr("Please choose a municipality."))
                return False
        else:
            if len(self._dw.myListWidget33.selectedItems()) == 0:
                self.setLabel(self._ui.tr("Please choose a mesh code."))
                return False
        return True

    def tab3DownloadAll2(self):
        if self._dw.myPushButton31.text() == self._ui.tr("Cancel"):
            self.cancel_download()
            return
        if not self.tab3CheckSelected():
            return

        self._dl_url_zip = []
        self._dl_iter = 0
        year = str(self._dw.myComboBox31.currentText())
        name_pref = self._dw.myListWidget31.selectedItems()[0].text()
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        # Check if municipality (shochiiki) is selected
        if self._dw.myComboBox32.currentIndex() == 0:
            # Get municipality names
            muni_names = self._dw.myListWidget32.selectedItems()
        else:
            # Get mesh codes
            muni_names = self._dw.myListWidget33.selectedItems()
        for muni_name in muni_names:
            # Usually, attributes are in one file, so for loop is not
            # really necessary
            row = jpDataMuni.getRowFromNames(name_pref, str(muni_name.text()))
            if self._dw.myComboBox32.currentIndex() == 0:
                code_muni = row["code_muni"]
            else:
                code_muni = str(muni_name.text())

            # Append the attribute data first
            tempUrl, tempZip, tempSubFolder = jpDataCensus.getAttr(
                year,
                code_pref,
                code_muni,
                self._dw.myComboBox32.currentIndex(),
            )
            if tempZip is not None:
                self._dl_url_zip.append(
                    {
                        "year": year,
                        "url": tempUrl,
                        "zip": tempZip,
                        "subfolder": tempSubFolder,
                    }
                )
            # Append the shp data
            tempUrl, tempZip, tempSubFolder = jpDataCensus.getZip(
                year,
                code_pref,
                code_muni,
                self._dw.myComboBox32.currentIndex(),
            )
            if tempZip is not None:
                self._dl_url_zip.append(
                    {
                        "year": year,
                        "url": tempUrl,
                        "zip": tempZip,
                        "subfolder": tempSubFolder,
                    }
                )

        self._download_iter_2()

    def tab3AddMap(self):
        if not self.tab3CheckSelected():
            return
        year = str(self._dw.myComboBox31.currentText())
        name_pref = self._dw.myListWidget31.selectedItems()[0].text()
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        tempSubFolder = jpDataCensus.getSubFolder(
            self._dw.myComboBox32.currentIndex()
        )

        if self._dw.myComboBox32.currentIndex() == 0:
            muni_names = self._dw.myListWidget32.selectedItems()
            tempQmlFile = "Census-" + year + ".qml"
            name_muni_suffix = ""
        else:
            muni_names = self._dw.myListWidget33.selectedItems()
            if self._dw.myComboBox32.currentIndex() == 1:
                tempQmlFile = "Census-SDDSWS-" + year + ".qml"
                name_muni_suffix = " " + self._ui.tr("3rd")
            elif self._dw.myComboBox32.currentIndex() == 2:
                tempQmlFile = "Census-HDDSWH-" + year + ".qml"
                name_muni_suffix = " " + self._ui.tr("4th")
            elif self._dw.myComboBox32.currentIndex() == 3:
                tempQmlFile = "Census-QDDSWQ-" + year + ".qml"
                name_muni_suffix = " " + self._ui.tr("5th")

        for muni_name in muni_names:
            name_muni = str(muni_name.text())
            if self._dw.myComboBox32.currentIndex() == 0:
                row = jpDataMuni.getRowFromNames(name_pref, name_muni)
                code_muni = row["code_muni"]
            else:
                code_muni = name_muni
            tempZipFileName, tempShpFileName = jpDataCensus.getZipShp(
                year,
                code_pref,
                code_muni,
                self._dw.myComboBox32.currentIndex(),
            )

            tempShpFullPath = jpDataUtils.unzipAndGetShp(
                posixpath.join(self._folderPath, tempSubFolder),
                tempZipFileName,
                tempShpFileName,
            )

            if tempShpFullPath is None:
                self.setLabel(self._ui.tr("Cannot find the .shp file: ") + tempShpFileName)
                self._iface.messageBar().pushMessage(
                    "Error",
                    "Cannot find the .shp file: " + tempShpFileName,
                    1,
                    duration=10,
                )
                break

            if tempShpFullPath != "":
                tempCsvFileName = jpDataCensus.getAttrCsvFileName(
                    year,
                    code_pref,
                    code_muni,
                    self._dw.myComboBox32.currentIndex(),
                )
                tempUrl, tempZip, tempSubFolder = jpDataCensus.getAttr(
                    year,
                    code_pref,
                    code_muni,
                    self._dw.myComboBox32.currentIndex(),
                )
                jpDataUtils.unzip(
                    posixpath.join(self._folderPath, tempSubFolder), tempZip
                )
                tempShpFullPath, encoding = jpDataCensus.performJoin(
                    posixpath.join(self._folderPath, tempSubFolder),
                    year,
                    tempShpFileName,
                    tempCsvFileName,
                )
                self._add_map(
                    tempShpFullPath,
                    name_muni + name_muni_suffix + " (" + year + ")",
                    tempQmlFile,
                    encoding=encoding,
                )





    def myPB_Addr_1_clicked(self):
        if self._dw.myPB_Addr_1.text() == self._ui.tr("Download"):
            self._dl_url_zip = []
            self._dl_iter = 0
            for i in range(1, 48):
                if not os.path.exists(
                    posixpath.join(
                        self._folderPath,
                        "Addr",
                        jpDataAddr.get_zip(i),
                    )
                ) and not jpDataAddr.get_csv_fullpath(i, self._folderPath):
                    self._dl_url_zip.append(
                        {
                            "year": "2024",
                            "url": jpDataAddr.get_url(i),
                            "zip": jpDataAddr.get_zip(i),
                            "subfolder": "Addr",
                        }
                    )
            if len(self._dl_url_zip) > 0:
                self._download_iter_2()
        elif self._dw.myPB_Addr_1.text() == self._ui.tr("Jump"):
            lon, lat = jpDataAddr.get_lonlat_by_addr(
                self._folderPath,
                str(self._dw.myCB_Addr_1.currentText()),
                str(self._dw.myCB_Addr_2.currentText()),
                str(self._dw.myCB_Addr_3.currentText()),
                str(self._dw.myCB_Addr_4.currentText()),
            )

            if lon is None or lat is None:
                return

            point_jgd2011 = QgsPointXY(lon, lat)

            # Transform to project CRS
            crs_src = QgsCoordinateReferenceSystem("EPSG:6668")  # JGD2011
            crs_dest = self._iface.mapCanvas().mapSettings().destinationCrs()
            transform = QgsCoordinateTransform(crs_src, crs_dest, QgsProject.instance())
            point_project = transform.transform(point_jgd2011)

            # Set canvas center
            canvas = self._iface.mapCanvas()
            canvas.setCenter(point_project)
            canvas.refresh()

    def _myCB_Addr_1_changed(self):
        if not jpDataAddr.set_cb_cities(
            self._dw.myCB_Addr_2,
            self._folderPath,
            self._dw.myCB_Addr_1.currentText(),
        ):
            self._dw.myPB_Addr_1.setText(self._ui.tr("Download"))
            self.setLabel(self._ui.tr("Missing address data."))
            self._dl_status = "ADDRESS"
        else:
            self._dw.myPB_Addr_1.setText(self._ui.tr("Jump"))