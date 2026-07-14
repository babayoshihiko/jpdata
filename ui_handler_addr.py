# -*- coding: utf-8 -*-
import os, posixpath
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsField,
    QgsMarkerSymbol,
    QgsSvgMarkerSymbolLayer,
    QgsUnitTypes,
    QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling,
    QgsTextFormat,
)
from qgis.PyQt.QtCore import (
    Qt, 
    QVariant, 
    QMetaType, 
    QPointF
)
from qgis.PyQt.QtGui import QFont, QColor
from qgis.PyQt.QtWidgets import QAction
from . import jpDataUtils
from .i18n import TR
from .jpdata_muni import jpDataMuni


class JPDataUIHandlerAddr:
    _verbose = True

    def __init__(self, iface, dockwidget, handler, lang):
        self._iface = iface
        self._dw = dockwidget
        self._ui = handler
        self._lang = lang
        self._Muni = jpDataMuni.instance()
        self._pin_layer = None
        self._mesh_layer = None
        self.mesh3_action = None
        self._connect_signals()
        self._setup_tab_addr()
        self._addr_populate_init_values()

    def _connect_signals(self):
        # Tab Addr
        self._dw.myCB_Addr_1.currentIndexChanged.connect(self._myCB_Addr_1_changed)
        self._dw.myCB_Addr_2.currentIndexChanged.connect(self._myCB_Addr_2_changed)
        self._dw.myCB_Addr_3.currentIndexChanged.connect(self._myCB_Addr_3_changed)
        self._dw.myPB_Addr_2.clicked.connect(self._myPB_Addr_2_clicked)
        self._dw.myPB_Addr_3.clicked.connect(self._myPB_Addr_3_clicked)
        self._dw.myPB_Addr_4.clicked.connect(self._myPB_Addr_4_clicked)

        self._dw.myTreeWidget.itemChanged.connect(self._tree_item_changed)

        # Tree View  contextMenuAboutToShow since QGIS 3.40
        # view = self._iface.layerTreeView()
        # view.contextMenuAboutToShow.connect(self.on_context_menu)
        # self._iface.mapCanvas().contextMenuAboutToShow.connect(self.on_canvas_context_menu)

        # Create mesh
        self.mesh3_action = QAction(TR.CREATE_THIRD_MESH(), self._iface.mainWindow())
        self.mesh3_action.triggered.connect(
            self.add_mesh3_from_selected
        )

    def _setup_tab_addr(self):
        self._dw.myPB_Addr_1.setText(TR.DOWNLOAD())
        self._dw.myPB_Addr_2.setText(TR.JUMP())
        self._dw.myPB_Addr_3.setText(TR.REPROJECT())
        self._dw.myPB_Addr_4.setText(TR.ADD_MESH())

    def _addr_populate_init_values(self):
        self._ui.populate_CB("allprefs", self._dw.myCB_Addr_1, add_empty_item=True)
        if hasattr(self, "_Muni"):
            projs = self._Muni.get_projections()
            for proj in projs:
                self._dw.myCB_Addr_Projection.addItem(proj)


    def unload(self):
        pass


    def _create_pin_layer(self):
        # Memory Layer For Address Search
        layers = QgsProject.instance().mapLayersByName("Address Pin")

        if layers:
            self._pin_layer = layers[0]
        else:
            self._pin_layer = QgsVectorLayer(
                f"Point?crs={QgsProject.instance().crs().authid()}",
                "Address Pin",
                "memory"
            )
            pr = self._pin_layer.dataProvider()
            pr.addAttributes([
                self._create_string_field("name"),
                self._create_string_field("pref"),
                self._create_string_field("muni"),
            ])
            self._pin_layer.updateFields()
            svg_path = None
            for p in QgsApplication.svgPaths():
                candidate = posixpath.join(p, "symbol", "blue-marker.svg")
                if os.path.exists(candidate):
                    svg_path = candidate
                    break
            if svg_path:
                symbol = QgsMarkerSymbol.createSimple({})
                svg_layer = QgsSvgMarkerSymbolLayer(svg_path)
                svg_layer.setSize(128)
                svg_layer.setSizeUnit(QgsUnitTypes.RenderPixels)
                svg_layer.setOffset(QPointF(0, -64))
                svg_layer.setOffsetUnit(QgsUnitTypes.RenderPixels)
                symbol.changeSymbolLayer(0, svg_layer)
                self._pin_layer.renderer().setSymbol(symbol)
            QgsProject.instance().addMapLayer(self._pin_layer)


    def _create_string_field(self, name):
        # QGIS 3.22 and earlier
        try:
            from qgis.PyQt.QtCore import QVariant
            return QgsField(name, QVariant.String)
        except Exception:
            pass

        # Qt6/QGIS4 and QGIS3.40
        try:
            from qgis.PyQt.QtCore import QMetaType
            return QgsField(name, QMetaType.QString)
        except Exception:
            pass

        try:
            from qgis.PyQt.QtCore import QMetaType
            return QgsField(name, QMetaType.Type.QString)
        except Exception:
            pass

        raise RuntimeError("No compatible string type found for QgsField")

    def _tree_item_changed(self, item, column):
        tab = item.data(0, Qt.UserRole)
        if tab is None:
            return

        self._dw.myTabWidget.setTabVisible(
            tab,
            item.checkState(0) == Qt.Checked
        )

    def _myPB_Addr_2_clicked(self):
        lon, lat = self._Muni.get_lonlat_by_addr(
            str(self._dw.myCB_Addr_1.currentText()),
            str(self._dw.myCB_Addr_2.currentText()),
            str(self._dw.myCB_Addr_3.currentText()),
            str(self._dw.myCB_Addr_4.currentText()),
        )
        if lon is None or lat is None:
            self.setLabel(TR.NO_XY())
            return
        point_jgd2011 = QgsPointXY(lon, lat)

        # Transform to project CRS
        crs_src = QgsCoordinateReferenceSystem("EPSG:6668")  # JGD2011
        crs_dest = self._iface.mapCanvas().mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(crs_src, crs_dest, QgsProject.instance())
        try:
            point_project = transform.transform(point_jgd2011)
        except Exception as e:
            self.setLabel(str(e))
            return


        # Set canvas center
        canvas = self._iface.mapCanvas()
        canvas.setCenter(point_project)
        canvas.refresh()

        self.set_pin(lon,lat)

    def set_pin(self,lon,lat):
        self._create_pin_layer()
        pr = self._pin_layer.dataProvider()
        # pr.truncate()
        feat = QgsFeature(self._pin_layer.fields())
        feat.setGeometry(
            QgsGeometry.fromPointXY(QgsPointXY(lon,lat))
        )
        feat["pref"] = str(self._dw.myCB_Addr_1.currentText())
        feat["muni"] = str(self._dw.myCB_Addr_2.currentText())
        pr.addFeature(feat)
        self._pin_layer.updateExtents()
        self._pin_layer.triggerRepaint()



    def _myPB_Addr_3_clicked(self):
        lon, lat = self._Muni.get_lonlat_by_addr(
            str(self._dw.myCB_Addr_1.currentText()),
            str(self._dw.myCB_Addr_2.currentText()),
            str(self._dw.myCB_Addr_3.currentText()),
            str(self._dw.myCB_Addr_4.currentText()),
        )
        if lon is None or lat is None:
            self.setLabel(TR.NO_XY())
            return
        from qgis.core import QgsCoordinateReferenceSystem, QgsProject
        proj_index = self._dw.myCB_Addr_Projection.currentIndex()
        proj_string = self._Muni.get_proj_string(proj_index, lat, lon)
        crs = QgsCoordinateReferenceSystem.fromProj(proj_string)
        if crs.isValid():
            QgsProject.instance().setCrs(crs)
            self.add_graticule_layer()
        else:
            self.setLabel(TR.INVALID_PROJECTION())


    def _myPB_Addr_4_clicked(self):
        self.add_mesh_layer()

    def _myCB_Addr_1_changed(self):
        name_pref = self._dw.myCB_Addr_1.currentText()
        munis = self._Muni.get_munis(name_pref)
        self._ui.populate_CB(munis, self._dw.myCB_Addr_2, add_empty_item=True)
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        if self._Muni.get_csv_fullpath(code_pref):
            self._dw.myPB_Addr_1.setEnabled(False)
        else:
            self._dw.myPB_Addr_1.setEnabled(True)

    def _myCB_Addr_2_changed(self):
        name_pref = self._dw.myCB_Addr_1.currentText()
        name_muni = self._dw.myCB_Addr_2.currentText()
        towns = self._Muni.get_towns(name_pref, name_muni)
        self._ui.populate_CB(towns, self._dw.myCB_Addr_3, add_empty_item=True)

    def _myCB_Addr_3_changed(self):
        name_pref = self._dw.myCB_Addr_1.currentText()
        name_muni = self._dw.myCB_Addr_2.currentText()
        name_town = self._dw.myCB_Addr_3.currentText()
        details = self._Muni.get_details(name_pref, name_muni, name_town)
        self._ui.populate_CB(details, self._dw.myCB_Addr_4, add_empty_item=True)


    def add_graticule_layer(self, interval=10):
        layer = QgsVectorLayer(
            "LineString?crs=EPSG:4326",
            f"Graticule_{interval}deg",
            "memory",
        )
        provider = layer.dataProvider()
        provider.addAttributes([
            QgsField("type", QVariant.String),
            QgsField("value", QVariant.Int),
        ])
        layer.updateFields()
        features = []
        for lon in range(-180, 181, interval):
            points = [
                QgsPointXY(lon, lat)
                for lat in range(-90, 91)
            ]

            feat = QgsFeature(layer.fields())
            feat.setGeometry(QgsGeometry.fromPolylineXY(points))
            feat["type"] = "longitude"
            feat["value"] = lon
            features.append(feat)
        for lat in range(-80, 81, interval):
            points = [
                QgsPointXY(lon, lat)
                for lon in range(-180, 181)
            ]
            feat = QgsFeature(layer.fields())
            feat.setGeometry(QgsGeometry.fromPolylineXY(points))
            feat["type"] = "latitude"
            feat["value"] = lat
            features.append(feat)
        provider.addFeatures(features)
        layer.updateExtents()
        QgsProject.instance().addMapLayer(layer)
        return layer

    def add_mesh_layer(self):
        # Memory Layer For Address Search
        layers = QgsProject.instance().mapLayersByName("Mesh")
        if layers:
            self._mesh_layer = layers[0]
        else:
            self._mesh_layer = QgsVectorLayer(
                "Polygon?crs=EPSG:4326",
                "Mesh",
                "memory"
            )
        pr = self._mesh_layer.dataProvider()
        pr.addAttributes([QgsField("code_mesh", QVariant.String)])
        self._mesh_layer.updateFields()
        features = []
        for p in range(30, 69):
            for u in range(22, 46):
                code = f"{p}{u}"
                lat0 = p / 1.5
                lon0 = u + 100
                lat1 = lat0 + 40 / 60
                lon1 = lon0 + 1
                geom = QgsGeometry.fromPolygonXY([[
                    QgsPointXY(lon0, lat0),
                    QgsPointXY(lon1, lat0),
                    QgsPointXY(lon1, lat1),
                    QgsPointXY(lon0, lat1),
                    QgsPointXY(lon0, lat0),
                ]])
                feat = QgsFeature(self._mesh_layer.fields())
                feat["code_mesh"] = code
                feat.setGeometry(geom)
                features.append(feat)
        pr.addFeatures(features)
        self._mesh_layer.updateExtents()
        # Label
        fmt = QgsTextFormat()
        fmt.setFont(QFont("Meiryo", 8))
        settings = QgsPalLayerSettings()
        settings.fieldName = "code_mesh"
        settings.setFormat(fmt)
        self._mesh_layer.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        self._mesh_layer.setLabelsEnabled(True)
        # Symbol
        symbol = self._mesh_layer.renderer().symbol()
        symbol.setColor(QColor(230, 230, 230, 51))      # α=51≒80%透明
        symbol.symbolLayer(0).setStrokeColor(QColor(180, 180, 180))
        symbol.symbolLayer(0).setStrokeWidth(0.1)
        QgsProject.instance().addMapLayer(self._mesh_layer)
        # Layer tree
        root = QgsProject.instance().layerTreeRoot()
        node = root.findLayer(self._mesh_layer.id())
        if node is None:
            return self._mesh_layer
        clone = node.clone()
        root.insertChildNode(0, clone)
        root.removeChildNode(node)
        return self._mesh_layer


    def on_context_menu(self, menu):
        if self.mesh3_action not in menu.actions():
            menu.addAction(self.mesh3_action)
    
    def on_canvas_context_menu(self, menu, event):
        if self.mesh3_action not in menu.actions():
            menu.addAction(self.mesh3_action)

    def add_mesh3_from_selected(self):
        if self._mesh_layer is None:
            return
        features = []
        pr = self._mesh_layer.dataProvider()
        for feat in self._mesh_layer.selectedFeatures():
            code1 = feat["code_mesh"]
            p = int(code1[:2])
            u = int(code1[2:4])
            lat0 = p / 1.5
            lon0 = u + 100
            for q in range(8):
                for v in range(8):
                    lat2 = lat0 + q * (5 / 60)
                    lon2 = lon0 + v * (7.5 / 60)
                    for r in range(10):
                        for w in range(10):
                            code3 = f"{code1}{q}{v}{r}{w}"
                            y0 = lat2 + r * (30 / 3600)
                            x0 = lon2 + w * (45 / 3600)
                            y1 = y0 + 30 / 3600
                            x1 = x0 + 45 / 3600
                            geom = QgsGeometry.fromPolygonXY([[
                                QgsPointXY(x0, y0),
                                QgsPointXY(x1, y0),
                                QgsPointXY(x1, y1),
                                QgsPointXY(x0, y1),
                                QgsPointXY(x0, y0),
                            ]])
                            f = QgsFeature(self._mesh_layer.fields())
                            f.setGeometry(geom)
                            f["code_mesh"] = code3
                            features.append(f)
        pr.addFeatures(features)
        self._mesh_layer.updateExtents()
        self._mesh_layer.removeSelection()


