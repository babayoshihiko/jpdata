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
        self._Muni = jpDataMuni.instance()
        self._Muni.set_lang(self._lang)
        self._LNI = jpDataLNI.instance()
        self._Census = jpDataCensus.instance()
        self._MHLW = jpDataMHLW.instance()
        self._LNI.set_lang(self._lang)
        self._MHLW.set_lang(self._lang)
        self._GSI = jpDataUtils.getTilesFromCsv()
        self._set_download_fullpath(self._folderPath)

        self._downloader = jpDataDownloader.DownloadThread()
        #self._dl_status = ""
        #self._dl_url_zip = []
        #self._dl_iter = 0
    
    def _set_download_fullpath(self, fullpath):
        self._Muni.set_download_folder(fullpath)
        self._LNI.set_download_folder(fullpath)
        self._Census.set_download_folder(fullpath)
        self._MHLW.set_download_folder(fullpath)

    def run(self):
        if not self._dw:
            from .jpdata_dockwidget import jpdataDockWidget
            self._dw = jpdataDockWidget()

        self._ui = JPDataUIHandler(self._iface, self._dw, self._lang)
        self._connect_signals()
        self._setup_initial_ui_state()

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
            self._ui._tab_changed(0)
            self._dw.myTabWidget.setCurrentIndex(0)
        else:
            self._dw.myLabel1.setText(TR.CHOOSE_FOLDER_INIT())
            self._dw.myTabWidget.setCurrentIndex(5)

        if self._proxyServer:
            self._dw.myLineEditSetting1.setText(self._proxyServer)




    def _connect_signals(self):
        # Tab LNI
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


        # Downloader
        self._downloader.setProxyServer(self._proxyServer)
        self._downloader.progress.connect(self._dw.progressBar.setValue)
        self._downloader.finished.connect(self._download_finished)
        self._downloader.message.connect(self.setLabel)

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
        if self._ui is not None:
            self._ui.unload()
        if self._dw:
            self._iface.removeDockWidget(self._dw)
            self._dw.deleteLater()
            self._dw = None
            self._ui = None


    def _add_map(
        self,
        shpFileFullPath,
        layerName,
        qml=None,
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
            and self._dw.myCheckBox2.isChecked()
        ):
            count_invalid = jpDataUtils.count_invalid_geometry(layer)
            if count_invalid > 0:
                layer.setName(f"{layerName} [invalid]")
                self.setLabel(TR.INVALID_GEOM(count_invalid))

        # --- Style from QML file ---
        if qml:
            qml_path = posixpath.join(self._plugin_dir, "qml", qml)
            if os.path.isfile(qml_path):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_qml = posixpath.join(temp_dir, qml)

                    with open(qml_path, "r") as f:
                        contents = f.read().replace("PLUGIN_DIR", self._plugin_dir)

                    with open(temp_qml, "w") as f:
                        f.write(contents)

                    if layer.loadNamedStyle(temp_qml):
                        layer.triggerRepaint()

        # --- Add to the current project ---
        QgsProject.instance().addMapLayer(layer)

        return layer





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
            # QgsProject.instance().addMapLayer(layer)
            project = QgsProject.instance()
            root = project.layerTreeRoot()

            project.addMapLayer(layer, False)
            root.addLayer(layer)


    def _tab1CheckSelected(self):
        if not self._dw.myListWidget11.selectedItems():
            self._dw.myLabelStatus.setText(TR.CHOOSE_MAP_TYPE())
            return False
        name_map = str(self._dw.myListWidget11.selectedItems()[0].text())
        if not self._dw.myListWidget12.selectedItems():
            if not (self._dw.myListWidget13.selectedItems() and self._LNI.get_records()[name_map]["type_muni"].lower() == "mesh1"):
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

    def _tab3CheckSelected(self):
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
        year = self._dw.myComboBox11.currentText()
        list_code = []  # Either name_pref from LW12 or code_mesh from LW13 (multiple)
        name_pref = self._dw.myListWidget12.selectedItems()[0].text() if len(self._dw.myListWidget12.selectedItems()) > 0 else ""
        name_muni = self._dw.myListWidget13.selectedItems()[0].text() if len(self._dw.myListWidget13.selectedItems()) > 0 else ""
        detail = None   # detail from LW13 (single)
        type_muni = self._LNI.get_records()[name_map]["type_muni"].lower()

        if type_muni == "single":
            list_code = [""]
        elif type_muni == "" or type_muni == "regional":
            for item in self._dw.myListWidget12.selectedItems():
                list_code.append(item.text())
        elif type_muni == "mesh1":
            for item in self._dw.myListWidget13.selectedItems():
                list_code.append(item.text())
        elif type_muni == "detail":
            for item in self._dw.myListWidget13.selectedItems():
                list_code.append(item.text())

        if process == "add":
            for x in list_code:
                self._set_lni_source(type_muni, name_map, year, name_pref, x)
                jpDataUtils.unzip(self._LNI.get_record()["download_fullpath"], self._LNI.get_record()["zip"])
                shp_full_path = jpDataUtils.unzipAndGetShp(
                    self._LNI.get_record()["download_fullpath"],
                    year,
                    self._LNI.get_record()["zip"],
                    self._LNI.get_record()["shp"],
                    self._LNI.get_record()["altdir"]
                )
                if type_muni == "single":
                    layer_name =  self._LNI.get_record()["name_map"] + " (" + year + ")"
                elif type_muni == "" or type_muni == "regional":
                    layer_name =  self._LNI.get_record()["name_map"] + " (" + self._LNI.get_record()["name_pref"] + ", " + year + ")"
                elif type_muni == "mesh1":
                    layer_name =  self._LNI.get_record()["name_map"] + " (" + self._LNI.get_record()["code_mesh"] + ", " + year + ")"
                elif type_muni == "detail":
                    layer_name =  self._LNI.get_record()["name_map"] + " (" + self._LNI.get_record()["detail"] + ", " + year + ")"
                
                self._add_map(
                    shp_full_path,
                    layer_name,
                    qml=self._LNI.get_record()["qml"],
                    encoding=self._LNI.get_record()["encoding"],
                    epsg=self._LNI.get_record()["epsg"],
                )
        elif process == "download":
            for x in list_code:
                self._set_lni_source(type_muni, name_map, year, name_pref, x)
                self._downloader.addJob(
                    self._LNI.get_record()["url"],
                    posixpath.join(self._LNI.get_record()["download_fullpath"], self._LNI.get_record()["zip"])
                )
            self._downloader.start()

    def _set_lni_source(self, type_muni, name_map, year, name_pref, x):
        if type_muni in ("", "single", "regional"):
            self._LNI.set_record(
                name_map,
                year,
                name_pref=x,
                name_muni=None,
                code_mesh=None,
                detail=None,
            )

        elif type_muni == "mesh1":
            self._LNI.set_record(
                name_map,
                year,
                name_pref=name_pref,
                name_muni=None,
                code_mesh=x,
                detail=None,
            )
        elif type_muni == "detail":
            self._LNI.set_record(
                name_map,
                year,
                name_pref=name_pref,
                name_muni=None,
                code_mesh=None,
                detail=x,
            )


    def _tab3_iter(self, process):
        if not self._tab3CheckSelected():
            return

        year = self._dw.myComboBox31.currentText()
        name_pref = self._dw.myListWidget31.selectedItems()[0].text()
        source = self._dw.myComboBox32.currentIndex()

        name_muni = None
        if self._dw.myListWidget32.selectedItems():
            name_muni = self._dw.myListWidget32.selectedItems()[0].text()

        suffix = {
            0: "",
            1: " " + TR.X3_MESH(),
            2: " " + TR.X4_MESH(),
            3: " " + TR.X5_MESH(),
            4: " " + TR.X6_MESH(),
        }
        name_muni_suffix = suffix[source]

        if source == 0:
            list_item = self._dw.myListWidget32.selectedItems()
        else:
            list_item = self._dw.myListWidget33.selectedItems()

        if process == "download":
            self._downloader.clearJobs()
            #self._dl_url_zip = []
            #self._dl_iter = 0

        for item in list_item:
            record = self._set_census_source(
                source,
                year,
                name_pref,
                name_muni,
                item.text(),
            )

            if process == "add":
                self._add_census_layer(
                    year,
                    item.text(),
                    name_muni_suffix
                )
            elif process == "download":
                self._downloader.addJob(
                    record["attr_url"],
                    posixpath.join(self._folderPath, record["subfolder"], record["attr_zip"])
                )
                self._downloader.addJob(
                    record["url"],
                    posixpath.join(self._folderPath, record["subfolder"], record["zip"])
                )

        if process == "download":
            self._downloader.start()

    def _set_census_source(
        self,
        index_census,
        year,
        name_pref,
        name_muni,
        name_or_code,
    ):
        if index_census == 0:
            self._Census.set_record(
                index_census,
                year,
                name_pref,
                name_or_code,
                None,
            )
        else:
            self._Census.set_record(
                index_census,
                year,
                name_pref,
                name_muni,
                name_or_code,
            )
        return self._Census.get_record()

    def _add_census_layer(
        self,
        year,
        item_name,
        name_muni_suffix
    ):
        record = self._Census.get_record()
        jpDataUtils.unzip(record["download_fullpath"], record["zip"])
        jpDataUtils.unzip(record["download_fullpath"], record["attr_zip"])
        record["attr_csv"] = self._Census.set_attr_csv()
        shp_full_path = jpDataUtils.unzipAndGetShp(
            record["download_fullpath"],
            year,
            record["zip"],
            record["shp"],
        )

        if shp_full_path is None:
            self.setLabel(
                TR.CANNOT_FIND_SHP_FILE(record["shp"]),
                critical=True,
            )
            return

        if shp_full_path == "":
            return


        qml = record["qml"]
        encoding = record["encoding"]
        jpDataUtils.printDebugLog(record)
        if record["attr_csv"]:
            shp_full_path, encoding = self._Census.perform_join(
                record["download_fullpath"],
                year,
                record["shp"],
                record["attr_csv"],
            )
        else:
            jpDataUtils.printDebugLog("CSV for Census not found.")
            self.setLabel("")

        self._add_map(
            shp_full_path,
            f"{item_name}{name_muni_suffix} ({year})",
            qml,
            encoding=encoding,
        )




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
                    self._downloader.addJob(
                        url,
                        posixpath.join(self._folderPath, subfolder, zip_filename),
                    )
            self._downloader.start()


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
        name_pref = self._dw.myCB_Addr_1.currentText()
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        url = self._Muni.get_url(code_pref)
        zip = self._Muni.get_zip(code_pref)
        self._downloader.addJob(
            url,
            posixpath.join(self._folderPath, "Addr", zip),
        )
        self._downloader.start()


# End of manager.py
