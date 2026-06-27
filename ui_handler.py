# -*- coding: utf-8 -*-
import os
from qgis.core import (
    QgsPointXY,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication, Qt
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView, QLineEdit
from qgis.PyQt.QtGui import QDesktopServices
# from . import jpDataAddr
from . import jpDataMesh
# from . import jpDataMuni
from . import jpDataUtils
from .i18n import TR
from .jpdata_lni import jpDataLNI
from .jpdata_census import jpDataCensus
from .jpdata_mhlw import jpDataMHLW
from .jpdata_muni import jpDataMuni


class JPDataUIHandler:
    _verbose = True

    def __init__(self, iface, dockwidget, lang):
        self._iface = iface
        self._dw = dockwidget
        self._lang = lang
        self._connect_signals()
        self._setup_ui_static_text()
        self._Muni = jpDataMuni.instance()
        self._LNI = jpDataLNI.instance()           # Singleton. See manager.py
        self._Census = jpDataCensus.instance()     # Singleton. See manager.py
        self._MHLW = jpDataMHLW.instance()         # Singleton. See manager.py


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
        self._dw.myTabWidget.currentChanged.connect(self._tab_changed)

        # Tab LNI
        self._dw.myListWidget11.itemSelectionChanged.connect(self._LW11_itemSelectionChanged)
        self._dw.myListWidget12.itemSelectionChanged.connect(self._LW12_itemSelectionChanged)
        # self._dw.myComboBox11.currentIndexChanged.connect(self._CB11_changed)
        self._dw.myPushButton15.clicked.connect(self._lni_web)

        # Tab Census
        self._dw.myListWidget31.currentItemChanged.connect(self._LW31_currentItemChanged)
        self._dw.myListWidget32.itemSelectionChanged.connect(self._LW32_itemSelectionChanged)
        self._dw.myComboBox32.currentIndexChanged.connect(self._LW32_itemSelectionChanged)

        # Tab MHLW
        self._dw.myLW_MHLW.currentRowChanged.connect(self._mhlw_map_changed)
        self._dw.myPB_MHLW_1.clicked.connect(self._mhlw_web)

        # Tab Addr
        self._dw.myCB_Addr_1.currentIndexChanged.connect(self._myCB_Addr_1_changed)
        #self._dw.myCB_Addr_2.currentIndexChanged.connect(
        #    lambda: jpDataAddr.set_cb_towns(
        #        self._dw.myCB_Addr_3,
        #        self._folderPath,
        #        self._dw.myCB_Addr_1.currentText(),
        #        self._dw.myCB_Addr_2.currentText(),
        #    )
        #)
        #self._dw.myCB_Addr_3.currentIndexChanged.connect(
        #    lambda: jpDataAddr.set_cb_details(
        #        self._dw.myCB_Addr_4,
        #        self._folderPath,
        #        self._dw.myCB_Addr_1.currentText(),
        #        self._dw.myCB_Addr_2.currentText(),
        #        self._dw.myCB_Addr_3.currentText(),
        #    )
        #)
        # self._dw.myPB_Addr_1.clicked.connect(self._myPB_Addr_1_clicked)
        self._dw.myPB_Addr_2.clicked.connect(self._myPB_Addr_2_clicked)
        self._dw.myPB_Addr_3.clicked.connect(self._myPB_Addr_3_clicked)



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


    def _setup_tab1(self, i):
        self._dw.myTabWidget.setTabText(i, TR.LANDNUMINFO())
        self._dw.myPushButton11.setText(TR.DOWNLOAD())
        self._dw.myPushButton11.setToolTip(TR.DOWNLOAD_LNI())
        self._dw.myPushButton14.setText(TR.ADD_TO_MAP())
        self._dw.myPushButton14.setToolTip(TR.ADD_TO_MAP_TOOLTIP())
        self._dw.myPushButton15.setText(TR.WEB())
        self._dw.myPushButton15.setToolTip(TR.WEB_TOOLTIP())

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
        self._dw.myTabWidget.setTabText(i, TR.GSI_TILES())
        self._dw.myPushButton25.setText(TR.ADD_TO_MAP())
        self._dw.myPushButton25.setToolTip(TR.GSI_TILES_TOOLTIP())
    
    def _setup_tab3(self, i):
        self._dw.myTabWidget.setTabText(i, TR.CENSUS())
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
        self._populate_LW("allprefs", self._dw.myListWidget31)
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
        self._dw.myTabWidget.setTabText(i, TR.MHLW())
        self._dw.myPB_MHLW_1.setText(TR.WEB())
        self._dw.myPB_MHLW_2.setText(TR.DOWNLOAD())
        self._dw.myPB_MHLW_3.setText(TR.ADD_TO_MAP())
        # Selection Modes
        self._dw.myLW_MHLW.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )

    def _setup_tab_addr(self, i):
        self._dw.myTabWidget.setTabText(i, TR.ADDRESS())
        self._dw.myPB_Addr_1.setText(TR.DOWNLOAD())
        self._dw.myPB_Addr_2.setText(TR.JUMP())
        self._dw.myPB_Addr_3.setText(TR.REPROJECT())

    def _setup_tab_setting(self, i):
        self._dw.myTabWidget.setTabText(i, TR.SETTING())
        self._dw.myCheckBox1.setText(TR.SETTING_BACKGROUND())
        self._dw.myCheckBox2.setText(TR.SETTING_GEOMETRY())

    def init_tabs(self, folder_path, LNI=None, MHLW=None):
        self._init_tab3()
        self._init_tab_addr()

    def _init_tab1(self, LNI=None):
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

    def _init_tab3(self):
        # jpDataUtils.set_pref_items(self._dw.myListWidget31)
        index = self._dw.myComboBox32.currentIndex()
        self._populate_CB(self._Census.get_years(index), self._dw.myComboBox31)

    def _init_tab_mhlw(self, MHLW=None):
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

    def _init_tab_addr(self):
        jpDataUtils.set_pref_items(self._dw.myCB_Addr_1, self._lang)
        projs = self._Muni.get_projections()
        for proj in projs:
            self._dw.myCB_Addr_Projection.addItem(proj)

    def enable_download(self, enable=True):
        if enable:
            self._dw.myPushButton11.setText(TR.DOWNLOAD())
            self._dw.myPushButton31.setText(TR.DOWNLOAD())
            self._dw.myPB_MHLW_2.setText(TR.DOWNLOAD())
            self._dw.myPushButton14.setEnabled(True)
            self._dw.myPushButton32.setEnabled(True)
            self._dw.myPB_MHLW_2.setEnabled(True)
        else:
            self._dw.myPushButton11.setText(TR.CANCEL())
            self._dw.myPushButton31.setText(TR.CANCEL())
            self._dw.myPB_MHLW_2.setText(TR.CANCEL())
            self._dw.myPushButton14.setEnabled(False)
            self._dw.myPushButton32.setEnabled(False)
            self._dw.myPB_MHLW_2.setEnabled(False)

    #
    #  Common UI handlers
    #
    def _populate_CB(self, texts, combo_widget):
        current_text = combo_widget.currentText()
        combo_widget.blockSignals(True)
        combo_widget.clear()
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

    def _populate_LW(self, texts, list_widget):
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
            self._init_tab1()
        elif index == 3:
            self._init_tab_mhlw()
        elif index == 4:  # tab #3 (4th tab)
            self._dw.myCB_Addr_1.setCurrentIndex(12)





    def _LW11_itemSelectionChanged(self):
        jpDataUtils.printLog("_LW11_itemSelectionChanged")
        if len(self._dw.myListWidget11.selectedItems()) == 0:
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()
        thisLandNum = self._LNI.get_record(name_map)
        self._dw.myLabelStatus.setText(thisLandNum.get("code_map", ""))
        str_new_LW12_text = []
        bol_redraw_LW12 = True
        bol_show_LW13 = False
        muni_type = thisLandNum.get("type_muni", "").lower()

        def all_prefs():
            return [jpDataUtils.getPrefNameByCode(code, self._lang) for code in range(1, 48)]

        if muni_type in ("", "allprefs"):
            jpDataUtils.printLog("allprefs")
            if self._LNI.get_prev_name() == "" or self._LNI.get_record(self._LNI.get_prev_name()).get("type_muni", "").lower() not in ("", "allprefs", "mesh1"):
                str_new_LW12_text = all_prefs()
            else:
                bol_redraw_LW12 = False
                self._dw.myListWidget13.hide()
        elif muni_type == "single":
            jpDataUtils.printLog("single")
            str_new_LW12_text = [TR.NATIONWIDE()]
        elif muni_type in ("regional", "detail"):
            jpDataUtils.printLog("regional or detail")
            if muni_type == "detail":
                bol_show_LW13 = True
            str_new_LW12_text = self._LNI.get_prefs(name_map)
        elif muni_type == "mesh1":
            jpDataUtils.printLog("mesh1")
            bol_show_LW13 = True
            str_new_LW12_text = all_prefs()

        if bol_redraw_LW12:
            self._tab1_clear(bol_show_LW13)
            self._populate_LW(str_new_LW12_text, self._dw.myListWidget12)

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
        name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        self._tab1_populate_years(name_map)
        thisLandNum = self._LNI.get_record(name_map)
        if thisLandNum["type_muni"].lower() in ("detail", "mesh1"):
            self._tab1_set_LW13(name_map, name_pref)

    def _tab1_populate_years(self, name_map):
        years = []
        name_pref = None
        if len(self._dw.myListWidget12.selectedItems()) > 0:
            name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        years = self._LNI.get_years(name_map, name_pref)
        self._populate_CB(years, self._dw.myComboBox11)

    def _tab1_set_LW13(self, name_map, name_pref):
        year = self._dw.myComboBox11.currentText()
        if not year.strip():
            return
        thisLandNum = self._LNI.get_records()[name_map]
        if thisLandNum["type_muni"].lower() not in ("detail", "mesh1"):
            self._dw.myListWidget13.hide()
            return
        self._dw.myListWidget13.show()
        if thisLandNum["type_muni"].lower() == "detail":
            details = self._LNI.get_details(
                name_map, name_pref, year
            )
        else:
            details = jpDataMesh.getMesh1ByPrefName(name_pref)

        self._populate_LW(details, self._dw.myListWidget13)

    # def _CB11_changed(self, index):
    #     self._tab1_set_LW13()

    def _lni_web(self):
        items = self._dw.myListWidget11.selectedItems()
        if items:
            thisLandNum = self._LNI.get_records()[items[0].text()]
            QDesktopServices.openUrl(QUrl(thisLandNum["source"]))






    def _LW31_currentItemChanged(self, current, previous):
        if not current or current == previous or isinstance(current, int):
            return

        name_pref = current.text()
        year = self._dw.myComboBox31.currentText()

        designated_cities = jpDataMuni.get_all_designated_cities(year, self._lang)

        rows = jpDataMuni.getMuniFromPrefName(name_pref, self._lang)
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
        self._populate_CB(years, self._dw.myComboBox31)
        self._dw.myListWidget33.clear()
        self._dw.myListWidget33.show()

        details = []
        if len(self._dw.myListWidget32.selectedItems()) == 0:
            details = jpDataMesh.getMesh1ByPrefName(name_pref)
        else:
            name_munis = []
            for name_muni in self._dw.myListWidget32.selectedItems():
                name_munis.append(name_muni.text())
            details = jpDataMesh.getMesh1ByPrefMuniName(name_pref, name_munis, self._lang)
        self._populate_LW(details, self._dw.myListWidget33)






    def _mhlw_map_changed(self, row):
        item = self._dw.myLW_MHLW.item(row)
        if item is None:
            return
        name_map = item.text()
        years = self._MHLW.get_years(name_map)
        self._populate_CB(years, self._dw.myCB_MHLW)

    def _mhlw_web(self):
        items = self._dw.myLW_MHLW.selectedItems()
        if items:
            thisLandNum = self._MHLW.get_records()[items[0].text()]
            QDesktopServices.openUrl(QUrl(thisLandNum["source"]))
        




    def _myPB_Addr_2_clicked(self):
        lon, lat = self._Muni.get_lonlat_by_addr(
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

    def _myPB_Addr_3_clicked(self):
        lon, lat = self._Muni.get_lonlat_by_addr(
            str(self._dw.myCB_Addr_1.currentText()),
            str(self._dw.myCB_Addr_2.currentText()),
            str(self._dw.myCB_Addr_3.currentText()),
            str(self._dw.myCB_Addr_4.currentText()),
        )
        from qgis.core import QgsCoordinateReferenceSystem, QgsProject
        proj_index = self._dw.myCB_Addr_Projection.currentIndex()
        proj_string = self._Muni.get_proj_string(proj_index, lat, lon)
        crs = QgsCoordinateReferenceSystem.fromProj(proj_string)
        if crs.isValid():
            QgsProject.instance().setCrs(crs)


    def _myCB_Addr_1_changed(self):
        jpDataUtils.printDebugLog(self._dw.myCB_Addr_1.currentText())
        cities = self._Muni.get_munis(self._dw.myCB_Addr_1.currentText())
        jpDataUtils.printDebugLog(cities)
        self._populate_CB(cities, self._dw.myCB_Addr_2)


