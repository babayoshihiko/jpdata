# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils


def getPrefsOrRegionsByMapCode(code_map, csvfile=None):
    if csvfile and csvfile.upper()[-3:] == "CSV" and len(csvfile) > 3:
        file_path = _get_csv_full_path(csvfile)
    else:
        file_path = _get_csv_full_path(code_map)
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
                                jpDataUtils.getPrefNameByCode(code_pref)
                            )
                else:
                    prefs_or_regions.append(row["availability"])
    unique_prefs_or_regions = []
    for x in prefs_or_regions:
        if x not in unique_prefs_or_regions:
            unique_prefs_or_regions.append(x)
    return unique_prefs_or_regions


def getYearsByMapCode(code_map, name_pref=None, csvfile=None):
    if csvfile.upper()[-3:] == "CSV" and len(csvfile) > 3:
        file_path = _get_csv_full_path(csvfile)
    else:
        file_path = _get_csv_full_path(code_map)
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


def getDetailsByMapCodePrefNameYear(code_map, name_pref, year):
    file_path = _get_csv_full_path(code_map)
    details = []
    with open(file_path, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if (
                len(row) >= 2
                and row["availability"] == name_pref
                and row["year"] == year
            ):
                details.append(row["detail1"] + " " + row["detail2"])
    unique_details = []
    for x in details:
        if x not in unique_details:
            unique_details.append(x)
    return unique_details


def getShapeByMapCodePrefNameYearDetail(code_map, name_pref, year, detail):
    file_path = _get_csv_full_path(code_map)
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


def getUrlCodeZipByPrefName(code_map, name_pref, year, detail=None, csvfile=None):
    code_pref = jpDataUtils.getPrefCodeByName(name_pref)
    return getUrlCodeZipByPrefCode(
        code_map, code_pref, year, detail, name_pref, csvfile
    )


def getUrlCodeZipByPrefCode(
    code_map, code_pref, year, detail=None, name_pref=None, csvfile=None
):
    if name_pref is None:
        name_pref = jpDataUtils.getPrefNameByCode(code_pref)
    file_path = ""
    if year.upper()[-3:] == "CSV":
        if csvfile is not None:
            file_path = _get_csv_full_path(csvfile)
        else:
            file_path = _get_csv_full_path(code_map)
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
                    x["url"] = row["url"].replace("code_pref", code_pref)
                    x["zip"] = row["zip"].replace("code_pref", code_pref)
                    x["shp"] = row["shp"].replace("code_pref", code_pref)
                    x["altdir"] = row["altdir"].replace("code_pref", code_pref)
                    if "qml" in row:
                        x["qml"] = row["qml"].replace("code_pref", code_pref)
                    if "epsg" in row:
                        x["epsg"] = row["epsg"]
                    if "encoding" in row:
                        x["encoding"] = row["encoding"]
                    break
    return x


def getZip(
    year, dict_lni_item, pref_name, code_pref_or_mesh1, type="urlzip", detail=None
):
    if not "code_map" in dict_lni_item:
        jpDataUtils.showError(
            "jpDataLNI.getZip",
            "The dictionary item does not contain 'code_map'.",
        )
        return None
    tempTypeMuni = dict_lni_item["type_muni"].lower()
    tempSubFolder = dict_lni_item["code_map"]
    tempUrl = dict_lni_item["url"]
    tempZip = dict_lni_item["zip"]
    tempShp = dict_lni_item["shp"]
    tempAltdir = dict_lni_item["altdir"]
    tempQml = dict_lni_item["qml"]
    tempEpsg = dict_lni_item["epsg"]
    tempEncoding = dict_lni_item["encoding"].upper()
    tempLayerName = dict_lni_item["name_j"] + " (" + pref_name + "," + year + ")"
    str_replace_before = "code_pref"

    if dict_lni_item["year"].upper()[-3:] == "CSV" and len(dict_lni_item["year"]) > 3:
        tempCsvFile = dict_lni_item["year"]
    else:
        tempCsvFile = None

    if tempTypeMuni == "mesh1":
        str_replace_before = "code_mesh1"
        tempLayerName = (
            dict_lni_item["name_j"] + " (" + code_pref_or_mesh1 + "," + year + ")"
        )

    dict_lni_item_from_csv = getUrlCodeZipByPrefName(
        dict_lni_item["code_map"], pref_name, year, detail, tempCsvFile
    )

    if dict_lni_item_from_csv:
        tempUrl = dict_lni_item_from_csv["url"].replace(
            str_replace_before, code_pref_or_mesh1
        )
        tempZip = dict_lni_item_from_csv["zip"].replace(
            str_replace_before, code_pref_or_mesh1
        )
        if "shp" in dict_lni_item_from_csv:
            tempShp = dict_lni_item_from_csv["shp"].replace(
                str_replace_before, code_pref_or_mesh1
            )
        if "altdir" in dict_lni_item_from_csv:
            tempAltdir = dict_lni_item_from_csv["altdir"].replace(
                str_replace_before, code_pref_or_mesh1
            )
        if "qml" in dict_lni_item_from_csv:
            tempQml = dict_lni_item_from_csv["qml"].replace(
                str_replace_before, code_pref_or_mesh1
            )
        if "epsg" in dict_lni_item_from_csv:
            tempEpsg = dict_lni_item_from_csv["epsg"]
        if "encoding" in dict_lni_item_from_csv:
            tempEncoding = dict_lni_item_from_csv["encoding"]
        if tempEncoding[:3] == "UTF":
            tempEncoding = "UTF-8"
        else:
            tempEncoding = "CP932"
    else:
        tempUrl = dict_lni_item["url"].replace(str_replace_before, code_pref_or_mesh1)
        tempZip = dict_lni_item["zip"].replace(str_replace_before, code_pref_or_mesh1)
        tempShp = dict_lni_item["shp"].replace(str_replace_before, code_pref_or_mesh1)

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


def _get_csv_full_path(arg1):
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
