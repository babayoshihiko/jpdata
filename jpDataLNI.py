# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils


def getPrefsOrRegionsByMapCode(code_map):
    file_path = posixpath.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
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


def getYearsByMapCode(code_map, name_pref=None):
    file_path = posixpath.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
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
    file_path = posixpath.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
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
    file_path = posixpath.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
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


def getUrlCodeZipByPrefName(code_map, name_pref, year, detail=None):
    code_pref = jpDataUtils.getPrefCodeByName(name_pref)
    return getUrlCodeZipByPrefCode(code_map, code_pref, year, detail, name_pref)


def getUrlCodeZipByPrefCode(code_map, code_pref, year, detail=None, name_pref=None):
    if name_pref is None:
        name_pref = jpDataUtils.getPrefNameByCode(code_pref)
    file_path = posixpath.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
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
                if detail is None or detail == row["detail1"] + " " + row["detail2"]:
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
