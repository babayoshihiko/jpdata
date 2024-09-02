# -*- coding: utf-8 -*-

from qgis.PyQt import QtGui, QtWidgets, uic
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'jpdata_mesh.ui'))

class jpdataMeshWidget(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(jpdataMeshWidget, self).__init__(parent)
        self.setupUi(self)
