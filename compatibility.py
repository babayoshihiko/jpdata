# -*- coding: utf-8 -*-

from . import jpDataUtils
from qgis.core import (
    Qgis,
    QgsProviderRegistry,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsUnitTypes,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import (
    Qt,
    QVariant,
    QMetaType,
)
from qgis.PyQt.QtWidgets import (
    QAbstractItemView,
    QLineEdit,
)

if Qgis.QGIS_VERSION_INT >= 40000:
    CHECKED = Qt.CheckState.Checked
    COL_DG = Qt.GlobalColor.darkGray
    COL_GRAY = Qt.GlobalColor.gray
    COL_WHITE = Qt.GlobalColor.white
    DOCK_LEFT = Qt.DockWidgetArea.LeftDockWidgetArea
    GEOM_POINT = QgsWkbTypes.GeometryType.PointGeometry
    ITEM_IS_SELECTABLE = Qt.ItemFlag.ItemIsSelectable
    LE_PASSWD = QLineEdit.EchoMode.Password
    MESSAGE_INFO = Qgis.MessageLevel.Info
    MESSAGE_WARNING = Qgis.MessageLevel.Warning
    MESSAGE_CRITICAL = Qgis.MessageLevel.Critical
    PARTIALLY_CHECKED = Qt.CheckState.PartiallyChecked
    RENDER_MAP_UNITS = QgsUnitTypes.RenderUnit.RenderMapUnits
    RENDER_PIXELS = QgsUnitTypes.RenderUnit.RenderPixels
    SELECTION_EXTENDED = QAbstractItemView.SelectionMode.ExtendedSelection
    TEXT_MOUSE = Qt.TextInteractionFlag.TextSelectableByMouse
    UNCHECKED = Qt.CheckState.Unchecked
    USER_ROLE = Qt.ItemDataRole.UserRole
else:
    CHECKED = Qt.Checked
    COL_DG = Qt.darkGray
    COL_GRAY = Qt.gray
    COL_WHITE = Qt.white
    DOCK_LEFT = Qt.LeftDockWidgetArea
    GEOM_POINT = QgsWkbTypes.PointGeometry
    ITEM_IS_SELECTABLE = Qt.ItemIsSelectable
    LE_PASSWD = QLineEdit.Password
    MESSAGE_INFO = Qgis.Info
    MESSAGE_WARNING = Qgis.Warning
    MESSAGE_CRITICAL = Qgis.Critical
    PARTIALLY_CHECKED = Qt.PartiallyChecked
    RENDER_MAP_UNITS = QgsUnitTypes.RenderMapUnits
    RENDER_PIXELS = QgsUnitTypes.RenderPixels
    SELECTION_EXTENDED = QAbstractItemView.ExtendedSelection
    TEXT_MOUSE = Qt.TextSelectableByMouse
    UNCHECKED = Qt.Unchecked
    USER_ROLE = Qt.UserRole


if Qgis.QGIS_VERSION_INT >= 34000:
    STRING = QMetaType.Type.QString
    INT = QMetaType.Type.Int
    DOUBLE = QMetaType.Type.Double
    BOOL = QMetaType.Type.Bool
    DATE = QMetaType.Type.QDate
else:
    STRING = QVariant.String
    INT = QVariant.Int
    DOUBLE = QVariant.Double
    BOOL = QVariant.Bool
    DATE = QVariant.Date


def add_map_qgis322(shp_fullpath, layerName, xField, yField, epsg, encoding="UTF-8"):
    uri = QgsProviderRegistry.instance().encodeUri(
        "delimitedtext",
        {
            "path": shp_fullpath,
            "delimiter": ",",
            "encoding": encoding,
        },
    )

    csv_layer = QgsVectorLayer(uri, layerName, "delimitedtext")

    if not csv_layer.isValid():
        jpDataUtils.printDebugLog("compatibility.py: Failed to load the csv file: " + shp_fullpath)
        return None

    point_layer = QgsVectorLayer(f"Point?crs=EPSG:{epsg}", layerName, "memory")

    pr = point_layer.dataProvider()
    pr.addAttributes(csv_layer.fields())
    point_layer.updateFields()

    features = []

    for row in csv_layer.getFeatures():

        try:
            x = float(row[xField])
            y = float(row[yField])
        except (TypeError, ValueError):
            continue

        feat = QgsFeature(point_layer.fields())
        feat.setAttributes(row.attributes())
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))

        features.append(feat)

    pr.addFeatures(features)

    point_layer.updateExtents()
    point_layer.triggerRepaint()

    # QgsProject.instance().addMapLayer(point_layer)

    return point_layer
