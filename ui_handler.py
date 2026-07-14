# -*- coding: utf-8 -*-
import os
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)
from qgis.PyQt.QtCore import (
    Qt, 
    QUrl, 
)
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView, QLineEdit
from qgis.PyQt.QtGui import QDesktopServices, QFontMetrics
from qgis.PyQt.QtWidgets import QLabel, QTreeWidgetItem
from . import jpDataMesh
from . import jpDataUtils
from .i18n import TR
from .ui_handler_lni import JPDataUIHandlerLNI
from .ui_handler_census import JPDataUIHandlerCensus
from .ui_handler_mhlw import JPDataUIHandlerMHLW
from .ui_handler_addr import JPDataUIHandlerAddr



class JPDataUIHandler:
    _verbose = True

    def __init__(self, manager, iface, dockwidget, lang):
        self._manager = manager
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
        self._setup_ui_static_text()
        self._ui_lni = None
        self._ui_census = None
        self._ui_mhlw = None
        self._ui_addr = None


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


    def _setup_ui_static_text(self):
        self._dw.myPushButton2.setText(TR.CHOOSE_FOLDER())
        self._dw.myPushButton2.setToolTip(TR.CHOOSE_FOLDER())
        self._dw.myLabelStatus.setText("")
        self._dw.myLineEditSetting3.setEchoMode(
            QLineEdit.EchoMode.Password
            if hasattr(QLineEdit, "EchoMode")
            else QLineEdit.Password
        )
        self._setup_tab2(1)
        self._setup_tab_setting(5)
        for index, name in self.TABS.items():
            self._dw.myTabWidget.setTabText(index, name)


    def _setup_tab2(self, i):
        self._dw.myPushButton25.setText(TR.ADD_TO_MAP())
        self._dw.myPushButton25.setToolTip(TR.GSI_TILES_TOOLTIP())

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
            if self._ui_lni is None:
                self._ui_lni = JPDataUIHandlerLNI(self._iface, self._dw, self, self._lang)
        elif index == 2:
            if self._ui_census is None:
                self._ui_census = JPDataUIHandlerCensus(self._iface, self._dw, self, self._lang)
        elif index == 3:
            if self._ui_mhlw is None:
                self._ui_mhlw = JPDataUIHandlerMHLW(self._iface, self._dw, self, self._lang)
        elif index == 4:  # addr
            if self._ui_addr is None:
                self._ui_addr = JPDataUIHandlerAddr(self._iface, self._dw, self, self._lang)




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


    def chooseFolder(self):
        from qgis.PyQt.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(
            self._iface.mainWindow(), 
            TR.CHOOSE_FOLDER(), 
            self._manager.get_folder()
        )
        if folder:
            if self._manager.set_folder(folder):
                self.populate_folder(folder)
            else:
                self.populate_folder("~")
                self.setLabel(TR.CHOOSE_FOLDER_INIT())


    def populate_folder(self, folder):
        home = os.path.normpath(os.path.expanduser("~"))
        folder = os.path.normpath(folder)

        if os.path.normcase(folder) == os.path.normcase(home):
            display = "~"
        elif os.path.normcase(folder).startswith(os.path.normcase(home + os.sep)):
            display = "~" + folder[len(home):]
        else:
            display = folder

        fm = QFontMetrics(self._dw.myLabel1.font())
        display = fm.elidedText(display, Qt.TextElideMode.ElideMiddle, self._dw.myLabel1.width())

        self._dw.myLabel1.setText(display)
        self._dw.myLabel1.setToolTip(folder)
