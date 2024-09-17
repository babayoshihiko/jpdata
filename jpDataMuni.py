# -*- coding: utf-8 -*-

from qgis.core import QgsMessageLog, Qgis
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
