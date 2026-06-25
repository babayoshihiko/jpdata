# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .translation import setup_translation
from .manager import JPDataManager

class jpData:
    def __init__(self, iface):
        self.plugin_dir = os.path.dirname(__file__)
        self.translator = setup_translation(
            self.plugin_dir,
            'jpData'
        )
        self.iface = iface

        self.manager = JPDataManager(self.iface)
        self.action = None


    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        self.action = QAction(
            QIcon(icon_path),
            "jpdata",
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&jpdata", self.action)

    def unload(self):
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&jpdata", self.action)
        self.manager.unload()

    def run(self):
        self.manager.run()