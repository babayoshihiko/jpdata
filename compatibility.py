# -*- coding: utf-8 -*-

from . import jpDataUtils
from qgis.core import (
    QgsProject,
    QgsProviderRegistry,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsSettings,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsWkbTypes
)
from qgis.PyQt.QtCore import (
    Qt, 
    QVariant, 
    QMetaType, 
    QPointF
)

try:
    from qgis.PyQt.QtCore import QMetaType

    STRING = QMetaType.Type.QString
    INT = QMetaType.Type.Int
    DOUBLE = QMetaType.Type.Double
    BOOL = QMetaType.Type.Bool
    DATE = QMetaType.Type.QDate
except ImportError:
    from qgis.PyQt.QtCore import QVariant

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
        }
    )


    csv_layer = QgsVectorLayer(uri, layerName, "delimitedtext")

    if not csv_layer.isValid():
        jpDataUtils.printDebugLog("28")
        return None

    point_layer = QgsVectorLayer(
        f"Point?crs=EPSG:{epsg}",
        layerName,
        "memory"
    )

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
        feat.setGeometry(
            QgsGeometry.fromPointXY(QgsPointXY(x, y))
        )

        features.append(feat)

    pr.addFeatures(features)

    point_layer.updateExtents()
    point_layer.triggerRepaint()

    # QgsProject.instance().addMapLayer(point_layer)

    return point_layer


