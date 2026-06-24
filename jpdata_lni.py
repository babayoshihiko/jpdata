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

    def __init__(self, download_fullpath, lang="j"):
        self.download_fullpath = ""
        self.set_download_folder(download_fullpath)
        self.source_csv = ""
        self.lang = lang
        self.records = []
        self.prev_name = ""
        self.current_name = ""
    
    def set_download_folder(self, download_fullpath):
        self.download_fullpath = download_fullpath

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
    
    def get_years(self, code_map, name_pref=None, csvfile=None):
        return self.getYearsByMapCode(code_map, name_pref, csvfile)

    def get_prefs(self, code_map, csvfile=None):
        return self.getPrefsOrRegionsByMapCode(code_map, csvfile)
    
    def get_shp(self, code_map, name_pref, year, detail):
        return self.getShapeByMapCodePrefNameYearDetail(code_map, name_pref, year, detail)
    
    def get_zip(self, code_map, name_pref, code_pref_mesh, detail=None, type="urlzip"):
        return self.getZip(
            year, 
            pref_name, 
            code_pref_or_mesh1, 
            type="urlzip", 
            detail=None,
            lang="ja"
        )




    def getPrefsOrRegionsByMapCode(self, code_map, csvfile):
        if csvfile and csvfile.upper()[-3:] == "CSV" and len(csvfile) > 3:
            file_path = self._get_csv_full_path(csvfile)
        else:
            file_path = self._get_csv_full_path(code_map)
        prefs_or_regions = []
        _allprefs = False
        with open(file_path, "r") as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
                if len(row) >= 2:
                    if row["availability"] == "allprefs":
                        if _allprefs == False:
                            _allprefs = True
                            for code_pref in range(1, 48):
                                prefs_or_regions.append(
                                    jpDataUtils.getPrefNameByCode(code_pref, lang)
                                )
                    else:
                        prefs_or_regions.append(row["availability"])
        unique_prefs_or_regions = []
        for x in prefs_or_regions:
            if x not in unique_prefs_or_regions:
                unique_prefs_or_regions.append(x)
        return unique_prefs_or_regions


    def getYearsByMapCode(self, code_map, name_pref=None, csvfile=None):
        try:
            if csvfile is None:
                return []
            years = [int(csvfile)]
            return years
        except (ValueError, TypeError):
            return []
        if csvfile.upper()[-3:] == "CSV" and len(csvfile) > 3:
            file_path = self._get_csv_full_path(csvfile)
        else:
            file_path = self._get_csv_full_path(code_map)
        years = []
        with open(file_path, "r") as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
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


    def getDetailsByMapCodePrefNameYear(self, code_map, name_pref, year):
        file_path = self._get_csv_full_path(code_map)
        details = []
        with open(file_path, "r") as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
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


    def getShapeByMapCodePrefNameYearDetail(self, code_map, name_pref, year, detail):
        file_path = self._get_csv_full_path(code_map)
        details = []
        with open(file_path, "r") as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
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


    def _get_url_by_pref_name(self, code_map, name_pref, year, detail=None, csvfile=None, lang="j"):
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        return self._get_url_by_pref_code(code_map, code_pref, year, detail, name_pref, csvfile, lang)


    def _get_url_by_pref_code(
        self, code_map, code_pref, year, detail=None, name_pref=None, csvfile=None, lang="j"
    ):
        if name_pref is None:
            name_pref = jpDataUtils.getPrefNameByCode(code_pref, lang)
        file_path = ""
        if csvfile is not None:
            file_path = self._get_csv_full_path(csvfile)
        else:
            file_path = self._get_csv_full_path(code_map)
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


    def getZip(
        self,
        year, 
        pref_name, 
        code_pref_or_mesh1, 
        type="urlzip", 
        detail=None,
        lang="ja"
    ):
        if not "code_map" in self.records:
            jpDataUtils.showError(
                "jpDataLNI.getZip",
                "The dictionary item does not contain 'code_map'.",
            )
            return None
        tempTypeMuni = self.records["type_muni"].lower()
        tempSubFolder = self.records["code_map"]
        tempUrl = self.records["url"]
        tempZip = self.records["zip"]
        tempShp = self.records["shp"]
        tempAltdir = self.records["altdir"]
        tempQml = self.records["qml"]
        tempEpsg = self.records["epsg"]
        tempEncoding = self.records["encoding"].upper()
        tempLayerName = self.records["name_" + lang] + " (" + pref_name + "," + year + ")"

        if self.records["year"].upper()[-3:] == "CSV" and len(self.records["year"]) > 3:
            tempCsvFile = self.records["year"]
            records_from_csv = self._get_url_by_pref_name(
                self.records["code_map"], pref_name, year, detail, tempCsvFile, lang
            )
        else:
            tempCsvFile = None
            records_from_csv = None


        if tempTypeMuni == "mesh1":
            tempLayerName = (
                self.records["name_" + lang] + " (" + code_pref_or_mesh1 + "," + year + ")"
            )
        if records_from_csv:
            # Read data from CSV
            tempUrl = records_from_csv["url"]
            tempZip = records_from_csv["zip"]
            tempShp = records_from_csv["shp"]
            if "altdir" in records_from_csv:
                tempAltdir = records_from_csv["altdir"]
            if "qml" in records_from_csv:
                tempQml = records_from_csv["qml"]
            if "epsg" in records_from_csv:
                tempEpsg = records_from_csv["epsg"]
            if "encoding" in records_from_csv:
                tempEncoding = records_from_csv["encoding"]
            if tempEncoding[:3] == "UTF":
                tempEncoding = "UTF-8"
            else:
                tempEncoding = "CP932"

        tempUrl = jpDataUtils.replaceCodes(
            tempUrl,
            code_map=self.records["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        tempZip = jpDataUtils.replaceCodes(
            tempZip,
            code_map=self.records["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        tempShp = jpDataUtils.replaceCodes(
            tempShp,
            code_map=self.records["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        tempAltdir = jpDataUtils.replaceCodes(
            tempAltdir,
            code_map=self.records["code_map"],
            code_pref_or_mesh1=code_pref_or_mesh1,
            year=year,
        )
        tempQml = jpDataUtils.replaceCodes(
            tempQml,
            code_map=self.records["code_map"],
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


    def _get_csv_full_path(self, arg1):
        if arg1.upper() == "CSV":
            jpDataUtils.printLog(
                "jpDataLNI._get_csv_full_path: "
                + "Wrong argument, expected a map code or CSV file name, not 'CSV'. "
                + arg1
            )
            return None

        csv_full_path = ""
        if arg1.upper()[-3:] == "CSV" and len(arg1) > 3:
            # If the arg1 is CSV, we use it
            csv_full_path = posixpath.join(os.path.dirname(__file__), "csv", arg1)
        if not os.path.exists(csv_full_path):
            csv_full_path = posixpath.join(
                os.path.dirname(__file__), "csv", "LandNumInfo_" + arg1 + ".csv"
            )
        if not os.path.exists(csv_full_path):
            jpDataUtils.printLog(
                "jpDataLNI._get_csv_full_path: "
                + "The CSV file does not exist: "
                + csv_full_path,
            )
        return csv_full_path
