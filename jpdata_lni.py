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
        if self.prev_name != "" and self.prev_name != self.current_name:
            self.prev_name = self.current_name
            self.current_name = name

    def get_prev_name(self):
        return self.prev_name

    def get_records(self):
        return self.records
    
    def get_years(self, name_map, name_pref=None, csvfile=None):
        return self.getYearsByMapCode(name_map, name_pref, csvfile)

    def get_prefs(self, name_map, csvfile=None):
        return self.getPrefsOrRegionsByMapCode(name_map, csvfile)
    
    def get_shp(self, name_map, name_pref, year, detail):
        return self.getShapeByMapCodePrefNameYearDetail(name_map, name_pref, year, detail)
    
    def get_url_zip(self, name_map, year, pref_name, code_pref_mesh, detail=None):
        return self.getZip(
            name_map,
            year, 
            pref_name, 
            code_pref_mesh, 
            "urlzip", 
            detail)

    def get_zip_shp(self, name_map, year, pref_name, code_pref_mesh, detail=None):
        return self.getZip(
            name_map,
            year, 
            pref_name, 
            code_pref_mesh, 
            "zipshp", 
            detail)
    
    def get_details(self, name_map, name_pref, year):
        return self.getDetailsByMapCodePrefNameYear(name_map, name_pref, year)


    def getPrefsOrRegionsByMapCode(self, name_map, csvfile=None):
        prefs_or_regions = []
        csvfile = self.records[name_map].get("year")
        try:
            if csvfile is not None:
                # "type_muni" (record) == "availability" (source)
                # THIS PART OF THE METHOD should be shared?
                pref_or_region = self.records[name_map].get("type_muni",{})
                if pref_or_region == "allprefs":
                    for code_pref in range(1, 48):
                        prefs_or_regions.append(
                            jpDataUtils.getPrefNameByCode(code_pref, self.lang)
                        )
                else:
                    prefs_or_regions.append(pref_or_region)
                return prefs_or_regions
        except (ValueError, TypeError):
            pass
        
        self._set_source(name_map)
        _allprefs = False
        # This method DOES NOT translate
        # regional names defined in CSV files
        # but returns as are
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
        unique_prefs_or_regions = []
        for x in prefs_or_regions:
            if x not in unique_prefs_or_regions:
                unique_prefs_or_regions.append(x)
        return unique_prefs_or_regions


    def getYearsByMapCode(self, name_map, name_pref=None, csvfile=None):
        years = []
        csvfile = self.records[name_map].get("year", "")
        if csvfile.isdigit():
            years.append(csvfile)
        
        self._set_source(name_map)
        for row in self.source:
            if len(row) >= 2:
                if name_pref is None:
                    years.append(row["year"])
                elif row["availability"] == name_pref:
                    years.append(row["year"])
                elif (
                    row["availability"] == "allprefs"
                    and int("0" + jpDataUtils.getPrefCodeByName(name_pref)) >= 1
                    and int("0" + jpDataUtils.getPrefCodeByName(name_pref)) <= 46
                ):
                    years.append(row["year"])
                elif (
                    row["availability"] == "allprefs"
                    and name_pref.replace("県", "") == "沖縄"
                ):
                    if row["year"] not in ["1955", "1960", "1965", "1970"]:
                        # N03 ["1955","1960","1965","1970"]
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


    def getShapeByMapCodePrefNameYearDetail(self, name_map, name_pref, year, detail):
        self._set_source(name_map)
        details = []
        for row in self.source:
            if (
                len(row) >= 2
                and row["availability"] == name_pref
                and row["year"] == year
                and row["detail1"] + " " + row["detail2"] == detail
            ):
                details.append(row["shp"])
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
                pref_name, 
                code_pref_or_mesh1, 
                type="urlzip", 
                detail=None):
        record = self.records()[name_map]
        tempTypeMuni = record["type_muni"].lower()
        tempSubFolder = record["code_map"]

        tempUrl = record["url"]
        tempZip = record["zip"]
        tempShp = record["shp"]
        tempAltdir = record["altdir"]
        tempQml = record["qml"]
        tempEpsg = record["epsg"]
        tempEncoding = record["encoding"].upper()
        tempLayerName = record["name_" + self.lang] + " (" + pref_name + "," + year + ")"

        if self.current_name != name_map:
            self._set_source(record["year"])
            # Read data from CSV
            tempUrl = self.source["url"]
            tempZip = self.source["zip"]
            tempShp = self.source["shp"]
            if "altdir" in self.source:
                tempAltdir = self.source["altdir"]
            if "qml" in self.source:
                tempQml = self.source["qml"]
            if "epsg" in self.source:
                tempEpsg = self.source["epsg"]
            if "encoding" in self.source:
                tempEncoding = self.source["encoding"]


        if tempTypeMuni == "mesh1":
            tempLayerName = (
                record["name_" + self.lang] + " (" + code_pref_or_mesh1 + "," + year + ")"
            )
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
                "jpDataLNI._get_csv_full_path: "
                + "The CSV file does not exist: "
                + csv_full_path,
            )
        self.source_csv = csv_full_path
        return csv_full_path

    def _set_source(self, name_map):
        if self.current_name == name_map:
            return
        csv_full_path = ""
        csvfile = self.records[name_map]["year"]
        if csvfile.upper()[-3:] == "CSV" and len(csvfile) > 3:
            csv_full_path = posixpath.join(os.path.dirname(__file__), "csv", csvfile)
        if not os.path.exists(csv_full_path):
            jpDataUtils.printLog(
                "jpdata_lni._set_source: "
                + "The CSV file does not exist: "
                + name_map,
            )
        else:
            self.source = jpDataUtils.get_records_from_csv(csv_full_path)
            self.prev_name = self.current_name
            self.current_name = name_map
