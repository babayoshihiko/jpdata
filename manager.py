# -*- coding: utf-8 -*-
import os, posixpath, tempfile
from qgis.PyQt.QtCore import Qt, QSettings, QTranslator, QCoreApplication, QUrl
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
    QgsWkbTypes
)

from .i18n import TR
from .ui_handler import JPDataUIHandler
from . import jpDataDownloader
from . import jpDataUtils
#from . import jpDataLNI
from . import jpDataCensus
from . import jpDataMuni
from . import jpDataMesh
from . import jpDataAddr
from .jpdata_lni import jpDataLNI
from .jpdata_mhlw import jpDataMHLW


class JPDataManager:
    def __init__(self, iface):
        self._iface = iface
        self._plugin_dir = os.path.dirname(__file__)

        self._dw = None
        self._ui = None
        self._lang = "e"
        if QgsSettings().value("locale/userLocale", "en")[:2] == "ja":
            self._lang = "j"

        self._folderPath = QSettings().value("jpdata/FolderPath", "~")
        self._proxyServer = QSettings().value("jpdata/ProxyServer", "http://")
        #self._land_info = jpDataUtils.getMapsFromCsv2(self._lang)
        self.LNI = jpDataLNI()
        self._GSI = jpDataUtils.getTilesFromCsv()
        self.MHLW = jpDataMHLW()
        self.LNI.set_download_folder(self._folderPath)
        self.LNI.set_lang(self._lang)
        self.MHLW.set_download_folder(self._folderPath)
        self.MHLW.set_lang(self._lang)

        self._downloader = jpDataDownloader.DownloadThread()
        self._dl_status = ""
        self._dl_url_zip = []
        self._dl_iter = 0
        self._name_map_prev = ""

        self._verbose = True

    def run(self):
        if not self._dw:
            from .jpdata_dockwidget import jpdataDockWidget

            self._dw = jpdataDockWidget()
            self._ui = JPDataUIHandler(self._dw)
            self.connect_signals()
            self.setup_initial_ui_state()

        if self._ui:
            self._ui.init_tabs(self.LNI,
                               self._folderPath,
                               self.MHLW)
            jpDataCensus.set_year_items(self._dw.myComboBox31, 2000)

        # QGIS 4 compatible
        dock_area = (
            Qt.DockWidgetArea.LeftDockWidgetArea
            if hasattr(Qt, "DockWidgetArea")
            else Qt.LeftDockWidgetArea
        )
        self._iface.addDockWidget(dock_area, self._dw)
        self._dw.show()

    def setup_initial_ui_state(self):
        if self._folderPath != "~":
            self._dw.myLabel1.setText(self._folderPath)
            self._dw.myTabWidget.setCurrentIndex(0)
        else:
            self._dw.myLabel1.setText(TR.CHOOSE_FOLDER_INIT())
            self._dw.myTabWidget.setCurrentIndex(5)

        if self._proxyServer:
            self._dw.myLineEditSetting1.setText(self._proxyServer)

        self._dw.myLineEditSetting3.setEchoMode(
            QLineEdit.EchoMode.Password
            if hasattr(QLineEdit, "EchoMode")
            else QLineEdit.Password
        )

        for row in self._GSI:
            self._dw.myListWidget23.addItem(row["name_" + self._lang])


    def connect_signals(self):
        dw = self._dw
        # Tab 1
        dw.myPushButton2.clicked.connect(self.chooseFolder)
        dw.myPushButton11.clicked.connect(self._tab1_download_all)
        dw.myPushButton14.clicked.connect(self._tab1_add_map)
        dw.myPushButton15.clicked.connect(self.tab1Web)
        dw.myListWidget11.itemSelectionChanged.connect(self.LW11_itemSelectionChanged)
        dw.myListWidget12.itemSelectionChanged.connect(self.LW12_itemSelectionChanged)
        dw.myComboBox11.currentIndexChanged.connect(self._cb11_changed)

        # Tab 2
        dw.myPushButton25.clicked.connect(self.addTile)

        # Tab 3
        dw.myPushButton31.clicked.connect(self._tab3_download_all)
        dw.myPushButton32.clicked.connect(self._tab3_add_map)
        dw.myListWidget31.currentItemChanged.connect(
            self._LW31_currentItemChanged
        )  ## NEEDS REFACTORING to itemSelectionChanged
        dw.myListWidget32.itemSelectionChanged.connect(self._LW32_itemSelectionChanged)
        dw.myComboBox32.currentIndexChanged.connect(self._LW32_itemSelectionChanged)

        # Tab MHLW
        dw.myLW_MHLW.currentRowChanged.connect(self._mhlw_service_changed)
        dw.myPB_MHLW_1.clicked.connect(self._tab_mhlw_web)
        dw.myPB_MHLW_2.clicked.connect(self._tab_mhlw_download_all)
        dw.myPB_MHLW_3.clicked.connect(self._tab_mhlw_add_map)

        # Tab 4 / Settings
        dw.myTabWidget.currentChanged.connect(self._tab_changed)
        dw.myCB_Addr_1.currentIndexChanged.connect(self._myCB_Addr_1_changed)
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

    def setLabel(self, message, critical=False):
        message = str(message)
        self._dw.myLabelStatus.setText(message)
        if self._verbose:
            jpDataUtils.printLog(message)
        if critical:
            self._iface.messageBar().pushMessage(
                "Error",
                message,
                1,
                duration=10,
            )

    def unload(self):
        if self._dw:
            self._iface.removeDockWidget(self._dw)
            self._dw.deleteLater()
            self._dw = None
            self._ui = None

    def _test_verbose(self):
        pass
        # This is a method for local testing purpose.

    def _add_map_old(
        self,
        shpFileFullPath,
        layerName,
        qmlFileName=None,
        encoding="CP932",
        epsg=None,
    ):
        # --- Create layer ---
        if shpFileFullPath is None:
            self.setLabel(TR.CANNOT_FIND_FILE_LAYER(layerName))
            return None
        layer = QgsVectorLayer(shpFileFullPath, layerName, "ogr")
        if not layer.isValid():
            self.setLabel(TR.CANNOT_LOAD_LAYER(layerName))
            return None

        layer.setProviderEncoding(encoding)

        # --- CRS ---
        if epsg:
            epsg_str = str(epsg).strip()
            if epsg_str.upper().startswith("EPSG:"):
                epsg_str = epsg_str[5:]
            if epsg_str.isdigit():
                epsg_int = int(epsg_str)
                epsg = epsg_int
                crs = QgsCoordinateReferenceSystem.fromEpsgId(epsg)
                if not crs.isValid():
                    self.setLabel(TR.INVALID_EPSG(epsg))
                layer.setCrs(crs)

        # --- Check geometry ---
        if not self._dw.myCheckBox2.isChecked():
            count_invalid = jpDataUtils.count_invalid_geometry(layer)
            if count_invalid > 0:
                layer.setName(f"{layerName} [invalid]")
                self.setLabel(TR.INVALID_GEOM(count_invalid))

        # --- Style from QML file ---
        if qmlFileName:
            qml_path = posixpath.join(self._plugin_dir, "qml", qmlFileName)
            if os.path.isfile(qml_path):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_qml = posixpath.join(temp_dir, qmlFileName)

                    with open(qml_path, "r") as f:
                        contents = f.read().replace("PLUGIN_DIR", self._plugin_dir)

                    with open(temp_qml, "w") as f:
                        f.write(contents)

                    if layer.loadNamedStyle(temp_qml):
                        layer.triggerRepaint()

        # --- Add to the current project ---
        QgsProject.instance().addMapLayer(layer)

        return layer

    def _add_map(
        self,
        shpFileFullPath,
        layerName,
        qmlFileName=None,
        encoding="CP932",
        epsg=None,
        xField=None,
        yField=None,
    ):

        if shpFileFullPath is None:
            self.setLabel(TR.CANNOT_FIND_FILE_LAYER(layerName))
            return None

        # ------------------------------
        # Create layer
        # ------------------------------
        if xField and yField:

            uri = (
                f"file:///{shpFileFullPath}"
                f"?encoding={encoding}"
                f"&delimiter=,"
                f"&xField={xField}"
                f"&yField={yField}"
            )

            layer = QgsVectorLayer(uri, layerName, "delimitedtext")

        else:

            layer = QgsVectorLayer(
                shpFileFullPath,
                layerName,
                "ogr",
            )

            layer.setProviderEncoding(encoding)

        if not layer.isValid():
            self.setLabel(TR.CANNOT_LOAD_LAYER(layerName))
            return None

        # --- CRS ---
        if epsg:
            epsg_str = str(epsg).strip()

            if epsg_str.upper().startswith("EPSG:"):
                epsg_str = epsg_str[5:]

            if epsg_str.isdigit():

                epsg_int = int(epsg_str)
                crs = QgsCoordinateReferenceSystem.fromEpsgId(epsg_int)

                if crs.isValid():
                    layer.setCrs(crs)
                else:
                    self.setLabel(TR.INVALID_EPSG(epsg))

        # --- Check geometry ---
        geom_type = layer.geometryType()
        if (
            geom_type != QgsWkbTypes.PointGeometry
            and not self._dw.myCheckBox2.isChecked()
        ):
            count_invalid = jpDataUtils.count_invalid_geometry(layer)
            if count_invalid > 0:
                layer.setName(f"{layerName} [invalid]")
                self.setLabel(TR.INVALID_GEOM(count_invalid))

        # --- Style from QML file ---
        if qmlFileName:
            qml_path = posixpath.join(self._plugin_dir, "qml", qmlFileName)
            if os.path.isfile(qml_path):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_qml = posixpath.join(temp_dir, qmlFileName)

                    with open(qml_path, "r") as f:
                        contents = f.read().replace("PLUGIN_DIR", self._plugin_dir)

                    with open(temp_qml, "w") as f:
                        f.write(contents)

                    if layer.loadNamedStyle(temp_qml):
                        layer.triggerRepaint()

        # --- Add to the current project ---
        QgsProject.instance().addMapLayer(layer)

        return layer


    def LW11_itemSelectionChanged(self):
        if len(self._dw.myListWidget11.selectedItems()) == 0:
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()

        thisLandNum = self.LNI.get_records()[name_map]

        self._dw.myLabelStatus.setText(thisLandNum.get("code_map", ""))

        str_current_LW12_selected = [
            item.text() for item in self._dw.myListWidget12.selectedItems()
        ]
        str_new_LW12_text = []
        bol_redraw_LW12 = True
        bol_show_LW13 = False
        muni_type = thisLandNum.get("type_muni", "").lower()

        def all_prefs():
            return [jpDataUtils.getPrefNameByCode(code, self._lang) for code in range(1, 48)]

        if muni_type in ("", "allprefs"):
            if self.LNI.get_prev_name() == "" or self.LNI.get_records()[self.LNI.get_prev_name()].get(
                "type_muni", ""
            ).lower() not in ("", "allprefs", "mesh1"):
                str_new_LW12_text = all_prefs()
            else:
                bol_redraw_LW12 = False
                self._dw.myListWidget13.hide()
        elif muni_type == "single":
            str_new_LW12_text = [TR.NATIONWIDE()]
        elif muni_type in ("regional", "detail"):
            if muni_type == "detail":
                bol_show_LW13 = True
            str_new_LW12_text = self.LNI.get_prefs(name_map)
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

    def _tab1_clear(self, bol_show_LW13):
        self._dw.myListWidget12.clear()
        mode = (
            QAbstractItemView.SelectionMode.SingleSelection
            if bol_show_LW13
            else QAbstractItemView.SelectionMode.ExtendedSelection
        )
        # QGIS 3/4 compatible
        if not hasattr(QAbstractItemView, "SelectionMode"):
            mode = (
                QAbstractItemView.SingleSelection
                if bol_show_LW13
                else QAbstractItemView.ExtendedSelection
            )

        self._dw.myListWidget12.setSelectionMode(mode)
        if bol_show_LW13:
            self._dw.myListWidget13.show()
        else:
            self._dw.myListWidget13.hide()

    def LW12_itemSelectionChanged(self):
        if (
            len(self._dw.myListWidget11.selectedItems()) == 0
            or len(self._dw.myListWidget12.selectedItems()) == 0
        ):
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()
        name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        self._tab1_check_year(name_map)
        thisLandNum = self.LNI.get_records()[name_map]
        if thisLandNum["type_muni"].lower() in ("detail", "mesh1"):
            self._tab1_set_LW13(name_pref)

    def _tab1_check_year(self, name_map):
        years = []
        name_pref = None
        record = self.LNI.get_records()[name_map]
        if len(self._dw.myListWidget12.selectedItems()) > 0:
            if record["type_muni"].lower() != "mesh1":
                name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        years = self.LNI.get_years(name_map, name_pref)
        self._ui.set_years_CB(years, self._dw.myComboBox11)
        self._tab1_set_LW13()

    def _cb11_changed(self, index):
        self._tab1_set_LW13()


    def _tab1_set_LW13(self, name_pref=None):
        str_selected_details = {
            item.text()
            for item in self._dw.myListWidget13.selectedItems()
        }
        str_current_text = None
        if self._dw.myListWidget13.currentItem():
            str_current_text = self._dw.myListWidget13.currentItem().text()

        if len(self._dw.myListWidget11.selectedItems()) == 0:
            return
        if name_pref is None:
            if len(self._dw.myListWidget12.selectedItems()) == 0:
                return
            name_pref = self._dw.myListWidget12.selectedItems()[0].text()

        str_name_j = self._dw.myListWidget11.selectedItems()[0].text()
        str_year = self._dw.myComboBox11.currentText()
        if not str_year.strip():
            return

        thisLandNum = self.LNI.get_records()[str_name_j]
        if thisLandNum["type_muni"].lower() not in ("detail", "mesh1"):
            return

        self._dw.myListWidget13.clear()
        self._dw.myListWidget13.show()

        if thisLandNum["type_muni"].lower() == "detail":
            details = self.LNI.get_details(
                thisLandNum["code_map"], name_pref, str_year
            )
        else:
            details = jpDataMesh.getMesh1ByPrefName(name_pref)

        for detail in details:
            item = QListWidgetItem(detail)
            self._dw.myListWidget13.addItem(item)

            if detail in str_selected_details:
                item.setSelected(True)

            if detail == str_current_text:
                self._dw.myListWidget13.setCurrentItem(item)


    def tab1Web(self):
        items = self._dw.myListWidget11.selectedItems()
        if items:
            thisLandNum = self.LNI.get_records()[items[0].text()]
            QDesktopServices.openUrl(QUrl(thisLandNum["source"]))


    def chooseFolder(self):
        from qgis.PyQt.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(
            self._iface.mainWindow(), TR.CHOOSE_FOLDER(), self._folderPath
        )
        if folder:
            self._folderPath = folder
            QSettings().setValue("jpdata/FolderPath", folder)
            self.LNI.set_download_folder(folder)
            self.MHLW.set_download_folder(folder)
            self._dw.myLabel1.setText(folder)

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
            if current_gsi["name_" + self._lang] == tile_name:
                tile_url_base = current_gsi["url"]
                zoom_min = current_gsi["zoom_min"]
                zoom_max = current_gsi["zoom_max"]
                break

        tile_url = (
            "type=xyz&url="
            + tile_url_base
            + "&zmax="
            + zoom_max
            + "&zmin="
            + zoom_min
            + "&crs=EPSG3857"
        )
        layer = QgsRasterLayer(tile_url, tile_name, "wms")
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)

    def tab1CheckSelected(self):
        if not self._dw.myListWidget11.selectedItems():
            self._dw.myLabelStatus.setText(TR.CHOOSE_MAP_TYPE())
            return False
        if not self._dw.myListWidget12.selectedItems():
            self._dw.myLabelStatus.setText(TR.CHOOSE_PREFECTURE_REGION())
            return False
        return True

    def _tab_changed(self, index):
        """Called whenever the current tab changes."""
        if index == 3:  # tab #3 (4th tab)
            self._dw.myCB_Addr_1.setCurrentIndex(12)

    def _tab1_download_all(self):
        if self._dw.myPushButton11.text() == TR.CANCEL():
            self.cancel_download()
            return
        self._tab1_iter(process="download")

    def _tab1_add_map(self):
        self._tab1_iter(process="add")

    # year = 2023 and so on
    # type must be one of ["regional","detail","single","","census"]
    # selection_code is a dictionary of codes
    #     (prefectural codes, municipal codes and so on)
    # a list of "code_pref"s (type = "" or "region")
    # or a list of "code_muni"s (type = "census")
    def _download_iter_2(self):
        _start_download = False

        for x in range(self._dl_iter, len(self._dl_url_zip)):
            tempUrl = self._dl_url_zip[x]["url"]
            tempZipFileName = self._dl_url_zip[x]["zip"]
            tempSubFolder = self._dl_url_zip[x]["subfolder"]
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
                # The file exists, so skip to the next one
                self.setLabel(TR.FILE_EXISTS(tempZipFileName))
        if _start_download:
            self._dw.progressBar.setValue(0)
            self._ui.enable_download(False)
            self._dl_iter = x + 1
            self.start_download(tempUrl, tempSubFolder, tempZipFileName)
        else:
            self._ui.enable_download()
            self._dl_iter = 0


    def start_download(self, url, subFolder, zipFileName):
        if not os.path.exists(posixpath.join(self._folderPath, subFolder)):
            os.mkdir(posixpath.join(self._folderPath, subFolder))

        if not os.path.exists(posixpath.join(self._folderPath, subFolder, zipFileName)):
            self.set_proxy()
            self.setLabel(TR.DOWNLOADING(zipFileName))
            self._downloader.setUrl(url)
            self._downloader.setFilePath(
                posixpath.join(self._folderPath, subFolder, zipFileName)
            )
            self._ui.enable_download(False)
            if self._dw.myCheckBox1.isChecked():
                self._downloader.download_wo_thread()
                self._ui.enable_download()
            else:
                self._downloader.start()
        else:
            # The file existance was checked, so this should not happen, but just in case
            self.setLabel(TR.FILE_EXISTS(zipFileName))
            self._ui.enable_download()

    def download_finished(self, success):
        current_text = self._dw.myLabelStatus.text()
        self.setLabel(current_text + TR.DONE())
        self._ui.enable_download()
        self._dw.progressBar.setValue(100)

        if len(self._dl_url_zip) > 0 and self._dl_iter < len(self._dl_url_zip):
            # Download next
            self._download_iter_2()
        else:
            # All downloads finished
            self._dl_iter = 0
            self._dl_url_zip = []
            if self._dl_status == "ADDRESS":
                self._dw.myPB_Addr_1.setText(TR.JUMP())
                self._myCB_Addr_1_changed()

    def cancel_download(self):
        self._dl_url_zip = []
        if self._downloader is not None:
            current_text = self._dw.myLabelStatus.text()
            self.setLabel(current_text + TR.CANCELLED())
            self._downloader.stop()
        else:
            self._downloader = jpDataDownloader.DownloadThread()
        self._ui.enable_download()

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

        designated_cities = jpDataMuni.get_all_designated_cities(year, self._lang)

        rows = jpDataMuni.getMuniFromPrefName(name_pref, self._lang)
        self._dw.myListWidget32.clear()

        for row in rows:
            name = row["name_muni_" + self._lang]
            if not name:
                continue
            item = QListWidgetItem(name)
            if name in designated_cities:
                if hasattr(Qt, "ItemFlag"):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                gray = Qt.GlobalColor.gray if hasattr(Qt, "GlobalColor") else Qt.gray
                item.setForeground(gray)

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
            details = jpDataMesh.getMesh1ByPrefMuniName(name_pref, name_munis)

        for detail in details:
            self._dw.myListWidget33.addItem(detail)

    def tab3CheckSelected(self):
        if len(self._dw.myListWidget31.selectedItems()) == 0:
            self.setLabel(TR.CHOOSE_PREFECTURE())
            return False
        if self._dw.myComboBox32.currentIndex() == 0:
            if len(self._dw.myListWidget32.selectedItems()) == 0:
                self.setLabel(TR.CHOOSE_MUNICIPALITY())
                return False
        else:
            if len(self._dw.myListWidget33.selectedItems()) == 0:
                self.setLabel(TR.CHOOSE_MESH())
                return False
        return True

    def _tab3_download_all(self):
        if self._dw.myPushButton31.text() == TR.CANCEL():
            self.cancel_download()
            return
        self._tab3_iter(process="download")

    def _tab3_add_map(self):
        self._tab3_iter(process="add")

    def myPB_Addr_1_clicked(self):
        if self._dw.myPB_Addr_1.text() == TR.DOWNLOAD():
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
        elif self._dw.myPB_Addr_1.text() == TR.JUMP():
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
            self._dw.myPB_Addr_1.setText(TR.DOWNLOAD())
            self.setLabel(TR.ADDRESS_MISSING())
            self._dl_status = "ADDRESS"
        else:
            self._dw.myPB_Addr_1.setText(TR.JUMP())

    def _tab1_iter(self, process):
        if not self.tab1CheckSelected():
            return
        this_landmum = self.LNI.get_records()[
            self._dw.myListWidget11.selectedItems()[0].text()
        ]
        year = self._dw.myComboBox11.currentText()
        list_code = []
        detail = None

        if this_landmum["type_muni"].lower() == "mesh1":
            for code_mesh1 in self._dw.myListWidget13.selectedItems():
                list_code.append(code_mesh1.text())
        elif this_landmum["type_muni"] == "single":
            list_code = [""]
        else:
            for name_pref in self._dw.myListWidget12.selectedItems():
                list_code.append(jpDataUtils.getPrefCodeByName(name_pref.text()))
            if (
                this_landmum["type_muni"].lower() == "detail"
                and self._dw.myListWidget13.selectedItems()
            ):
                detail = self._dw.myListWidget13.selectedItems()[0].text()

        count_prefs = len(self._dw.myListWidget12.selectedItems())

        if process == "add":
            for x in range(len(list_code)):
                (
                    zip_filename,
                    shp_filename,
                    altdir,
                    qml_filename,
                    epsg,
                    encoding,
                    subfolder,
                    layer_name,
                ) = self.LNI.get_zip_shp(
                    self._dw.myListWidget11.selectedItems()[0].text(),
                    year,
                    (
                        self._dw.myListWidget12.selectedItems()[x].text()
                        if x < count_prefs
                        else ""
                    ),
                    list_code[x],
                    detail=detail,
                )
                shp_full_path = jpDataUtils.unzipAndGetShp(
                    posixpath.join(self._folderPath, subfolder),
                    year,
                    zip_filename,
                    shp_filename,
                    altdir,
                    list_code[x],
                    epsg=epsg,
                    encoding=encoding,
                )
                self._add_map(
                    shp_full_path,
                    layer_name,
                    qml_filename,
                    encoding=encoding,
                    epsg=epsg,
                )
        elif process == "download":
            self._dl_url_zip = []
            self._dl_iter = 0
            for x in range(len(list_code)):
                url, zip_filename, subfolder = self.LNI.get_url_zip(
                    self._dw.myListWidget11.selectedItems()[0].text(),
                    year,
                    (
                        self._dw.myListWidget12.selectedItems()[x].text()
                        if x < count_prefs
                        else ""
                    ),
                    list_code[x],
                    detail=detail,
                )
                if zip_filename is not None:
                    self._dl_url_zip.append(
                        {
                            "year": year,
                            "url": url,
                            "zip": zip_filename,
                            "subfolder": subfolder,
                        }
                    )
            self._download_iter_2()

    def _tab3_iter(self, process):
        if not self.tab3CheckSelected():
            return
        year = self._dw.myComboBox31.currentText()
        name_pref = self._dw.myListWidget31.selectedItems()[0].text()
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        subfolder, qml_filename = jpDataCensus.get_subfolder_qml(
            self._dw.myComboBox32.currentIndex(), year
        )

        name_muni_suffix = ""
        if self._dw.myComboBox32.currentIndex() == 0:
            # Get municipality names
            list_item = self._dw.myListWidget32.selectedItems()
        else:
            # Get mesh codes
            list_item = self._dw.myListWidget33.selectedItems()
            if self._dw.myComboBox32.currentIndex() == 1:
                name_muni_suffix = " " + TR.X3_MESH()
            elif self._dw.myComboBox32.currentIndex() == 2:
                name_muni_suffix = " " + TR.X4_MESH()
            elif self._dw.myComboBox32.currentIndex() == 3:
                name_muni_suffix = " " + TR.X5_MESH()
            elif self._dw.myComboBox32.currentIndex() == 4:
                name_muni_suffix = " " + TR.X6_MESH()

        if process == "add":
            for _item_name_or_code in list_item:
                if self._dw.myComboBox32.currentIndex() == 0:
                    row = jpDataMuni.getRowFromNames(
                        name_pref, _item_name_or_code.text()
                    )
                    code_muni = row["code_muni"]
                else:
                    code_muni = _item_name_or_code.text()
                zip_filename, shp_filename = jpDataCensus.getZipShp(
                    year,
                    code_pref,
                    code_muni,
                    self._dw.myComboBox32.currentIndex(),
                )

                shp_full_path = jpDataUtils.unzipAndGetShp(
                    posixpath.join(self._folderPath, subfolder),
                    year,
                    zip_filename,
                    shp_filename,
                )

                if shp_full_path is None:
                    self.setLabel(
                        TR.CANNOT_FIND_SHP_FILE(shp_filename),
                        critical=True,
                    )
                    break

                if shp_full_path != "":
                    url, zip_filename, subfolder = jpDataCensus.getAttr(
                        year,
                        code_pref,
                        code_muni,
                        self._dw.myComboBox32.currentIndex(),
                    )
                    jpDataUtils.unzip(
                        posixpath.join(self._folderPath, subfolder), zip_filename
                    )
                    csv_filename = jpDataCensus.get_attr_csv_filename(
                        year,
                        code_pref,
                        code_muni,
                        self._dw.myComboBox32.currentIndex(),
                        self._folderPath,
                    )
                    encoding = "CP932"
                    if csv_filename is not None:
                        shp_full_path, encoding = jpDataCensus.perform_join(
                            posixpath.join(self._folderPath, subfolder),
                            year,
                            shp_filename,
                            csv_filename,
                        )
                    else:
                        self.setLabel("")
                    self._add_map(
                        shp_full_path,
                        _item_name_or_code.text()
                        + name_muni_suffix
                        + " ("
                        + year
                        + ")",
                        qml_filename,
                        encoding=encoding,
                    )
        elif process == "download":
            self._dl_url_zip = []
            self._dl_iter = 0
            for _item_name_or_code in list_item:
                if self._dw.myComboBox32.currentIndex() == 0:
                    row = jpDataMuni.getRowFromNames(
                        name_pref, _item_name_or_code.text()
                    )
                    code_muni = row["code_muni"]
                else:
                    code_muni = _item_name_or_code.text()

                attr_url, attr_zip, attr_sub = jpDataCensus.getAttr(
                    year, code_pref, code_muni, self._dw.myComboBox32.currentIndex()
                )
                shp_url, shp_zip, shp_sub = jpDataCensus.getZip(
                    year, code_pref, code_muni, self._dw.myComboBox32.currentIndex()
                )

                if attr_zip:
                    self._dl_url_zip.append(
                        {
                            "year": year,
                            "url": attr_url,
                            "zip": attr_zip,
                            "subfolder": attr_sub,
                        }
                    )
                if shp_zip:
                    self._dl_url_zip.append(
                        {
                            "year": year,
                            "url": shp_url,
                            "zip": shp_zip,
                            "subfolder": shp_sub,
                        }
                    )
            self._download_iter_2()


    def _mhlw_service_changed(self, row):
        item = self._dw.myLW_MHLW.item(row)
        if item is None:
            return
        service_name = item.text()
        years = self.MHLW.get_years(service_name)
        self._ui.set_years_CB(years, self._dw.myCB_MHLW)


    def _tab_mhlw_iter(self, process):
        # if not self.tab1CheckSelected():
        #     return
        year = self._dw.myCB_MHLW.currentText()
        these_services = self._dw.myLW_MHLW.selectedItems()

        if process == "add":
            for this_service in these_services:
                (
                    zip_filename,
                    shp_filename,
                    altdir,
                    qml_filename,
                    epsg,
                    encoding,
                    subfolder,
                    layer_name,
                    xField,
                    yField
                ) =  self.MHLW.get_zip(
                    year,
                    this_service.text(),
                    type="add"
                )
                shp_full_path = jpDataUtils.unzipAndGetShp(
                    posixpath.join(self._folderPath, subfolder),
                    year,
                    zip_filename,
                    shp_filename,
                    altdir,
                    epsg=epsg,
                    encoding=encoding,
                )
                self._add_map(
                    shp_full_path,
                    layer_name,
                    qml_filename,
                    encoding=encoding,
                    epsg=epsg,
                    xField=xField,
                    yField=yField
                )
        elif process == "download":
            self._dl_url_zip = []
            self._dl_iter = 0
            for this_service in these_services:
                url, zip_filename, subfolder = self.MHLW.get_zip(
                    year,
                    this_service.text(),
                    type="urlzip"
                )
                if zip_filename is not None:
                    self._dl_url_zip.append(
                        {
                            "year": year,
                            "url": url,
                            "zip": zip_filename,
                            "subfolder": subfolder,
                        }
                    )
            self._download_iter_2()

    def _tab_mhlw_web(self):
        items = self._dw.myLW_MHLW.selectedItems()
        if items:
            thisLandNum = self.MHLW.get_records()[items[0].text()]
            QDesktopServices.openUrl(QUrl(thisLandNum["source"]))

    def _tab_mhlw_download_all(self):
        if self._dw.myPB_MHLW_2.text() == TR.CANCEL():
            self.cancel_download()
            return
        self._tab_mhlw_iter(process="download")

    def _tab_mhlw_add_map(self):
        self._tab_mhlw_iter(process="add")

# End of manager.py
