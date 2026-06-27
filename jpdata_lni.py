# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils


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
        self.source_csv = ""
        self.source = []
        self.prev_name = ""
        self.current_name = ""
    
    def init(self):
        if self.records is None:
            self.load_records()

    def set_download_folder(self, download_fullpath):
        self.download_fullpath = download_fullpath

    def set_lang(self, lang):
        self.lang = lang[:1].lower()

    def load_records(self):
        self.records = jpDataUtils.get_records_from_csv("LandNumInfo.csv", "name_" + self.lang)

    def set_name(self, name):
        if name is None:
            jpDataUtils.printLog("jpdata_lni.py: the argument name is None.")
        self._set_source(name)

    def get_prev_name(self):
        return self.prev_name

    def get_records(self):
        return self.records
    
    def get_record(self, name_map):
        return self.records[name_map]
    
    def get_years(self, name_map, name_pref=None, csvfile=None):
        return self.getYearsByMapCode(name_map, name_pref, csvfile)

    def get_prefs(self, name_map, csvfile=None):
        return self.getPrefsOrRegionsByMapCode(name_map, csvfile)
    
    def get_source(self, name_map=None):
        if name_map is not None:
            self._set_source(name_map)
        return self.source
    
    def get_url_zip(self, name_map, year, name_pref_mesh, detail=None):
        return self.getZip(
            name_map,
            year, 
            name_pref_mesh, 
            "urlzip", 
            detail)

    def get_zip_shp(self, name_map, year, name_pref_mesh, detail=None):
        return self.getZip(
            name_map,
            year, 
            name_pref_mesh, 
            "zipshp", 
            detail)
    
    def get_details(self, name_map, name_pref, year):
        return self.getDetailsByMapCodePrefNameYear(name_map, name_pref, year)


    def getPrefsOrRegionsByMapCode(self, name_map, csvfile=None):
        prefs_or_regions = []
        csvfile = self.records[name_map].get("year", "")

        pref_or_region = self.records[name_map].get("type_muni","")
        if pref_or_region == "allprefs" or pref_or_region == "" or pref_or_region == "mesh1":
            for code_pref in range(1, 48):
                prefs_or_regions.append(
                    jpDataUtils.getPrefNameByCode(code_pref, self.lang)
                )
            return prefs_or_regions
        elif pref_or_region == "single" or pref_or_region == "Nation-wide":
            prefs_or_regions.append(TR.NATIONWIDE())
            return prefs_or_regions

        # pref_or_region == "regional" OR "detail"
        # This method DOES NOT translate
        # regional names defined in CSV files
        # but returns as are
        self._set_source(name_map)
        _allprefs = False
        for row in self.source:
            if len(row) >= 2:
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


    def getYearsByMapCode(self, name_map, name_pref=None, csvfile=None):
        years = []
        csvfile = self.records[name_map].get("year", "")
        if csvfile.isdigit():
            years.append(csvfile)
            return years
        
        self._set_source(name_map)
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

        unique_years = []
        for x in years:
            if x not in unique_years:
                unique_years.append(x)
        return unique_years


    def getDetailsByMapCodePrefNameYear(self, name_map, name_pref, year):
        self._set_source(name_map)
        details = []
        for row in self.source:
            if (
                len(row) >= 2
                and (
                    row["availability"] == name_pref
                    or row["availability"] == "allprefs"
                )
                and row["year"] == year
            ):
                details.append(row["detail1"] + " " + row["detail2"])
        unique_details = []
        for x in details:
            if x not in unique_details:
                unique_details.append(x)
        return unique_details


    def _get_url_by_pref_name(self, code_map, name_pref, year, detail=None, csvfile=None):
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        return self._get_url_by_pref_code(code_map, code_pref, year, detail, name_pref, csvfile)


    def _get_url_by_pref_code(
        self, code_map, code_pref, year, detail=None, name_pref=None, csvfile=None):
        if name_pref is None:
            name_pref = jpDataUtils.getPrefNameByCode(code_pref, self.lang)
        file_path = ""
        if csvfile is not None:
            file_path = self._get_csv_full_path(csvfile)
        if not os.path.exists(file_path):
            return None
        x = {
            "year": "",
            "url": "",
            "code_map": code_map,
            "zip": "",
            "shp": "",
            "altdir": "",
            "qml": "",
            "epsg": "",
            "encoding": "",
        }
        with open(file_path, "r") as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
                if (
                    len(row) >= 2
                    and row["year"] == year
                    and (
                        row["availability"] == name_pref
                        or (
                            row["availability"] == "allprefs"
                            and int("0" + jpDataUtils.getPrefCodeByName(name_pref)) >= 1
                            and int("0" + jpDataUtils.getPrefCodeByName(name_pref)) <= 47
                        )
                        or row["availability"] == "all"
                    )
                ):
                    overwrite = False
                    if detail is None:
                        overwrite = True
                    if "detail1" in row and "detail2" in row:
                        if detail == row["detail1"] + " " + row["detail2"]:
                            overwrite = True
                    if overwrite:
                        x["year"] = row["year"]
                        x["url"] = row["url"]
                        x["zip"] = row["zip"]
                        x["shp"] = row["shp"]
                        if "altdir" in row:
                            x["altdir"] = row["altdir"]
                        if "qml" in row:
                            # x["qml"] = row["qml"].replace("code_pref", code_pref)
                            x["qml"] = jpDataUtils.replaceCodes(
                                row["qml"],
                                code_map=code_map,
                                code_pref_or_mesh1=code_pref,
                                year=year,
                            )

                        if "epsg" in row:
                            x["epsg"] = row["epsg"]
                        if "encoding" in row:
                            x["encoding"] = row["encoding"]
                        break
        return x


    def getZip( self,
                name_map,
                year, 
                name_pref_mesh, 
                type="urlzip", 
                detail=None):
        record = self.records[name_map]
        if record["type_muni"] == "detail" and detail is None:
            return
        tempTypeMuni = record["type_muni"].lower()
        tempSubFolder = record["code_map"]

        tempUrl = record["url"]
        tempZip = record["zip"]
        tempShp = record["shp"]
        tempAltdir = record["altdir"]
        tempQml = record["qml"]
        tempEpsg = record["epsg"]
        tempEncoding = record["encoding"].upper()
        tempLayerName = record["name_" + self.lang] + " (" + name_pref_mesh + "," + year + ")"
        if (not record["year"].isdigit()) or record["year"][:3].upper() == "CSV":
            self._set_source(name_map)
            # Read data from CSV
            for row in self.source:
                if row["year"] != year:
                    continue
                if tempTypeMuni != "single" and row["availability"] != name_pref_mesh and row["availability"] != "allprefs" and row["availability"] != "all":
                    continue
                if tempTypeMuni == "detail" and row["detail1"] + " " + row["detail1"] != detail:
                    continue

                tempUrl = row["url"]
                tempZip = row["zip"]
                tempShp = row["shp"]
                if "altdir" in row:
                    tempAltdir = row["altdir"]
                if "qml" in row:
                    tempQml = row["qml"]
                if "epsg" in row:
                    tempEpsg = row["epsg"]
                if "encoding" in row:
                    tempEncoding = row["encoding"]

        code_pref_or_mesh1 = jpDataUtils.getPrefCodeByName(name_pref_mesh)
        if tempTypeMuni == "mesh1":
            tempLayerName = (
                record["name_" + self.lang] + " (" + name_pref_mesh + "," + year + ")"
            )
            code_pref_or_mesh1 = name_pref_mesh
        if tempEncoding[:3] == "UTF":
            tempEncoding = "UTF-8"
        else:
            tempEncoding = "CP932"

        tempUrl = jpDataUtils.replaceCodes(
            tempUrl,
            code_map=record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        tempZip = jpDataUtils.replaceCodes(
            tempZip,
            code_map=record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        tempShp = jpDataUtils.replaceCodes(
            tempShp,
            code_map=record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        tempAltdir = jpDataUtils.replaceCodes(
            tempAltdir,
            code_map=record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        tempQml = jpDataUtils.replaceCodes(
            tempQml,
            code_map=record["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        if type == "urlzip":
            return tempUrl, tempZip, tempSubFolder
        else:
            return (
                tempZip,
                tempShp,
                tempAltdir,
                tempQml,
                tempEpsg,
                tempEncoding,
                tempSubFolder,
                tempLayerName,
            )


    def _get_csv_full_path(self, csvfile):
        csv_full_path = ""
        if csvfile.upper()[-3:] == "CSV" and len(csvfile) > 3:
            csv_full_path = posixpath.join(os.path.dirname(__file__), "csv", csvfile)
        if not os.path.exists(csv_full_path):
            jpDataUtils.printLog(
                "jpdata_lni._get_csv_full_path: "
                + "The CSV file does not exist: "
                + csv_full_path,
            )
            return
        self.source_csv = csv_full_path
        return csv_full_path

    def _set_source(self, name_map):
        if name_map is None or self.current_name == name_map:
            return
        csv_full_path = ""
        csvfile = self.records[name_map].get("year", "")
        if csvfile.isdigit():
            return
        if csvfile.upper()[-3:] == "CSV" and len(csvfile) > 3:
            csv_full_path = posixpath.join(os.path.dirname(__file__), "csv", csvfile)
        if not os.path.exists(csv_full_path):
            jpDataUtils.printLog(
                "jpdata_lni._set_source: Cannot find the CSV file for " + name_map + " " + csvfile,
            )
        else:
            self.prev_name = self.current_name
            self.current_name = name_map
            self.source = jpDataUtils.get_records_from_csv(csv_full_path)

