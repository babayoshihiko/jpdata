# -*- coding: utf-8 -*-
import os
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsField,
    QgsMarkerSymbol,
    QgsSvgMarkerSymbolLayer,
    QgsUnitTypes,
    QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling,
    QgsTextFormat,
)
from qgis.PyQt.QtCore import (
    Qt, 
    QVariant, 
    QUrl, 
    QMetaType, 
    QPointF
)
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView, QLineEdit
from qgis.PyQt.QtGui import QDesktopServices, QFont, QColor
from qgis.PyQt.QtWidgets import QLabel, QTreeWidgetItem
from . import jpDataMesh
from . import jpDataUtils
from .i18n import TR
from .jpdata_lni import jpDataLNI
from .jpdata_census import jpDataCensus
from .jpdata_mhlw import jpDataMHLW
from .jpdata_muni import jpDataMuni
from .ui_handler_addr import JPDataUIHandlerAddr



class JPDataUIHandler:
    _verbose = True

    def __init__(self, iface, dockwidget, lang):
        self._iface = iface
        self._dw = dockwidget
        self._lang = lang
        self.TABS = {
            0: TR.LANDNUMINFO(),
            1: TR.GSI_TILES(),
            2: TR.CENSUS(),
            3: TR.MHLW(),
            4: TR.ADDRESS(),
            5: TR.SETTING()
        }
        self.meshLabel = QLabel("Japanese Mesh Code")
        self._iface.statusBarIface().addPermanentWidget(self.meshLabel)
        self.meshLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._connect_signals()
        self._Muni = jpDataMuni.instance()
        self._LNI = jpDataLNI.instance()           # Singleton. See manager.py
        self._Census = jpDataCensus.instance()     # Singleton. See manager.py
        self._MHLW = jpDataMHLW.instance()         # Singleton. See manager.py
        self._setup_ui_static_text()
        self._ui_addr = None


    def _create_pin_layer(self):
        # Memory Layer For Address Search
        layers = QgsProject.instance().mapLayersByName("Address Pin")

        if layers:
            self._pin_layer = layers[0]
        else:
            self._pin_layer = QgsVectorLayer(
                f"Point?crs={QgsProject.instance().crs().authid()}",
                "Address Pin",
                "memory"
            )
            pr = self._pin_layer.dataProvider()
            pr.addAttributes([
                QgsField("name", QMetaType.Type.QString),
                QgsField("pref", QMetaType.Type.QString),
                QgsField("muni", QMetaType.Type.QString),
            ])
            self._pin_layer.updateFields()
            svg_path = None
            for p in QgsApplication.svgPaths():
                candidate = os.path.join(p, "symbol", "blue-marker.svg")
                if os.path.exists(candidate):
                    svg_path = candidate
                    break
            if svg_path:
                symbol = QgsMarkerSymbol.createSimple({})
                svg_layer = QgsSvgMarkerSymbolLayer(svg_path)
                svg_layer.setSize(128)  # 32 px
                svg_layer.setSizeUnit(QgsUnitTypes.RenderPixels)
                svg_layer.setOffset(QPointF(0, -64))
                svg_layer.setOffsetUnit(QgsUnitTypes.RenderPixels)
                symbol.changeSymbolLayer(0, svg_layer)
                self._pin_layer.renderer().setSymbol(symbol)
            QgsProject.instance().addMapLayer(self._pin_layer)

    def unload(self):
        try:
            self._iface.mapCanvas().xyCoordinates.disconnect(
                self._updateMeshCode
            )
        except TypeError:
            pass

        meshLabel = getattr(self, "meshLabel", None)
        if meshLabel is not None:
            self._iface.statusBarIface().removeWidget(meshLabel)
            meshLabel.deleteLater()
            self.meshLabel = None

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
        

    def _connect_signals(self):
        self._iface.mapCanvas().xyCoordinates.connect(self._updateMeshCode)
        self._dw.myTabWidget.currentChanged.connect(self._tab_changed)

        # Tab LNI
        self._dw.myListWidget11.itemSelectionChanged.connect(self._LW11_itemSelectionChanged)
        self._dw.myListWidget12.itemSelectionChanged.connect(self._LW12_itemSelectionChanged)
        self._dw.myPushButton15.clicked.connect(self._lni_web)
        self._dw.myPB_LNI_Wiki.clicked.connect(self._lni_wiki)

        # Tab Census
        self._dw.myListWidget31.currentItemChanged.connect(self._LW31_currentItemChanged)
        self._dw.myListWidget32.itemSelectionChanged.connect(self._LW32_itemSelectionChanged)
        self._dw.myComboBox32.currentIndexChanged.connect(self._LW32_itemSelectionChanged)

        # Tab MHLW
        self._dw.myLW_MHLW.currentRowChanged.connect(self._mhlw_map_changed)
        self._dw.myPB_MHLW_1.clicked.connect(self._mhlw_web)
        self._dw.myPB_MHLW_Wiki.clicked.connect(self._mhlw_wiki)



    def _setup_ui_static_text(self):
        self._dw.myPushButton2.setText(TR.CHOOSE_FOLDER())
        self._dw.myPushButton2.setToolTip(TR.CHOOSE_FOLDER())
        self._dw.myLabelStatus.setText("")
        self._dw.myLineEditSetting3.setEchoMode(
            QLineEdit.EchoMode.Password
            if hasattr(QLineEdit, "EchoMode")
            else QLineEdit.Password
        )
        self._setup_tab1(0)
        self._setup_tab2(1)
        self._setup_tab3(2)
        self._set_tab_mhlw(3)
        self._setup_tab_addr(4)
        self._setup_tab_setting(5)
        for index, name in self.TABS.items():
            self._dw.myTabWidget.setTabText(index, name)


    def _setup_tab1(self, i):
        self._dw.myPushButton11.setText(TR.DOWNLOAD())
        self._dw.myPushButton11.setToolTip(TR.DOWNLOAD_LNI())
        self._dw.myPushButton14.setText(TR.ADD_TO_MAP())
        self._dw.myPushButton14.setToolTip(TR.ADD_TO_MAP_TOOLTIP())
        self._dw.myPushButton15.setText(TR.WEB())
        self._dw.myPushButton15.setToolTip(TR.WEB_TOOLTIP())
        self._dw.myPB_LNI_Wiki.setText("Wiki")

        # Selection Modes
        self._dw.myListWidget12.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )
        self._dw.myListWidget13.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )
        self._dw.myListWidget13.hide()

    def _setup_tab2(self, i):
        self._dw.myPushButton25.setText(TR.ADD_TO_MAP())
        self._dw.myPushButton25.setToolTip(TR.GSI_TILES_TOOLTIP())
    
    def _setup_tab3(self, i):
        self._dw.myLabel31.setText(TR.YEAR())
        self._dw.myPushButton31.setText(TR.DOWNLOAD())
        self._dw.myPushButton32.setText(TR.ADD_TO_MAP())
        self._dw.myComboBox31.setToolTip(TR.CENSUS_YEAR_TOOLTIP())
        self._dw.myComboBox32.addItem(TR.NEIGHBOURHOOD())
        self._dw.myComboBox32.addItem(TR.X3_MESH())
        self._dw.myComboBox32.addItem(TR.X4_MESH())
        self._dw.myComboBox32.addItem(TR.X5_MESH())
        self._dw.myComboBox32.addItem(TR.X6_MESH())
        self._dw.myComboBox32.setToolTip(TR.CENSUS_TYPE_TOOLTIP())
        self.populate_LW("allprefs", self._dw.myListWidget31)
        self._dw.myPushButton31.setText(TR.DOWNLOAD())
        self._dw.myPushButton31.setToolTip(TR.DOWNLOAD_CENSUS())
        self._dw.myPushButton32.setText(TR.ADD_TO_MAP())
        self._dw.myPushButton32.setToolTip(TR.ADD_TO_MAP_TOOLTIP())
        self._dw.myListWidget32.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )

        self._dw.myListWidget33.hide()
        self._dw.myListWidget33.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )

    def _set_tab_mhlw(self, i):
        self._dw.myPB_MHLW_1.setText(TR.WEB())
        self._dw.myPB_MHLW_2.setText(TR.DOWNLOAD())
        self._dw.myPB_MHLW_3.setText(TR.ADD_TO_MAP())
        # Selection Modes
        self._dw.myLW_MHLW.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )
        self._dw.myPB_MHLW_Wiki.setText("Wiki")

    def _setup_tab_addr(self, i):
        self._dw.myPB_Addr_1.setText(TR.DOWNLOAD())
        self._dw.myPB_Addr_2.setText(TR.JUMP())
        self._dw.myPB_Addr_3.setText(TR.REPROJECT())
        self._dw.myPB_Addr_4.setText(TR.ADD_GRATICULES())

    def _setup_tab_setting(self, i):
        self._dw.myPushButton2.clicked.connect(self.chooseFolder)
        # For local testing purpose
        if self._verbose:
            self._dw.myPushButtonTest.clicked.connect(self._test_verbose)
        else:
            self._dw.myPushButtonTest.hide()
        self._dw.myCheckBox1.setText(TR.SETTING_BACKGROUND())
        self._dw.myCheckBox2.setText(TR.SETTING_GEOMETRY())
        self._dw.myCheckBox2.setChecked(True)

        tree = self._dw.myTreeWidget
        tree.setHeaderHidden(True)
        for index, name in self.TABS.items():
            if name != TR.SETTING():
                item = QTreeWidgetItem(tree)
                item.setText(0, name)
                item.setData(0, Qt.UserRole, index)
                item.setCheckState(0, Qt.Checked)
        tree.expandAll()

    def _test_verbose(self):
        self._dw.myTabWidget.setTabVisible(0, False)
        # pass
        # This is a method for local testing purpose.

    def chooseFolder(self):
        from qgis.PyQt.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(
            self._iface.mainWindow(), TR.CHOOSE_FOLDER(), self._folderPath
        )
        if folder:
            self._folderPath = folder
            QSettings().setValue("jpdata/FolderPath", folder)
            self._set_download_fullpath(folder)
            self._dw.myLabel1.setText(folder)

    def _lni_populate_init_values(self):
        self._LNI.init()
        self._dw.myListWidget11.clear()
        bg = (
            Qt.GlobalColor.darkGray
            if hasattr(Qt, "GlobalColor")
            else Qt.darkGray
        )
        fg = (
            Qt.GlobalColor.white if hasattr(Qt, "GlobalColor") else Qt.white
        )
        gray = (
            Qt.GlobalColor.gray if hasattr(Qt, "GlobalColor") else Qt.gray
        )
        for key, record in self._LNI.get_records().items():
            item = QListWidgetItem(key)

            if record["availability"] != "yes":
                # Disable selection
                if hasattr(Qt, "ItemFlag"):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

                if record["availability"] == "heading":
                    item.setBackground(bg)
                    item.setForeground(fg)
                else:
                    item.setForeground(gray)

            self._dw.myListWidget11.addItem(item)

    def _census_populate_init_values(self):
        # jpDataUtils.set_pref_items(self._dw.myListWidget31)
        index = self._dw.myComboBox32.currentIndex()
        self.populate_CB(self._Census.get_years(index), self._dw.myComboBox31)

    def _mhlw_populate_init_values(self, MHLW=None):
        self._MHLW.init()
        self._dw.myLW_MHLW.clear()
        bg = (
            Qt.GlobalColor.darkGray
            if hasattr(Qt, "GlobalColor")
            else Qt.darkGray
        )
        fg = (
            Qt.GlobalColor.white if hasattr(Qt, "GlobalColor") else Qt.white
        )
        for key, record in self._MHLW.get_records().items():
            item = QListWidgetItem(key)
 
            if record["code_map"] != "heading":
                # item.setBackground(fg)
                # item.setForeground(bg)
                pass
            else:
                item.setBackground(bg)
                item.setForeground(fg)
                # Disable selection
                if hasattr(Qt, "ItemFlag"):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self._dw.myLW_MHLW.addItem(item)


    def enable_download(self, enable=True):
        if enable:
            self._dw.myPushButton11.setText(TR.DOWNLOAD())
            self._dw.myPushButton31.setText(TR.DOWNLOAD())
            self._dw.myPB_MHLW_2.setText(TR.DOWNLOAD())
            self._dw.myPushButton14.setEnabled(True)
            self._dw.myPushButton32.setEnabled(True)
            self._dw.myPB_Addr_1.setEnabled(True)
            self._dw.myPB_MHLW_2.setEnabled(True)
        else:
            self._dw.myPushButton11.setText(TR.CANCEL())
            self._dw.myPushButton31.setText(TR.CANCEL())
            self._dw.myPB_MHLW_2.setText(TR.CANCEL())
            self._dw.myPushButton14.setEnabled(False)
            self._dw.myPushButton32.setEnabled(False)
            self._dw.myPB_Addr_1.setEnabled(False)
            self._dw.myPB_MHLW_2.setEnabled(False)

    #
    #  Common UI handlers
    #
    def populate_CB(self, texts, combo_widget, add_empty_item=False):
        if texts == "allprefs":
            texts = [jpDataUtils.getPrefNameByCode(i, lang = self._lang) for i in range(1, 48)]
        current_text = combo_widget.currentText()
        combo_widget.blockSignals(True)
        combo_widget.clear()
        if texts is not None:
            if add_empty_item:
                texts.insert(0, "---")
            for text in texts:
                if text:
                    combo_widget.addItem(text)
        # Restore selection if it still exists
        index = combo_widget.findText(current_text)
        if index != -1:
            combo_widget.setCurrentIndex(index)
        else:
            combo_widget.setCurrentIndex(0)
        combo_widget.blockSignals(False)

    def populate_LW(self, texts, list_widget):
        if texts == "allprefs":
            texts = [jpDataUtils.getPrefNameByCode(i, lang = self._lang) for i in range(1, 48)]
        current_selected = [
            item.text() for item in list_widget.selectedItems()
        ]
        current_text = ""
        if list_widget.currentItem():
            current_text = list_widget.currentItem().text()
        if len(texts) == 1:
            current_text = texts[0]
            current_selected = texts

        list_widget.blockSignals(True)
        list_widget.clear()
        for text in texts:
            item = QListWidgetItem(text)
            list_widget.addItem(item)
            if text in current_selected:
                item.setSelected(True)
            if current_text != "" and text == current_text:
                list_widget.setCurrentItem(item)
        list_widget.blockSignals(False)

    def _tab_changed(self, index):
        """Called whenever the current tab changes."""
        if index == 0:
            self._lni_populate_init_values()
        elif index == 2:
            self._census_populate_init_values()
        elif index == 3:
            self._mhlw_populate_init_values()
        elif index == 4:  # addr
            if self._ui_addr is None:
                self._ui_addr = JPDataUIHandlerAddr(self._iface, self._dw, self, self._lang)





    def _LW11_itemSelectionChanged(self):
        if len(self._dw.myListWidget11.selectedItems()) == 0:
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()
        self._LNI.set_record(name_map)
        thisLandNum = self._LNI.get_record()
        self._dw.myLabelStatus.setText(thisLandNum.get("code_map", ""))
        str_new_LW12_text = []
        bol_redraw_LW12 = True
        bol_show_LW13 = False
        muni_type = thisLandNum.get("type_muni", "").lower()

        def all_prefs():
            return [jpDataUtils.getPrefNameByCode(code, self._lang) for code in range(1, 48)]

        prev_muni_type = "DUMMY"
        if self._LNI.get_prev_name() != "":
            prev_muni_type = self._LNI.get_records()[self._LNI.get_prev_name()].get("type_muni", "").lower() 
        if muni_type in ("", "allprefs"):
            if prev_muni_type in ("", "allprefs", "mesh1"):
                bol_redraw_LW12 = False
                self._dw.myListWidget13.hide()
            else:
                str_new_LW12_text = all_prefs()
        elif muni_type == "single":
            str_new_LW12_text = [TR.NATIONWIDE()]
        elif muni_type in ("regional", "detail"):
            if muni_type == "detail":
                bol_show_LW13 = True
                self._dw.myListWidget13.clear()
            str_new_LW12_text = self._LNI.get_prefs(name_map)
        elif muni_type == "mesh1":
            bol_show_LW13 = True
            if prev_muni_type in ("", "allprefs", "mesh1"):
                bol_redraw_LW12 = False
            else:
                str_new_LW12_text = all_prefs()
                self._dw.myListWidget13.clear()

        if bol_redraw_LW12:
            self._tab1_clear(bol_show_LW13)
            self.populate_LW(str_new_LW12_text, self._dw.myListWidget12)

        self._tab1_populate_years(name_map)

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

    def _LW12_itemSelectionChanged(self):
        if (
            len(self._dw.myListWidget11.selectedItems()) == 0
            or len(self._dw.myListWidget12.selectedItems()) == 0
        ):
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()
        year = self._dw.myComboBox11.currentText()
        name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        self._tab1_populate_years(name_map)
        self._LNI.set_record(name_map, year, name_pref)
        thisLandNum = self._LNI.get_record()
        if thisLandNum["type_muni"].lower() in ("detail", "mesh1"):
            self._LNI_is_Mesh = (thisLandNum["type_muni"].lower() == "mesh1")
            self._tab1_set_LW13(name_map, name_pref)

    def _tab1_populate_years(self, name_map):
        years = []
        name_pref = None
        if len(self._dw.myListWidget12.selectedItems()) > 0:
            name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        years = self._LNI.get_years(name_map, name_pref)
        self.populate_CB(years, self._dw.myComboBox11)

    def _tab1_set_LW13(self, name_map, name_pref):
        year = self._dw.myComboBox11.currentText()
        if not year.strip():
            return
        self._LNI.set_record(name_map, year, name_pref)
        thisLandNum = self._LNI.get_record()
        if thisLandNum["type_muni"].lower() not in ("detail", "mesh1"):
            self._dw.myListWidget13.hide()
            return
        self._dw.myListWidget13.show()
        if thisLandNum["type_muni"].lower() == "detail":
            details = self._LNI.get_details(name_map, year, name_pref)
        else:
            details = jpDataMesh.getMesh1ByPrefName(name_pref)
        self.populate_LW(details, self._dw.myListWidget13)
        if (
            not self._dw.myListWidget13.selectedItems()
            and thisLandNum["type_muni"].lower() == "mesh1"
        ):
            point = self._iface.mapCanvas().center()
            code = self._updateMeshCode(point)
            lw = self._dw.myListWidget13
            for i in range(lw.count()):
                item = lw.item(i)
                if item.text() == code:
                    item.setSelected(True)
                    lw.setCurrentItem(item)
                    break

    def _lni_web(self):
        items = self._dw.myListWidget11.selectedItems()
        if items:
            self._LNI.set_record(items[0].text())
            item = self._LNI.get_record()
            if item != "":
                QDesktopServices.openUrl(QUrl(item["source"]))

    def _lni_wiki(self):
        items = self._dw.myListWidget11.selectedItems()
        if items:
            name_map = items[0].text()
            web_wiki = "https://github.com/babayoshihiko/jpdata/wiki/" + name_map
            QDesktopServices.openUrl(QUrl(web_wiki))

    def _mhlw_web(self):
        items = self._dw.myLW_MHLW.selectedItems()
        if items:
            item = self._MHLW.get_record(items[0].text())
            if item["source"] != "":
                QDesktopServices.openUrl(QUrl(item["source"]))

    def _mhlw_wiki(self):
        items = self._dw.myLW_MHLW.selectedItems()
        if items:
            name_map = items[0].text()
            web_wiki = "https://github.com/babayoshihiko/jpdata/wiki/" + name_map
            QDesktopServices.openUrl(QUrl(web_wiki))

    def _LW31_currentItemChanged(self, current, previous):
        if not current or current == previous or isinstance(current, int):
            return

        name_pref = current.text()
        year = self._dw.myComboBox31.currentText()

        designated_cities = self._Muni.get_all_designated_cities(year)

        rows = self._Muni.get_munis(name_pref) # (name_pref, self._lang)
        self._dw.myListWidget32.clear()

        for name in rows:
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
            return
        years = self._Census.get_years(self._dw.myComboBox32.currentIndex())
        self.populate_CB(years, self._dw.myComboBox31)
        self._dw.myListWidget33.show()
        details = []
        if len(self._dw.myListWidget32.selectedItems()) == 0:
            details = jpDataMesh.getMesh1ByPrefName(name_pref)
        else:
            name_munis = []
            for name_muni in self._dw.myListWidget32.selectedItems():
                name_munis.append(name_muni.text())
            details = jpDataMesh.getMesh1ByPrefMuniName(name_pref, name_munis, self._lang)
        self.populate_LW(details, self._dw.myListWidget33)






    def _mhlw_map_changed(self, row):
        item = self._dw.myLW_MHLW.item(row)
        if item is None:
            return
        name_map = item.text()
        years = self._MHLW.get_years(name_map)
        self.populate_CB(years, self._dw.myCB_MHLW)



    def _mesh1code(self, lat, lon):
        p = int(lat * 60 / 40)
        a = int(lon) - 100
        return f"{p:02d}{a:02d}"

    def _updateMeshCode(self, point):
        if not hasattr(self, "meshLabel") or self.meshLabel is None:
            return
        canvas = self._iface.mapCanvas()
        src_crs = canvas.mapSettings().destinationCrs()
        dst_crs = QgsCoordinateReferenceSystem("EPSG:4612")
        if src_crs != dst_crs:
            tr = QgsCoordinateTransform(
                src_crs,
                dst_crs,
                QgsProject.instance()
            )
            pt = tr.transform(point)
        else:
            pt = point
        code = self._mesh1code(pt.y(), pt.x())
        self.meshLabel.setText(f"mesh: {code}")
        return code