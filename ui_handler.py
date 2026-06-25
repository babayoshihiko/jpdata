# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import QCoreApplication, Qt
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView
from qgis.PyQt.QtGui import QDesktopServices
from . import jpDataUtils
from .i18n import TR
from .jpdata_lni import jpDataLNI
from .jpdata_mhlw import jpDataMHLW

class JPDataUIHandler:
    def __init__(self, dockwidget, lang):
        self._dw = dockwidget
        self._lang = lang
        self._connect_signals()
        self._setup_ui_static_text()
        self._LNI = jpDataLNI.instance()     # Singleton. See manager.py
        self._GSI = jpDataUtils.getTilesFromCsv()
        self._MHLW = jpDataMHLW.instance()   # Singleton. See manager.py


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
        self._dw.myComboBox11.currentIndexChanged.connect(self._CB11_changed)
        self._dw.myPushButton15.clicked.connect(self._lni_web)


        # Tab MHLW
        self._dw.myLW_MHLW.currentRowChanged.connect(self._mhlw_map_changed)
        self._dw.myPB_MHLW_1.clicked.connect(self._mhlw_web)


    def _setup_ui_static_text(self):
        # Global / Folder Settings
        self._dw.myPushButton2.setText(TR.CHOOSE_FOLDER())
        self._dw.myPushButton2.setToolTip(TR.CHOOSE_FOLDER())
        self._dw.myLabelStatus.setText("")

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

    def _setup_tab_setting(self, i):
        self._dw.myTabWidget.setTabText(i, TR.SETTING())
        self._dw.myCheckBox1.setText(TR.SETTING_BACKGROUND())
        self._dw.myCheckBox2.setText(TR.SETTING_GEOMETRY())

    def init_tabs(self, folder_path, LNI=None, MHLW=None):
        self._init_tab3()
        self._init_tab_addr(folder_path)

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
        jpDataUtils.set_pref_items(self._dw.myListWidget31)

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

    def _init_tab_addr(self, folder_path):
        jpDataUtils.set_pref_items(self._dw.myCB_Addr_1)
        if os.path.exists(
            os.path.join(folder_path, "Addr")
        ):  # If the folder exists, set cities
            self._dw.myPB_Addr_1.setText(TR.JUMP())
        else:
            self._dw.myPB_Addr_1.setText(TR.DOWNLOAD())

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


    def _populate_years_CB(self, years, combBox):
        current_year = combBox.currentText()
        combBox.clear()
        for year in years:
            if year:
                combBox.addItem(year)
        # Restore selection if it still exists
        index = combBox.findText(current_year)
        if index != -1:
            combBox.setCurrentIndex(index)
        else:
            combBox.setCurrentIndex(0)

    def _tab_changed(self, index):
        """Called whenever the current tab changes."""
        if index == 0:
            self._init_tab1()
        elif index == 3:
            self._init_tab_mhlw()
        elif index == 4:  # tab #3 (4th tab)
            self._dw.myCB_Addr_1.setCurrentIndex(12)





    def _LW11_itemSelectionChanged(self):
        if len(self._dw.myListWidget11.selectedItems()) == 0:
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()

        thisLandNum = self._LNI.get_records()[name_map]
        self._LNI.set_name(name_map)

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
            if self._LNI.get_prev_name() == "" or self._LNI.get_records()[self._LNI.get_prev_name()].get(
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
            str_new_LW12_text = self._LNI.get_prefs(name_map)
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

    def _LW12_itemSelectionChanged(self):
        if (
            len(self._dw.myListWidget11.selectedItems()) == 0
            or len(self._dw.myListWidget12.selectedItems()) == 0
        ):
            return
        name_map = self._dw.myListWidget11.selectedItems()[0].text()
        name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        self._tab1_check_year(name_map)
        thisLandNum = self._LNI.get_records()[name_map]
        if thisLandNum["type_muni"].lower() in ("detail", "mesh1"):
            self._tab1_set_LW13(name_pref)

    def _tab1_check_year(self, name_map):
        years = []
        name_pref = None
        record = self._LNI.get_records()[name_map]
        if len(self._dw.myListWidget12.selectedItems()) > 0:
            if record["type_muni"].lower() != "mesh1":
                name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        years = self._LNI.get_years(name_map, name_pref)
        self._populate_years_CB(years, self._dw.myComboBox11)
        self._tab1_set_LW13()

    def _CB11_changed(self, index):
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

        thisLandNum = self._LNI.get_records()[str_name_j]
        if thisLandNum["type_muni"].lower() not in ("detail", "mesh1"):
            return

        self._dw.myListWidget13.clear()
        self._dw.myListWidget13.show()

        if thisLandNum["type_muni"].lower() == "detail":
            details = self._LNI.get_details(
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


    def _lni_web(self):
        items = self._dw.myListWidget11.selectedItems()
        if items:
            thisLandNum = self._LNI.get_records()[items[0].text()]
            QDesktopServices.openUrl(QUrl(thisLandNum["source"]))




    def _mhlw_map_changed(self, row):
        item = self._dw.myLW_MHLW.item(row)
        if item is None:
            return
        service_name = item.text()
        years = self._MHLW.get_years(service_name)
        self._populate_years_CB(years, self._dw.myCB_MHLW)

    def _mhlw_web(self):
        items = self._dw.myLW_MHLW.selectedItems()
        if items:
            thisLandNum = self._MHLW.get_records()[items[0].text()]
            QDesktopServices.openUrl(QUrl(thisLandNum["source"]))
        
