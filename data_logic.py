# -*- coding: utf-8 -*-
import posixpath
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer
from . import jpDataLNI, jpDataUtils, jpDataMesh

class JPDataLogic:
    def __init__(self, iface):
        self.iface = iface

    def get_folder_path(self):
        from qgis.PyQt.QtCore import QSettings
        return QSettings().value("jpdata/FolderPath", "~")

    def add_gsi_tile(self, tile_data):
        tile_url = (f"type=xyz&url={tile_data['url']}"
                    f"&zmax={tile_data['zoom_max']}&zmin={tile_data['zoom_min']}&crs=EPSG3857")
        layer = QgsRasterLayer(tile_url, tile_data["name_j"], "wms")
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            return True
        return False

    def prepare_lni_download(self, map_name, pref_names, year, land_num_info_all):
        this_land_num = land_num_info_all[map_name]
        download_list = []

        for pref_item in pref_names:
            pref_name = pref_item.text()
            if this_land_num["type_muni"].lower() == "mesh1":
                replace_code = "MESH_CODE_HERE" 
            else:
                replace_code = jpDataUtils.getPrefCodeByName(pref_name)

            url, zip_file, subfolder = jpDataLNI.getZip(
                year, this_land_num, pref_name, replace_code, "urlzip"
            )
            if zip_file:
                download_list.append({
                    "year": year, "url": url, "zip": zip_file, "subfolder": subfolder
                })
        return download_list

    def add_lni_layer(self, map_name, pref_name, year, land_num_info_all, detail=None):
        this_land_num = land_num_info_all[map_name]
        folder_base = self.get_folder_path()
        
        pref_code = jpDataUtils.getPrefCodeByName(pref_name) if pref_name else ""
        
        res = jpDataLNI.getZip(year, this_land_num, pref_name, pref_code, "full", detail=detail)
        zip_fn, shp_fn, altdir, qml, epsg, enc, subf, layer_name = res

        shp_path = jpDataUtils.unzipAndGetShp(
            posixpath.join(folder_base, subf), zip_fn, shp_fn, altdir, pref_code,
            epsg=epsg, encoding=enc
        )

        if shp_path:
            layer = QgsVectorLayer(shp_path, layer_name, "ogr")
            if layer.isValid():
                QgsProject.instance().addMapLayer(layer)
                return True
