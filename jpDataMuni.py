# -*- coding: utf-8 -*-

# from qgis.core import QgsMessageLog, Qgis
import os, csv

# The CSV contains the codes and names of prefs and munis in Japan
#
# code_dantai	code_region	code_pref	code_muni	name_pref	name_muni	name_muni_kana


def getMuniFromPrefCode(code_pref):
    filePath = os.path.join(os.path.dirname(__file__), "csv", "code_pref_muni.csv")
    filtered_rows = []
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2 and row["code_pref"] == code_pref:
                filtered_rows.append(row)
    return filtered_rows


def getMuniFromPrefName(name_pref):
    filePath = os.path.join(os.path.dirname(__file__), "csv", "code_pref_muni.csv")
    filtered_rows = []
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2 and row["name_pref"] == name_pref:
                filtered_rows.append(row)
    return filtered_rows


def getMesh1FromPrefName(name_muni):
    filePath = os.path.join(os.path.dirname(__file__), "csv", "muni_mesh1.csv")
    filtered_rows = []
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2 and row["name_muni"] == name_muni:
                filtered_rows.append(row)
    return filtered_rows


def getMesh3FromPrefName(name_muni):
    filePath = os.path.join(os.path.dirname(__file__), "csv", "muni_mesh3.csv")
    filtered_rows = []
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2 and row["name_muni"] == name_muni:
                filtered_rows.append(row)
    return filtered_rows


def getRowFromNames(name_pref, name_muni):
    filePath = os.path.join(os.path.dirname(__file__), "csv", "code_pref_muni.csv")
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if (
                len(row) >= 2
                and row["name_pref"] == name_pref
                and row["name_muni"] == name_muni
            ):
                if int(row["code_pref"]) < 10:
                    row["code_pref"] = "0" + row["code_pref"]
                return row


def get_all_designated_cities(year=2024):
    """Return all the designated cities"""
    year_int = int(year)
    # The current list as of 2026
    cities = {
        "札幌市", "仙台市", "千葉市", "さいたま市", "横浜市", "川崎市",
        "相模原市", "新潟市", "静岡市", "浜松市", "名古屋市", "京都市",
        "大阪市", "堺市", "神戸市", "岡山市", "広島市", "福岡市",
        "北九州市", "熊本市"
    }

    # Discard cities by
    if year_int < 2012:
        cities.discard("熊本市")
    if year_int < 2010:
        cities.discard("相模原市")
    if year_int < 2009:
        cities.discard("岡山市")

    return cities
