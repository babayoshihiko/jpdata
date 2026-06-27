# -*- coding: utf-8 -*-
import os, posixpath, tempfile
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.core import (
    QgsProject,
    QgsSettings,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsWkbTypes
)

from .i18n import TR
from .ui_handler import JPDataUIHandler
from . import jpDataDownloader
from . import jpDataUtils
#from . import jpDataLNI
#from . import jpDataCensus
#from . import jpDataMuni
#from . import jpDataAddr
from .jpdata_lni import jpDataLNI
from .jpdata_census import jpDataCensus
from .jpdata_mhlw import jpDataMHLW
from .jpdata_muni import jpDataMuni


class JPDataManager:
    _verbose = True

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
        self._Muni = jpDataMuni.instance()
        self._Muni.set_download_folder(self._folderPath)
        self._Muni.set_lang(self._lang)
        self._LNI = jpDataLNI.instance()
        self._Census = jpDataCensus.instance()
        self._MHLW = jpDataMHLW.instance()
        self._LNI.set_download_folder(self._folderPath)
        self._LNI.set_lang(self._lang)
        self._Census.set_download_folder(self._folderPath)
        self._MHLW.set_download_folder(self._folderPath)
        self._MHLW.set_lang(self._lang)
        self._GSI = jpDataUtils.getTilesFromCsv()

        self._downloader = jpDataDownloader.DownloadThread()
        self._dl_status = ""
        self._dl_url_zip = []
        self._dl_iter = 0

    def run(self):
        if not self._dw:
            from .jpdata_dockwidget import jpdataDockWidget
            self._dw = jpdataDockWidget()

        self._ui = JPDataUIHandler(self._iface, self._dw, self._lang)
        self._connect_signals()
        self._setup_initial_ui_state()

        if self._ui:
            self._ui.init_tabs(self._folderPath)
            # jpDataCensus.set_year_items(self._dw.myComboBox31, 2000)

        # QGIS 4 compatible
        dock_area = (
            Qt.DockWidgetArea.LeftDockWidgetArea
            if hasattr(Qt, "DockWidgetArea")
            else Qt.LeftDockWidgetArea
        )
        self._iface.addDockWidget(dock_area, self._dw)
        self._dw.show()

    def _setup_initial_ui_state(self):
        if self._folderPath != "~":
            self._dw.myLabel1.setText(self._folderPath)
            self._dw.myTabWidget.setCurrentIndex(0)
        else:
            self._dw.myLabel1.setText(TR.CHOOSE_FOLDER_INIT())
            self._dw.myTabWidget.setCurrentIndex(5)

        if self._proxyServer:
            self._dw.myLineEditSetting1.setText(self._proxyServer)




    def _connect_signals(self):
        # Tab LNI
        self._dw.myPushButton2.clicked.connect(self.chooseFolder)
        self._dw.myPushButton11.clicked.connect(self._tab1_download_all)
        self._dw.myPushButton14.clicked.connect(self._tab1_add_map)

        # Tab 2
        self._dw.myPushButton25.clicked.connect(self._addTile)
        for row in self._GSI:
            self._dw.myListWidget23.addItem(row["name_" + self._lang])
        
        # Tab 3
        self._dw.myPushButton31.clicked.connect(self._tab3_download_all)
        self._dw.myPushButton32.clicked.connect(self._tab3_add_map)

        # Tab MHLW
        self._dw.myPB_MHLW_2.clicked.connect(self._tab_mhlw_download_all)
        self._dw.myPB_MHLW_3.clicked.connect(self._tab_mhlw_add_map)

        # Tab Address
        self._dw.myPB_Addr_1.clicked.connect(self._myPB_Addr_dl_clicked)


        # For local testing purpose
        if self._verbose:
            self._dw.myPushButtonTest.clicked.connect(self._test_verbose)
        else:
            self._dw.myPushButtonTest.hide()

        # Downloader
        self._downloader.setProxyServer(self._proxyServer)
        self._downloader.progress.connect(self._dw.progressBar.setValue)
        self._downloader.finished.connect(self._download_finished)

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






    def chooseFolder(self):
        from qgis.PyQt.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(
            self._iface.mainWindow(), TR.CHOOSE_FOLDER(), self._folderPath
        )
        if folder:
            self._folderPath = folder
            QSettings().setValue("jpdata/FolderPath", folder)
            self._LNI.set_download_folder(folder)
            self._MHLW.set_download_folder(folder)
            self._dw.myLabel1.setText(folder)

    def _addTile(self):
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

    def _tab1CheckSelected(self):
        if not self._dw.myListWidget11.selectedItems():
            self._dw.myLabelStatus.setText(TR.CHOOSE_MAP_TYPE())
            return False
        if not self._dw.myListWidget12.selectedItems():
            self._dw.myLabelStatus.setText(TR.CHOOSE_PREFECTURE_REGION())
            return False
        return True

    def _tab1_download_all(self):
        if self._dw.myPushButton11.text() == TR.CANCEL():
            self._cancel_download()
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
        _bol_start_download = False

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
                _bol_start_download = True
                break
            else:
                # The file exists, so skip to the next one
                self.setLabel(TR.FILE_EXISTS(tempZipFileName))
        if _bol_start_download:
            self._dw.progressBar.setValue(0)
            self._ui.enable_download(False)
            self._dl_iter = x + 1
            self._start_download(tempUrl, tempSubFolder, tempZipFileName)
        else:
            self._ui.enable_download()
            self._dl_iter = 0


    def _start_download(self, url, subFolder, zipFileName):
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

    def _download_finished(self):
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

    def _cancel_download(self):
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
            self._cancel_download()
            return
        self._tab3_iter(process="download")

    def _tab3_add_map(self):
        self._tab3_iter(process="add")


    def _tab1_iter(self, process):
        if not self._tab1CheckSelected():
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()
        this_landmum = self._LNI.get_record(name_map)
        year = self._dw.myComboBox11.currentText()
        list_code = []  # Either name_pref from LW12 or code_mesh from LW13 (multiple)
        detail = None   # detail from LW13 (single)

        if this_landmum["type_muni"].lower() == "mesh1":
            for code_mesh1 in self._dw.myListWidget13.selectedItems():
                list_code.append(code_mesh1.text())
        elif this_landmum["type_muni"] == "single":
            list_code = [""]
        else:
            for name_pref in self._dw.myListWidget12.selectedItems():
                list_code.append(name_pref.text())
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
                ) = self._LNI.get_zip_shp(
                    name_map,
                    year,
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
                url, zip_filename, subfolder = self._LNI.get_url_zip(
                    name_map,
                    year,
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
        if not self._tab3CheckSelected():
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




    def _tab_mhlw_iter(self, process):
        # if not self._tab1CheckSelected():
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
                ) =  self._MHLW.get_zip(
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
                url, zip_filename, subfolder = self._MHLW.get_zip(
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

    def _tab_mhlw_download_all(self):
        if self._dw.myPB_MHLW_2.text() == TR.CANCEL():
            self._cancel_download()
            return
        self._tab_mhlw_iter(process="download")

    def _tab_mhlw_add_map(self):
        self._tab_mhlw_iter(process="add")


    def _myPB_Addr_dl_clicked(self):
        self._dl_url_zip = []
        self._dl_iter = 0
        for i in range(1, 48):
            if not os.path.exists(
                posixpath.join(
                    self._folderPath,
                    "Addr",
                    self._Muni.get_zip(i),
                )
            ) and not self._Muni.get_csv_fullpath(i):
                self._dl_url_zip.append(
                    {
                        "year": "2024",
                        "url": self._Muni.get_url(i),
                        "zip": self._Muni.get_zip(i),
                        "subfolder": "Addr",
                    }
                )
        if len(self._dl_url_zip) > 0:
            self._download_iter_2()


# End of manager.py
