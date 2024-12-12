# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils


def getPrefsOrRegionsByMapCode(code_map):
    file_path = posixpath.join(
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
    file_path = posixpath.join(
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

def getDetailsByMapCodePrefNameYear(code_map, name_pref, year):
    file_path = posixpath.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )
    details = []
    with open(file_path, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2 and row["availability"] == name_pref and row["year"] == year:
                details.append(row["detail1"] + ' ' + row["detail2"])
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
            if len(row) >= 2 and row["availability"] == name_pref and row["year"] == year and row["detail1"] + ' ' +  row["detail2"] == detail:
                details.append(row["shp"])
    unique_details = []
    for x in details:
        if x not in unique_details:
            unique_details.append(x)
    return unique_details

def getUrlCodeZipByPrefName(code_map, name_pref, year, detail = None):
    # name_pref = jpDataUtils.getPrefNameByCode(code_pref)
    file_path = posixpath.join(
        os.path.dirname(__file__), "csv", "LandNumInfo_" + code_map + ".csv"
    )

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
                if detail is None:
                    x["year"] = row["year"]
                    x["url"] = row["url"].replace("code_pref",code_pref)
                    x["zip"] = row["zip"].replace("code_pref",code_pref)
                    x["shp"] = row["shp"].replace("code_pref",code_pref)
                    x["altdir"] = row["altdir"].replace("code_pref",code_pref)
                elif detail == row["detail1"] + ' ' + row["detail2"]:
                    x["year"] = row["year"]
                    x["url"] = row["url"].replace("code_pref",code_pref)
                    x["zip"] = row["zip"].replace("code_pref",code_pref)
                    x["shp"] = row["shp"].replace("code_pref",code_pref)
                    x["altdir"] = row["altdir"].replace("code_pref",code_pref)
    return x

