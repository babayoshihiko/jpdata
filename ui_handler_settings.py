# -*- coding: utf-8 -*-
import os, tempfile
from qgis.PyQt.QtCore import (
    Qt,
)
from qgis.PyQt.QtWidgets import (
    QTreeWidgetItem,
    QLineEdit,
    QCheckBox,
    QWidget,
    QHBoxLayout,
    QPushButton,
)
from qgis.PyQt.QtWidgets import QTreeWidgetItem
from .jpdata_settings import jpDataSettings
from . import jpDataUtils
from .compatibility import LE_PASSWD
from .i18n import TR


class JPDataUIHandlerSettings:

    def __init__(self, iface, dockwidget, handler):
        self.settings = jpDataSettings.instance()

        self._iface = iface
        self._dw = dockwidget
        self._ui = handler

        self._setup()

    def _setup(self):
        tree = self._dw.myTreeWidget
        tree.clear()

        tree.setColumnCount(2)
        tree.setHeaderLabels([TR.DESC(), TR.VALUE()])

        #
        # General
        #
        general = QTreeWidgetItem(tree)
        general.setText(0, TR.GENERAL())

        # Download
        item = QTreeWidgetItem(general)
        item.setText(0, TR.DOWNLOAD_FOLDER())

        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)

        self._folderEdit = QLineEdit(self.settings.folder_path)
        btn = QPushButton("...")

        layout.addWidget(self._folderEdit)
        layout.addWidget(btn)

        tree.setItemWidget(item, 1, w)

        btn.clicked.connect(self.chooseFolder)

        item = QTreeWidgetItem(general)
        item.setText(0, TR.CHECK_GEOM())

        self._geometryCheck = QCheckBox()
        self._geometryCheck.setChecked(True)
        tree.setItemWidget(item, 1, self._geometryCheck)

        proxy = QTreeWidgetItem(tree)
        proxy.setText(0, TR.PROXY())

        def addLine(parent, title, value="", password=False):
            item = QTreeWidgetItem(parent)
            item.setText(0, title)

            edit = QLineEdit(value)
            if password:
                edit.setEchoMode(LE_PASSWD)

            tree.setItemWidget(item, 1, edit)
            return edit

        self._proxyUrlEdit = addLine(proxy, "URL", self.settings.proxy_server)
        self._proxyUserEdit = addLine(proxy, TR.USER())
        self._proxyPassEdit = addLine(proxy, TR.PASSWORD(), password=True)

        # Tab
        tabs = QTreeWidgetItem(tree)
        tabs.setText(0, TR.TAB())

        for index, name in self._ui.TABS.items():
            if name == TR.SETTING():
                continue

            item = QTreeWidgetItem(tabs)
            item.setText(0, name)

            check = QCheckBox()
            check.setChecked(True)

            tree.setItemWidget(item, 1, check)
            check.toggled.connect(
                lambda checked, i=index: self._dw.myTabWidget.setTabVisible(i, checked)
            )

        tree.expandAll()
        tree.resizeColumnToContents(0)

    def chooseFolder(self):
        from qgis.PyQt.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(
            self._iface.mainWindow(), TR.CHOOSE_FOLDER(), self.settings.folder_path
        )
        if folder:
            if self.set_folder(folder):
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
            display = "~" + folder[len(home) :]
        else:
            display = folder

        self._folderEdit.setText(display)

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

    def set_folder(self, folder):
        if not folder:
            return False
        if not os.path.isdir(folder):
            return False
        if not self._is_writable(folder):
            return False

        self.settings.folder_path = folder
        return True

    def _is_writable(self, folder):
        try:
            fd, path = tempfile.mkstemp(dir=folder)
            os.close(fd)
            os.remove(path)
            return True
        except OSError:
            return False
