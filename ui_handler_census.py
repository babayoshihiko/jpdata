# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import (
    Qt,
)
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView, QLineEdit
from . import jpDataMesh
from . import jpDataUtils
from .i18n import TR
from .jpdata_muni import jpDataMuni
from .jpdata_census import jpDataCensus


class JPDataUIHandlerCensus:

    def __init__(self, iface, dockwidget, handler, lang=None):
        self._iface = iface
        self._dw = dockwidget
        self._ui = handler
        # self._lang = lang
        self._connect_signals()
        self._Muni = jpDataMuni.instance()
        self._Census = jpDataCensus.instance()  # Singleton. See manager.py
        self._setup_ui_static_text()
        self._census_populate_init_values()

    def _connect_signals(self):
        # Tab Census
        self._dw.myListWidget31.currentItemChanged.connect(
            self._LW31_currentItemChanged
        )
        self._dw.myListWidget32.itemSelectionChanged.connect(
            self._LW32_itemSelectionChanged
        )
        self._dw.myComboBox32.currentIndexChanged.connect(
            self._LW32_itemSelectionChanged
        )

    def _setup_ui_static_text(self):
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
        self._ui.populate_LW("allprefs", self._dw.myListWidget31)
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

    def _census_populate_init_values(self):
        index = self._dw.myComboBox32.currentIndex()
        self._ui.populate_CB(self._Census.get_years(index), self._dw.myComboBox31)

    def _tab3_set_mesh(self):
        if len(self._dw.myListWidget31.selectedItems()) == 0:
            return
        name_pref = str(self._dw.myListWidget31.selectedItems()[0].text())

        if self._dw.myComboBox32.currentIndex() == 0:
            self._dw.myListWidget33.clear()
            self._dw.myListWidget33.hide()
            return
        years = self._Census.get_years(self._dw.myComboBox32.currentIndex())
        self._ui.populate_CB(years, self._dw.myComboBox31)
        self._dw.myListWidget33.show()
        details = []
        if len(self._dw.myListWidget32.selectedItems()) == 0:
            details = jpDataMesh.getMesh1ByPrefName(name_pref)
        else:
            name_munis = []
            for name_muni in self._dw.myListWidget32.selectedItems():
                name_munis.append(name_muni.text())
            details = jpDataMesh.getMesh1ByPrefMuniName(name_pref, name_munis)
        self._ui.populate_LW(details, self._dw.myListWidget33)

    def _LW31_currentItemChanged(self, current, previous):
        if not current or current == previous or isinstance(current, int):
            return

        name_pref = current.text()
        year = self._dw.myComboBox31.currentText()

        designated_cities = self._Muni.get_all_designated_cities(year)

        rows = self._Muni.get_munis(name_pref)
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
