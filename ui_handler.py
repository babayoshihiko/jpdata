# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication, Qt
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView
from . import jpDataUtils
from .i18n import TR
import os


class JPDataUIHandler:
    def __init__(self, dockwidget):
        self.dw = dockwidget
        self.setup_ui_static_text()

    def setup_ui_static_text(self):
        # Global / Folder Settings
        self.dw.myPushButton2.setText(TR.CHOOSE_FOLDER())
        self.dw.myPushButton2.setToolTip(TR.CHOOSE_FOLDER())
        self.dw.myLabelStatus.setText("")

        self._setup_tab1(0)
        self._setup_tab2(1)
        self._setup_tab3(2)
        self._set_tab_mhlw(3)
        self._setup_tab_addr(4)
        self._setup_tab_setting(5)


    def _setup_tab1(self, i):
        self.dw.myTabWidget.setTabText(i, TR.LANDNUMINFO())
        self.dw.myPushButton11.setText(TR.DOWNLOAD())
        self.dw.myPushButton11.setToolTip(TR.DOWNLOAD_LNI())
        self.dw.myPushButton14.setText(TR.ADD_TO_MAP())
        self.dw.myPushButton14.setToolTip(TR.ADD_TO_MAP_TOOLTIP())
        self.dw.myPushButton15.setText(TR.WEB())
        self.dw.myPushButton15.setToolTip(TR.WEB_TOOLTIP())

        # Selection Modes
        self.dw.myListWidget12.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )
        self.dw.myListWidget13.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )
        self.dw.myListWidget13.hide()

    def _setup_tab2(self, i):
        self.dw.myTabWidget.setTabText(i, TR.GSI_TILES())
        self.dw.myPushButton25.setText(TR.ADD_TO_MAP())
        self.dw.myPushButton25.setToolTip(TR.GSI_TILES_TOOLTIP())

    def _setup_tab3(self, i):
        self.dw.myTabWidget.setTabText(i, TR.CENSUS())
        self.dw.myLabel31.setText(TR.YEAR())
        self.dw.myPushButton31.setText(TR.DOWNLOAD())
        self.dw.myPushButton32.setText(TR.ADD_TO_MAP())
        self.dw.myComboBox31.setToolTip(TR.CENSUS_YEAR_TOOLTIP())
        self.dw.myComboBox32.addItem(TR.NEIGHBOURHOOD())
        self.dw.myComboBox32.addItem(TR.X3_MESH())
        self.dw.myComboBox32.addItem(TR.X4_MESH())
        self.dw.myComboBox32.addItem(TR.X5_MESH())
        self.dw.myComboBox32.addItem(TR.X6_MESH())
        self.dw.myComboBox32.setToolTip(TR.CENSUS_TYPE_TOOLTIP())
        self.dw.myPushButton31.setText(TR.DOWNLOAD())
        self.dw.myPushButton31.setToolTip(TR.DOWNLOAD_CENSUS())
        self.dw.myPushButton32.setText(TR.ADD_TO_MAP())
        self.dw.myPushButton32.setToolTip(TR.ADD_TO_MAP_TOOLTIP())
        self.dw.myListWidget32.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )

        self.dw.myListWidget33.hide()
        self.dw.myListWidget33.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )

    def _set_tab_mhlw(self, i):
        self.dw.myTabWidget.setTabText(i, TR.MHLW())
        self.dw.myPB_MHLW_1.setText(TR.WEB())
        self.dw.myPB_MHLW_2.setText(TR.DOWNLOAD())
        self.dw.myPB_MHLW_3.setText(TR.ADD_TO_MAP())
        # Selection Modes
        self.dw.myLW_MHLW.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if hasattr(QAbstractItemView, "SelectionMode")
            else QAbstractItemView.ExtendedSelection
        )

    def _setup_tab_addr(self, i):
        self.dw.myTabWidget.setTabText(i, TR.ADDRESS())

    def _setup_tab_setting(self, i):
        self.dw.myTabWidget.setTabText(i, TR.SETTING())
        self.dw.myCheckBox1.setText(TR.SETTING_BACKGROUND())
        self.dw.myCheckBox2.setText(TR.SETTING_GEOMETRY())

    def init_tabs(self, land_info_dict, folder_path, MHLW_names):
        self._init_tab1(land_info_dict)
        self._init_tab3()
        self._init_tab_mhlw(MHLW_names)
        self._init_tab_addr(folder_path)

    def _init_tab1(self, land_info_dict, lang="ja"):
        self.dw.myListWidget11.clear()
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
        for thisLandNum in land_info_dict.values():
            item = QListWidgetItem(thisLandNum["name_e"])
            if lang=="ja":
                item = QListWidgetItem(thisLandNum["name_j"])

            if thisLandNum["availability"] != "yes":
                # Disable selection
                if hasattr(Qt, "ItemFlag"):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

                if thisLandNum["availability"] == "heading":
                    item.setBackground(bg)
                    item.setForeground(fg)
                else:
                    item.setForeground(gray)

            self.dw.myListWidget11.addItem(item)

    def _init_tab3(self):
        jpDataUtils.set_pref_items(self.dw.myListWidget31)

    def _init_tab_mhlw(self, MHLW_names, lang="ja"):
        self.dw.myLW_MHLW.clear()
        bg = (
            Qt.GlobalColor.darkGray
            if hasattr(Qt, "GlobalColor")
            else Qt.darkGray
        )
        fg = (
            Qt.GlobalColor.white if hasattr(Qt, "GlobalColor") else Qt.white
        )
        for thisService in MHLW_names.values():
            item = QListWidgetItem(thisService["name_e"])
            if lang=="ja":
                item = QListWidgetItem(thisService["name_j"])
 
            if thisService["code_map"] != "heading":
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
            self.dw.myLW_MHLW.addItem(item)

    def _init_tab_addr(self, folder_path):
        jpDataUtils.set_pref_items(self.dw.myCB_Addr_1)
        if os.path.exists(
            os.path.join(folder_path, "Addr")
        ):  # If the folder exists, set cities
            self.dw.myPB_Addr_1.setText(TR.JUMP())
        else:
            self.dw.myPB_Addr_1.setText(TR.DOWNLOAD())

    def enable_download(self, enable=True):
        if enable:
            self.dw.myPushButton11.setText(TR.DOWNLOAD())
            self.dw.myPushButton31.setText(TR.DOWNLOAD())
            self.dw.myPB_MHLW_2.setText(TR.DOWNLOAD())
            self.dw.myPushButton14.setEnabled(True)
            self.dw.myPushButton32.setEnabled(True)
            self.dw.myPB_MHLW_2.setEnabled(True)
        else:
            self.dw.myPushButton11.setText(TR.CANCEL())
            self.dw.myPushButton31.setText(TR.CANCEL())
            self.dw.myPB_MHLW_2.setText(TR.CANCEL())
            self.dw.myPushButton14.setEnabled(False)
            self.dw.myPushButton32.setEnabled(False)
            self.dw.myPB_MHLW_2.setEnabled(False)


    def set_years_CB(self, years, combBox):
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
