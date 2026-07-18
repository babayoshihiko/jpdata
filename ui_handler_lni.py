# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import (
    Qt,
    QUrl,
)
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView
from qgis.PyQt.QtGui import QDesktopServices
from . import jpDataMesh
from . import jpDataUtils
from .i18n import TR
from .jpdata_lni import jpDataLNI


class JPDataUIHandlerLNI:

    def __init__(self, iface, dockwidget, handler, lang=None):
        self._iface = iface
        self._dw = dockwidget
        self._ui = handler
        self._lang = lang
        self._connect_signals()
        self._LNI = jpDataLNI.instance()  # Singleton. See manager.py
        self._setup_ui_static_text()
        self._lni_populate_init_values()

    def _connect_signals(self):
        # Tab LNI
        self._dw.myListWidget11.itemSelectionChanged.connect(
            self._LW11_itemSelectionChanged
        )
        self._dw.myListWidget12.itemSelectionChanged.connect(
            self._LW12_itemSelectionChanged
        )
        self._dw.myPushButton15.clicked.connect(self._lni_web)
        self._dw.myPB_LNI_Wiki.clicked.connect(self._lni_wiki)

    def _setup_ui_static_text(self):
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

    def _lni_populate_init_values(self):
        self._LNI.init()
        self._dw.myListWidget11.clear()
        bg = Qt.GlobalColor.darkGray if hasattr(Qt, "GlobalColor") else Qt.darkGray
        fg = Qt.GlobalColor.white if hasattr(Qt, "GlobalColor") else Qt.white
        gray = Qt.GlobalColor.gray if hasattr(Qt, "GlobalColor") else Qt.gray
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
            return [
                jpDataUtils.getPrefNameByCode(code, self._LNI.settings.lang1)
                for code in range(1, 48)
            ]

        prev_muni_type = "DUMMY"
        if self._LNI.get_prev_name() != "":
            prev_muni_type = (
                self._LNI.get_records()[self._LNI.get_prev_name()]
                .get("type_muni", "")
                .lower()
            )
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
            self._ui.populate_LW(str_new_LW12_text, self._dw.myListWidget12)

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
            self._LNI_is_Mesh = thisLandNum["type_muni"].lower() == "mesh1"
            self._tab1_set_LW13(name_map, name_pref)

    def _tab1_populate_years(self, name_map):
        years = []
        name_pref = None
        if len(self._dw.myListWidget12.selectedItems()) > 0:
            name_pref = self._dw.myListWidget12.selectedItems()[0].text()
        years = self._LNI.get_years(name_map, name_pref)
        self._ui.populate_CB(years, self._dw.myComboBox11)

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
        self._ui.populate_LW(details, self._dw.myListWidget13)
        if (
            not self._dw.myListWidget13.selectedItems()
            and thisLandNum["type_muni"].lower() == "mesh1"
        ):
            point = self._iface.mapCanvas().center()
            code = self._ui._updateMeshCode(point)
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
