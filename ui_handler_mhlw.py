# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import (
    Qt, 
    QUrl, 
)
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView
from qgis.PyQt.QtGui import QDesktopServices
from . import jpDataUtils
from .i18n import TR
from .jpdata_mhlw import jpDataMHLW
from .jpdata_muni import jpDataMuni




class JPDataUIHandlerMHLW:

    def __init__(self, iface, dockwidget, handler, lang):
        self._iface = iface
        self._dw = dockwidget
        self._ui = handler
        self._lang = lang

        self._connect_signals()
        self._Muni = jpDataMuni.instance()
        self._MHLW = jpDataMHLW.instance()         # Singleton. See manager.py
        self._setup_ui_static_text()
        self._mhlw_populate_init_values()


    def _connect_signals(self):
        # Tab MHLW
        self._dw.myLW_MHLW.currentRowChanged.connect(self._mhlw_map_changed)
        self._dw.myPB_MHLW_1.clicked.connect(self._mhlw_web)
        self._dw.myPB_MHLW_Wiki.clicked.connect(self._mhlw_wiki)


    def _setup_ui_static_text(self):
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


    def _mhlw_populate_init_values(self):
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


    def _mhlw_map_changed(self, row):
        item = self._dw.myLW_MHLW.item(row)
        if item is None:
            return
        name_map = item.text()
        years = self._MHLW.get_years(name_map)
        self._ui.populate_CB(years, self._dw.myCB_MHLW)
