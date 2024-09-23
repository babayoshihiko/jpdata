# -*- coding: utf-8 -*-
import os, csv
from . import jpDataUtils

def getPrefsOrRegionsByMapCode(code_map):
    file_path = os.path.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
    prefs_or_regions = []
    with open(file_path, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2:
                prefs_or_regions.append(row["availability"])
    unique_prefs_or_regions = []
    for x in prefs_or_regions:
        if x not in unique_prefs_or_regions:
            unique_prefs_or_regions.append(x)
    return unique_prefs_or_regions


def getYearsByMapCode(code_map, name_pref=None):
    file_path = os.path.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
    years = []
    with open(file_path, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2 and name_pref is None:
                years.append(row["year"])
            elif len(row) >= 2 and row["availability"] == name_pref:
                years.append(row["year"])
    unique_years = []
    for x in years:
        if x not in unique_years:
            unique_years.append(x)
    return unique_years


def getUrlCodeZipByPrefName(code_map, name_pref, year):
    # name_pref = jpDataUtils.getPrefNameByCode(code_pref)
    file_path = os.path.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
    filtered_rows = []
    code_pref = jpDataUtils.getPrefCodeByName(name_pref)
    x = {
        "year": "",
        "url": "",
        "code_map": code_map,
        "zip": "",
        "shp": "",
        "altdir": "",
    }
    with open(file_path, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if (
                len(row) >= 2
                and row["availability"] == name_pref
                and row["year"] == year
            ):
                x["year"] = row["year"]
                x["url"] = row["url"].replace("code_pref",code_pref)
                x["zip"] = row["zip"].replace("code_pref",code_pref)
                x["shp"] = row["shp"].replace("code_pref",code_pref)
                x["altdir"] = row["altdir"].replace("code_pref",code_pref)
    return x

