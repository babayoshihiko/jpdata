# -*- coding: utf-8 -*-
import os, posixpath
from . import jpDataUtils
from .jpdata_muni import jpDataMuni
from qgis import processing
import json


class jpDataCensus:
    _instance = None
    # index:code = [0:"", 1:"SDDSWS", 2:"HDDSWH", 3:"QDDSWQ", 4:"EDDSWE"]
    _CENSUS_CODE = {0:"", 1:"SDDSWS", 2:"HDDSWH", 3:"QDDSWQ", 4:"EDDSWE"}
    _CENSUS_YEAR_STATSID = {
        0: {
            "2020": "001082",
            "2015": "000849",
            "2010": "000573",
            "2005": "000051",
            "2000": "000002",
        },
        1: {
            "2020": "001140",
            "2015": "000846",
            "2010": "000608",
            "2005": "000148",
            "2000": "000146",
            "1995": "000751",
        },
        2: {
            "2020": "001141",
            "2015": "000847",
            "2010": "000609",
            "2005": "000387",
            "2000": "000386",
            "1995": "000752",
        },
        3: {"2020": "001142", "2015": "000876", "2010": "000649", "2005": "000652"},
        4: {"2020": "001231", "2015": "001218"},
    }

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._download_fullpath = "" # This does NOT include Census folder
        self._lang = "j"
        self.record = None
        self._Muni = jpDataMuni.instance()
        _census_json = posixpath.join(os.path.dirname(__file__), "csv", "census_attr.json")
        with open(_census_json, encoding="utf-8") as f:
            self._CENSUS_ATTR = json.load(f)

    def _clear_record(self):
        self.record = {
            "source":"https://www.e-stat.go.jp/gis/statmap-search?type=1",
            "index_census":9,
            "year":"",
            "name_pref":"",
            "code_pref":"",
            "name_muni":"",
            "code_muni":"",
            "code_mesh":"",
            "url":"",
            "zip":"",
            "shp":"",
            "qml":"",
            "epsg":"",
            "encoding":"CP932",
            "download_fullpath":"",
            "subfolder":"Census",
            "attr_url":"",
            "attr_zip":"",
            "attr_csv":""
        }

    def init(self):
        return

    def set_download_folder(self, download_fullpath):
        self._download_fullpath = download_fullpath

    def get_download_folder(self):
        return self._download_fullpath

    def set_lang(self, lang):
        self._lang = lang[:1].lower()

    def get_record(self):
        return self.record
    
    def get_years(self, index_census):
        return list(self._CENSUS_YEAR_STATSID.get(index_census, {}).keys())

    def get_attrs(type_, year):
        try:
            return list(self._CENSUS_ATTR[year][type_].keys())
        except KeyError:
            return []

    def set_record(self, index_census, year, name_pref, name_muni=None, code_mesh=None):
        self._clear_record()
        self.record["index_census"] = index_census
        self.record["year"] = year
        self.record["name_pref"] = name_pref
        self.record["code_pref"] = jpDataUtils.getPrefCodeByName(name_pref)
        self.record["name_muni"] = name_muni
        self.record["code_mesh"] = code_mesh
        if name_muni is not None:
            self.record["code_muni"] = self._Muni.get_code_muni(name_pref, name_muni)
        self._set_url()
        self._set_zip()
        self._set_shp()
        self._set_qml()
        if self._CENSUS_CODE[index_census] == "":
            self.record["subfolder"] = "Census"
        else:
            self.record["subfolder"] = "Census" + "-" + self._CENSUS_CODE[index_census]
        if os.path.exists(posixpath.join(self.record["download_fullpath"], self.record["subfolder"])):
            os.mkdir(posixpath.join(self._download_fullpath, self.record["subfolder"]))
        self.record["download_fullpath"] = posixpath.join(self._download_fullpath, self.record["subfolder"])
        self._set_attr_url()
        self._set_attr_zip()
        self._set_attr_csv()


    def _set_url(self):
        year = self.record["year"] 
        code_pref = self.record["code_pref"] 
        code_muni = self.record["code_muni"] 
        code_mesh = self.record["code_mesh"] 
        if self.record["index_census"] == 0:
            datum = "2011" if int(year) >= 2015 else "2000"
            self.record["url"] = (
                f"https://www.e-stat.go.jp/gis/statmap-search/data?"
                f"dlserveyId=A00200521{year}&"
                f"code={code_pref}{code_muni}&"
                f"coordSys=2&format=shape&downloadType=5&datum={datum}"
            )
        else:
            survey_char = self._CENSUS_CODE[self.record["index_census"]][:1]
            if not survey_char:
                return None
            self.record["url"] = (
                f"https://www.e-stat.go.jp/gis/statmap-search/data?"
                f"dlserveyId={survey_char}&"
                f"code={code_mesh}&"
                f"coordSys=1&format=shape&downloadType=5"
            )

    def _set_zip(self):
        zipFileName = None
        code_pref = self.record["code_pref"]
        code_muni = self.record["code_muni"]
        code_mesh = self.record["code_mesh"]
        if self.record["index_census"] == 0:
            if int(self.record["year"]) >= 2015:
                zipFileName = (
                    "A00200521" + self.record["year"] + "XYSWC" + code_pref + code_muni + "-JGD2011.zip"
                )
            else:
                zipFileName = "A00200521" + self.record["year"] + "XYSWC" + code_pref + code_muni + ".zip"
        else:
            zipFileName = self._CENSUS_CODE[self.record["index_census"]] + code_mesh + ".zip"
        self.record["zip"] = zipFileName

    def _set_shp(self):
        shpFileName = None
        year = self.record["year"] 
        code_pref = self.record["code_pref"] 
        code_muni = self.record["code_muni"] 
        if self.record["index_census"] == 0:
            if year == "2020":
                shpFileName = "r2ka" + code_pref + code_muni + ".shp"
            elif year == "2015":
                shpFileName = "h27ka" + code_pref + code_muni + ".shp"
            elif year == "2010":
                shpFileName = "h22ka" + code_pref + code_muni + ".shp"
            elif year == "2005":
                shpFileName = "h17ka" + code_pref + code_muni + ".shp"
            elif year == "2000":
                shpFileName = "h12ka" + code_pref + code_muni + ".shp"
        else:
            shpFileName = "MESH0" + self.record["code_mesh"]  + ".shp"
        self.record["shp"] = shpFileName

    def _set_qml(self):
        if self.record["index_census"] == 0:
            self.record["qml"] = "Census-" + self.record["year"]  + ".qml"
        else:
            self.record["qml"] = "Census-" + self._CENSUS_CODE[self.record["index_census"]] + "-" + self.record["year"] + ".qml"


    def _get_statsid_for_mesh(self):
        return self._CENSUS_YEAR_STATSID.get(self.record["index_census"], {}).get(self.record["year"])

    def _get_attr_base(self):
        _statsId = self._get_statsid_for_mesh()
        if not _statsId:
            return None
        if self.record["index_census"] == 0:
            suffix = self.record["code_pref"]
        else:
            suffix = self._CENSUS_CODE[self.record["index_census"]][:1] + self.record["code_mesh"]
        return f"{_statsId}{suffix}"
    
    def _set_attr_url(self):
        if self.record["index_census"] == 0:
            _code = self.record["code_pref"]
        else:
            _code = self.record["code_mesh"]
        _statsId = self._get_statsid_for_mesh()
        url = (
            f"https://www.e-stat.go.jp/gis/statmap-search/data?"
            f"statsId=T{_statsId}&"
            f"code={_code}&"
            f"downloadType=2"
        )
        self.record["attr_url"] =  url

    def set_attr_zip(self, key=None):
        self._set_attr_csv(key)
        return self.record["attr_zip"] 

    def _set_attr_zip(self, key=None):
        # Uses
        # key = "人口及び世帯"
        str_i = str(self.record["index_census"])
        if self.record["index_census"] == 0:
            if key is None:
                key = "年齢（５歳階級、４区分）別、男女別人口"
            int_attr = self._CENSUS_ATTR[self.record["year"]][str_i][key]
            base = str(int_attr).zfill(6) + "C" + self.record["code_pref"]        
        else:
            if key is None:
                key = "人口及び世帯"
            int_attr = self._CENSUS_ATTR[self.record["year"]][str_i][key]
            base = str(int_attr).zfill(6) + self._CENSUS_CODE[self.record["index_census"]][:1] + self.record["code_mesh"]
            self.record["attr_zip"] = f"tblT{base}.zip"

    def set_attr_csv(self, key=None):
        self._set_attr_csv(key)
        return self.record["attr_csv"] 

    def _set_attr_csv(self, key=None):
        str_i = str(self.record["index_census"])
        if self.record["index_census"] == 0:
            if key is None:
                key = "年齢（５歳階級、４区分）別、男女別人口"
            int_attr = self._CENSUS_ATTR[self.record["year"]][str_i][key]
            base = str(int_attr).zfill(6) + "C" + self.record["code_pref"]        
        else:
            if key is None:
                key = "人口及び世帯"
            int_attr = self._CENSUS_ATTR[self.record["year"]][str_i][key]
            base = str(int_attr).zfill(6) + self._CENSUS_CODE[self.record["index_census"]][:1] + self.record["code_mesh"]
        file_name = f"tbl{base}.txt"
        file_name_t = f"tblT{base}.txt"
        path = posixpath.join(self.record["download_fullpath"], file_name)
        if os.path.exists(posixpath.join(self.record["download_fullpath"], file_name)):
            self.record["attr_csv"] = file_name
        elif os.path.exists(posixpath.join(self.record["download_fullpath"], file_name_t)):
            self.record["attr_csv"] = file_name_t






    def perform_join(self, folder, year, shp_name, csv_name):
        import processing
        from qgis.core import (
            QgsVectorLayer,
            QgsVectorFileWriter,
            QgsCoordinateTransformContext,
        )
        from qgis.PyQt.QtCore import QUrl

        # 1. Path
        shp_path = posixpath.join(folder, shp_name)
        csv_path = posixpath.join(folder, csv_name)
        output_path = shp_path[:-4] + "-" + year + ".shp"

        # 2. CSV from CP932 (.txt) to UTF-8 (.csv) ---
        csv_utf8 = csv_path[:-4] + ".csv"
        if not os.path.exists(csv_utf8):
            with open(csv_path, "r", encoding="CP932") as fin, open(
                csv_utf8, "w", encoding="UTF-8"
            ) as fout:
                for i, line in enumerate(fin):
                    if i == 1:
                        count = line.count(",")
                        csvt = (
                            "String,Integer,String,String" + ",Integer" * (count - 3)
                            if count > 4
                            else "String" + ",Integer" * count
                        )
                        with open(csv_utf8 + "t", "w", encoding="UTF-8") as f_csvt:
                            f_csvt.write(csvt)
                        continue
                    fout.write(line.replace("*", ""))

        # 3. Create layer objects WITH ENCODING ---
        lyr_shp = QgsVectorLayer(shp_path, "base_shp", "ogr")
        lyr_shp.setProviderEncoding("CP932")
        lyr_shp.dataProvider().setEncoding("CP932")

        uri = QUrl.fromLocalFile(csv_utf8).toString()
        uri += "?delimiter=,&useHeader=yes&detectTypes=yes"
        lyr_csv = QgsVectorLayer(uri, "data_csv", "delimitedtext")
        lyr_csv.setProviderEncoding("UTF-8")
        lyr_csv.dataProvider().setEncoding("UTF-8")

        if not lyr_shp.isValid() or not lyr_csv.isValid():
            return None, None

        join_params = {
            "INPUT": lyr_shp,
            "FIELD": "KEY_CODE",
            "INPUT_2": lyr_csv,
            "FIELD_2": "KEY_CODE",
            "OUTPUT": "TEMPORARY_OUTPUT",
        }
        result = processing.run("qgis:joinattributestable", join_params)
        joined_layer = result["OUTPUT"]

        # --- 5. Save as UTF-8 Shapefile ---
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.fileEncoding = "UTF-8"
        options.driverName = "ESRI Shapefile"

        QgsVectorFileWriter.writeAsVectorFormatV2(
            joined_layer, output_path, QgsCoordinateTransformContext(), options
        )

        # --- 6. .cpg ---
        with open(output_path[:-4] + ".cpg", "w") as f:
            f.write("UTF-8")

        # Memory
        del lyr_shp
        del lyr_csv

        return output_path, "UTF-8"
