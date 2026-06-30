# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils
from .jpdata_muni import jpDataMuni


class jpDataLNI:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.download_fullpath = ""
        self.lang = "j"
        self.records = None
        self.record = None
        self.source_csv = ""
        self.source = []
        self.current_name = ""
        self.prev_name = ""
        self.current_source_name = ""
        self._Muni = jpDataMuni.instance()
    
    def init(self):
        if self.records is None:
            self.load_records()

    def _clear_record(self):
        self.record = {
            "name_map":"",
            "code_map":"",
            "type_muni":"",
            "csv":"",
            "year":"",
            "name_pref":"",
            "code_pref":"",
            "name_muni":"",
            "code_muni":"",
            "code_mesh":"",
            "detail":"",
            "url":"",
            "zip":"",
            "shp":"",
            "altdir":"",
            "qml":"",
            "epsg":"",
            "encoding":"CP932",
            "download_fullpath":"",
            "subfolder":""
        }

    def set_download_folder(self, download_fullpath):
        self.download_fullpath = download_fullpath

    def set_lang(self, lang):
        self.lang = lang[:1].lower()

    def load_records(self):
        self.records = jpDataUtils.get_records_from_csv("LandNumInfo.csv", "name_" + self.lang)

    def set_record(self, name_map, year=None, name_pref=None, name_muni=None, code_mesh=None, detail=None):
        if name_map is None:
            jpDataUtils.printDebugLog("jpdata_lni.py: the argument name_map is None.")
            return
        self._clear_record()        
        self.record["name_map"] = name_map
        self.record["year"] = year
        self.record["name_pref"] = name_pref
        self.record["code_pref"] = jpDataUtils.getPrefCodeByName(name_pref) if name_pref is not None else ""
        self.record["name_muni"] = name_muni
        self.record["code_muni"] = self._Muni.get_code_muni(name_pref, name_muni)
        self.record["code_mesh"] = code_mesh
        self.record["detail"] = detail
        _record = self.records[name_map]
        self.record["code_map"] = _record["code_map"]
        self.record["type_muni"] = _record["type_muni"]
        self.record["csv"] = _record["year"] if _record["year"][-4:].upper() == ".CSV" else ""
        self.record["url"] = _record["url"]
        self.record["zip"] = _record["zip"]
        self.record["shp"] = _record["shp"]
        self.record["altdir"] = _record["altdir"]
        self.record["source"] = _record["source"]
        self.record["qml"] = _record["qml"]
        self.record["epsg"] = _record["epsg"]
        self.record["encoding"] = _record["encoding"]
        self.record["subfolder"] = self.record["code_map"]
        self.record["download_fullpath"] = posixpath.join(self.download_fullpath, self.record["subfolder"])
        self.prev_name = self.current_name
        self.current_name = name_map
        if self.record["csv"] != "":
            self._load_source(name_map)
            self._set_record_from_source()
        code_pref_or_mesh1 = self.record["code_pref"]
        if self.record["type_muni"] == "mesh1":
            code_pref_or_mesh1 = code_mesh
        self.record["url"] = jpDataUtils.replaceCodes(
            self.record["url"],
            code_map=self.record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=self.record["year"],
        )
        self.record["zip"] = jpDataUtils.replaceCodes(
            self.record["zip"],
            code_map=self.record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=self.record["year"],
        )
        self.record["shp"] = jpDataUtils.replaceCodes(
            self.record["shp"],
            code_map=self.record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=self.record["year"],
        )
        self.record["altdir"] = jpDataUtils.replaceCodes(
            self.record["altdir"],
            code_map=self.record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=self.record["year"],
        )
        self.record["qml"] = jpDataUtils.replaceCodes(
            self.record["qml"],
            code_map=self.record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=self.record["year"],
        )
        self.record["encoding"] = "UTF-8" if self.record["encoding"][:3] == "UTF" else "CP932"
    
    def _set_record_from_source(self):
        type_muni = self.record["type_muni"]
        for row in self.source:
            if row["year"] != self.record["year"]:
                continue
            if type_muni == "single" or type_muni == "all":
                break
            if type_muni == "detail" and row["detail1"] + " " + row["detail2"] == self.record["detail"]:
                break
            if type_muni == "regional" and "allprefs" == row["availability"] and (self.record["name_pref"] in jpDataUtils.PREF_NAMES["j"] or self.record["name_pref"] in jpDataUtils.PREF_NAMES["e"]): 
                break
            if type_muni == "regional" and self.record["name_pref"] == row["availability"]:
                break
            if type_muni == "mesh1":
                break
        self.record["url"] = row["url"]
        self.record["zip"] = row["zip"]
        self.record["shp"] = row["shp"]
        self.record["altdir"] = row["altdir"] if "altdir" in row else self.record["altdir"]
        self.record["qml"] = row["qml"] if "qml" in row else self.record["qml"]
        self.record["epsg"] = row["epsg"] if "encoding" in row else self.record["epsg"]
        self.record["encoding"] = row["encoding"] if "encoding" in row else self.record["encoding"]





    def get_record(self):
        return self.record

    def get_prev_name(self):
        return self.prev_name

    def get_records(self):
        return self.records
    
    def get_years(self, name_map, name_pref=None, csvfile=None):
        years = []
        csvfile = self.records[name_map].get("year", "")
        if csvfile.isdigit():
            years.append(csvfile)
            return years
        
        self._load_source(name_map)
        if name_pref is None:
            for row in self.source:
                years.append(row["year"])
        elif name_pref.replace("県", "") == "沖縄":
            for row in self.source:
                if 1971 < int(row["year"]) and (row["availability"] == name_pref or row["availability"] != "regional"):
                    years.append(row["year"])
        else:
            for row in self.source:
                if row["availability"] == name_pref or row["availability"] != "regional":
                    years.append(row["year"])
        return jpDataUtils.unique_list(years)

    def get_prefs(self, name_map):
        prefs_or_regions = []
        csvfile = self.records[name_map].get("year", "")
        if csvfile.isdigit():
            type_muni = self.records[name_map].get("type_muni","")
            if type_muni == "" or type_muni == "mesh1":
                for code_pref in range(1, 48):
                    prefs_or_regions.append(
                        jpDataUtils.getPrefNameByCode(code_pref, self.lang)
                    )
                return prefs_or_regions
            elif type_muni == "single":
                prefs_or_regions.append(TR.NATIONWIDE())
                return prefs_or_regions
        self._load_source(name_map)
        _allprefs = False
        for row in self.source:
            if row["availability"] == "allprefs":
                if _allprefs == False:
                    _allprefs = True
                    for code_pref in range(1, 48):
                        prefs_or_regions.append(
                            jpDataUtils.getPrefNameByCode(code_pref, self.lang)
                        )
            else:
                prefs_or_regions.append(row["availability"])
        return jpDataUtils.unique_list(prefs_or_regions)

    def get_details(self, name_map, year, name_pref):
        if self.records[name_map]["type_muni"] != "detail":
            return
        details = []
        self._load_source(name_map)
        for row in self.source:
            if row["year"] == year and row["availability"] == name_pref:
                details.append(row["detail1"] + " " + row["detail2"])
        return jpDataUtils.unique_list(details)


    def get_source(self, name_map=None):
        if name_map is not None:
            self._load_source(name_map)
        return self.source
    






    def _load_source(self, name_map):
        if name_map is None or self.current_source_name == name_map:
            return
        csv_full_path = ""
        csvfile = self.records[name_map].get("year", "")
        if csvfile.isdigit():
            return
        if csvfile.upper()[-4:] == ".CSV":
            csv_full_path = posixpath.join(os.path.dirname(__file__), "csv", csvfile)
        if not os.path.exists(csv_full_path):
            jpDataUtils.printLog(
                "jpdata_lni._load_source: Cannot find the CSV file for " + name_map + " " + csvfile,
            )
        else:
            self.source = jpDataUtils.get_records_from_csv(csv_full_path)
            self.current_source_name = name_map

