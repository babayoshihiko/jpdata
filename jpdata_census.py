# -*- coding: utf-8 -*-
import os, posixpath
from . import jpDataUtils
from qgis import processing


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
        self.download_fullpath = ""


    def _get_statsid_for_mesh(index_census, year):
        return self._CENSUS_YEAR_STATSID.get(index_census, {}).get(str(year))

    def init(self):
        return

    def set_download_folder(self, download_fullpath):
        if not os.path.exists(posixpath.join(download_fullpath, "Census")):
            os.mkdir(posixpath.join(download_fullpath, "Census"))
        self.download_fullpath = posixpath.join(download_fullpath, "Census")

    def set_lang(self, lang):
        self.lang = lang[:1].lower()

    def get_records(self):
        return
    
    def get_years(self, index_census):
        return list(self._CENSUS_YEAR_STATSID.get(index_census, {}).keys())

    def get_prefs(self, code_census):
        return
    
    def get_shp(self, code_census, name_pref, year, detail):
        return self.getZipShp()
    
    def get_url_zip(self, code_census, year, name_pref, code_muni_mesh):
        return self.getZip()

    def get_zip_shp(self, code_census, year, name_pref, code_muni_mesh):
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        return self.getZipShp(year, code_pref, code_muni_mesh, code_census)



    def _get_char_for_mesh(index_census):
        if 0 <= index_census < len(_CENSUS_CODE):
            return _CENSUS_CODE[index_census][:1]
        return ""

    def _get_string_for_mesh(index_census):
        if 0 <= index_census < len(_CENSUS_CODE):
            return _CENSUS_CODE[index_census]
        return ""

    def get_subfolder_qml(type_muni, year):
        if type_muni == 0:
            tempSubFolder = "Census"
            tempQmlFile = "Census-" + year + ".qml"
        else:
            tempSubFolder = _get_string_for_mesh(type_muni)
            tempQmlFile = "Census-" + _get_string_for_mesh(type_muni) + "-" + year + ".qml"
        return tempSubFolder, tempQmlFile

    def getZipShp(year, code_pref, code_muni, type_muni=0):
        tempZipFileName = getZipFileName(
            year,
            code_pref,
            code_muni,
            type_muni,
        )
        tempShpFileName = getShpFileName(
            year,
            code_pref,
            code_muni,
            type_muni,
        )
        return tempZipFileName, tempShpFileName

    def getZip(year, code_pref, code_muni, type_muni=0):
        tempUrl = getUrl(year, code_pref, code_muni, type_muni)
        tempZip = getZipFileName(year, code_pref, code_muni, type_muni)
        tempSubFolder, tmpQmlFile = get_subfolder_qml(type_muni, year)
        return tempUrl, tempZip, tempSubFolder

    def getUrl(year, code_pref, code_muni, type_muni=0):
        code_pref = str(code_pref).zfill(2)
        if type_muni == 0:
            datum = "2011" if year in ["2020", "2015"] else "2000"

            return (
                f"https://www.e-stat.go.jp/gis/statmap-search/data?"
                f"dlserveyId=A00200521{year}&"
                f"code={code_pref}{code_muni}&"
                f"coordSys=2&format=shape&downloadType=5&datum={datum}"
            )
        survey_char = _get_char_for_mesh(type_muni)

        if not survey_char:
            return None

        return (
            f"https://www.e-stat.go.jp/gis/statmap-search/data?"
            f"dlserveyId={survey_char}&"
            f"code={code_muni}&"
            f"coordSys=1&format=shape&downloadType=5"
        )

    def getZipFileName(year, code_pref, code_muni, type_muni=0):
        zipFileName = None
        if type_muni == 0:
            if len(code_pref) == 1:
                code_pref = "0" + code_pref
            if year == "2020" or year == "2015":
                zipFileName = (
                    "A00200521" + year + "XYSWC" + code_pref + code_muni + "-JGD2011.zip"
                )
            else:
                zipFileName = "A00200521" + year + "XYSWC" + code_pref + code_muni + ".zip"
        else:
            zipFileName = _get_string_for_mesh(type_muni) + code_muni + ".zip"
        return zipFileName

    def getShpFileName(year, code_pref, code_muni, type_muni=0):
        shpFileName = None
        if len(code_pref) == 1:
            code_pref = "0" + code_pref
        if type_muni == 0:
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
        elif type_muni >= 1:
            shpFileName = "MESH0" + code_muni + ".shp"
        return shpFileName


    def getAttr(year, code_pref, code_muni, type_muni=0):
        tempUrl = getAttrUrl(year, code_pref, code_muni, type_muni)
        tempZip = getAttrZipFileName(year, code_pref, code_muni, type_muni)
        tempSubFolder, tmpQmlFile = get_subfolder_qml(type_muni, year)
        return tempUrl, tempZip, tempSubFolder


    def getAttrUrl(year, code_pref, code_muni, type_muni=0):
        if type_muni == 0:
            _code = str(code_pref).zfill(2)
        else:
            _code = code_muni
        _statsId = _get_statsid_for_mesh(year, type_muni)
        if not _code:
            return None
        url = (
            f"https://www.e-stat.go.jp/gis/statmap-search/data?"
            f"statsId=T{_statsId}&"
            f"code={_code}&"
            f"downloadType=2"
        )
        return url

    def _get_base_filename(year, code_pref, code_muni, type_muni):
        _statsId = _get_statsid_for_mesh(year, type_muni)
        if not _statsId:
            return None
        if type_muni == 0:
            suffix = f"C{str(code_pref).zfill(2)}"
        else:
            char = _get_char_for_mesh(type_muni)
            suffix = f"{char}{code_muni}"

        return f"{_statsId}{suffix}"

    def getAttrZipFileName(year, code_pref, code_muni, type_muni=0):
        base = _get_base_filename(year, code_pref, code_muni, type_muni)
        return f"tblT{base}.zip" if base else None

    def get_attr_csv_filename(year, code_pref, code_muni, type_muni=0, folder="."):
        base = _get_base_filename(year, code_pref, code_muni, type_muni)
        if not base:
            return None
        if type_muni == 0:
            folder_path = posixpath.join(folder, "Census")
        else:
            folder_path = posixpath.join(folder, "Census-" + _get_string_for_mesh(type_muni) )

        file_name = f"tbl{base}.txt"
        path = posixpath.join(folder_path, file_name)
        if os.path.exists(path):
            return file_name
        
        file_name_t = f"tblT{base}.txt"
        return file_name_t

    def get_attr_csv_fullpath(year, code_pref, code_muni, type_muni=0, folder="."):
        base = _get_base_filename(year, code_pref, code_muni, type_muni)
        if not base:
            return None
        if type_muni == 0:
            folder_path = posixpath.join(folder, "Census")
        else:
            folder_path = posixpath.join(folder, "Census-" + _get_string_for_mesh(type_muni) )

        file_name = f"tbl{base}.txt"
        
        path = posixpath.join(folder_path, file_name)
        
        if os.path.exists(path):
            return path
        
        file_name_t = f"tblT{base}.txt"
        path_t = posixpath.join(folder_path, file_name_t)
        
        if os.path.exists(path_t):
            return path_t

    def perform_join(folder, year, shp_name, csv_name):
        import os
        import posixpath
        import processing
        from qgis.core import (
            QgsVectorLayer,
            QgsVectorFileWriter,
            QgsCoordinateTransformContext,
        )
        from qgis.PyQt.QtCore import QUrl

        # 1. Path
        shp_path = (
            posixpath.join(folder, shp_name)
        )
        csv_path = (
            posixpath.join(folder, csv_name)
        )
        output_path = shp_path[:-4] + "-" + year + ".shp"

        # --- 2. CSV from CP932 (.txt) to UTF-8 (.csv) ---
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

        # --- 3. Create layer objects WITH ENCODING ---
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
