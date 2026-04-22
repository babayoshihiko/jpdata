# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication, Qt
from qgis.PyQt.QtWidgets import QListWidgetItem, QAbstractItemView

class JPDataUIHandler:
    def __init__(self, dockwidget):
        self.dw = dockwidget
        self.setup_ui_static_text()

    def tr(self, message):
        return QCoreApplication.translate("jpdata", message)

    def setup_ui_static_text(self):
        # Global / Folder Settings
        self.dw.myPushButton2.setText(self.tr("Choose Folder"))
        self.dw.myPushButton2.setToolTip(self.tr("Choose Folder"))
        self.dw.myLabelStatus.setText("")

        # Tab 1 (LandNumInfo)
        self.dw.myTabWidget.setTabText(0, self.tr("LandNumInfo"))
        self.dw.myPushButton11.setText(self.tr("Download"))
        self.dw.myPushButton11.setToolTip(self.tr("Download Land Numerical Information data"))
        self.dw.myPushButton14.setText(self.tr("Add to Map"))
        self.dw.myPushButton14.setToolTip(self.tr("Add Shapefile as a Layer to Map on QGIS"))
        self.dw.myPushButton15.setText(self.tr("Web"))
        self.dw.myPushButton15.setToolTip(self.tr("Open the webpage with the standard browser"))
        
        # Selection Modes
        self.dw.myListWidget12.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection if hasattr(QAbstractItemView, 'SelectionMode') else QAbstractItemView.ExtendedSelection)
        self.dw.myListWidget13.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection if hasattr(QAbstractItemView, 'SelectionMode') else QAbstractItemView.ExtendedSelection)
        self.dw.myListWidget13.hide()

        # Tab 2 (GSI)
        self.dw.myTabWidget.setTabText(1, self.tr("GSI Tiles"))
        self.dw.myPushButton25.setText(self.tr("Add to Map"))
        self.dw.myPushButton25.setToolTip(self.tr("Add GSI xyz tile server to Map on QGIS"))

        # Tab 3 (Census)
        self.dw.myTabWidget.setTabText(2, self.tr("Census"))
        self.dw.myLabel31.setText(self.tr("Year"))
        self.dw.myPushButton31.setText(self.tr("Download"))
        self.dw.myPushButton32.setText(self.tr("Add to Map"))
        self.dw.myComboBox31.setToolTip(
            self.tr(
                "Nieghbourhood: Since 2000<br />5th Mesh: Since2005<br />Others: Since 1995"
            )
        )
        self.dw.myComboBox32.addItem(self.tr("Neighbourhood"))
        self.dw.myComboBox32.addItem(self.tr("3rd Mesh"))
        self.dw.myComboBox32.addItem(self.tr("4th Mesh"))
        self.dw.myComboBox32.addItem(self.tr("5th Mesh"))
        self.dw.myComboBox32.setToolTip(
            self.tr(
                "Nieghbourhood: population of cho, aza, etc.<br />3rd Mesh: 1 km mesh<br />4th Mesh: 500 m mesh<br />5th Mesh: 250 m mesh"
            )
        )
        self.dw.myPushButton31.setToolTip(
            self.tr("Download census data by city")
        )
        self.dw.myPushButton32.setToolTip(
            self.tr("Add Shapefile as a Layer to Map on QGIS")
        )
        self.dw.myListWidget32.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection if hasattr(QAbstractItemView, 'SelectionMode') else QAbstractItemView.ExtendedSelection)

        self.dw.myListWidget33.hide()
        self.dw.myListWidget33.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection if hasattr(QAbstractItemView, 'SelectionMode') else QAbstractItemView.ExtendedSelection)


        # Tab 4 (Address)
        self.dw.myTabWidget.setTabText(3, self.tr("Address"))

        # Tab Setting
        self.dw.myTabWidget.setTabText(4, self.tr("Setting"))
        self.dw.myCheckBox1.setText(self.tr("Turn off background download"))
        self.dw.myCheckBox2.setText(self.tr("Check geometry validity when adding"))

    def init_tab1(self, land_info_dict):
        self.dw.myListWidget11.clear()
        for thisLandNum in land_info_dict.values():
            item = QListWidgetItem(thisLandNum["name_j"])
            
            if thisLandNum["availability"] != "yes":
                # Disable selection
                if hasattr(Qt, 'ItemFlag'):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

                if thisLandNum["availability"] == "heading":
                    bg = Qt.GlobalColor.darkGray if hasattr(Qt, 'GlobalColor') else Qt.darkGray
                    fg = Qt.GlobalColor.white if hasattr(Qt, 'GlobalColor') else Qt.white
                    item.setBackground(bg)
                    item.setForeground(fg)
                else:
                    gray = Qt.GlobalColor.gray if hasattr(Qt, 'GlobalColor') else Qt.gray
                    item.setForeground(gray)
            
            self.dw.myListWidget11.addItem(item)

