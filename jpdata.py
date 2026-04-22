# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .manager import JPDataManager

class jpdata:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(self.plugin_dir, "i18n", f"jpdata_{locale}.qm")
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.manager = JPDataManager(self.iface)
        self.action = None

    def tr(self, message):
        return QCoreApplication.translate("jpdata", message)

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        self.action = QAction(
            QIcon(icon_path),
            self.tr("jpdata"),
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu(self.tr("&jpdata"), self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginMenu(self.tr("&jpdata"), self.action)
        self.manager.unload()

    def run(self):
        self.manager.run()