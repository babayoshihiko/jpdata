# -*- coding: utf-8 -*-

import os, posixpath, csv
from . import jpDataUtils

def getMesh1ByPrefName(name_pref):
    str_code_pref = jpDataUtils.getPrefCodeByName(name_pref)
    mesh1s = getMesh1ByPrefCode(str_code_pref)
    unique_mesh1s = []
    for x in mesh1s:
        if x["code_mesh1"] not in unique_mesh1s:
            unique_mesh1s.append(x["code_mesh1"])
    return unique_mesh1s

def getMesh1ByPrefCode(code_pref):
    int_code_pref = int(code_pref)
    tempMesh1 = []

    filePath = posixpath.join(os.path.dirname(__file__), "csv", "muni_mesh1.csv")
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)

    for row in rows:
         if int(row["code_pref"]) == int_code_pref:
              tempMesh1.append(row)
	
    return tempMesh1

def getMesh1ByPrefMuniCode(code_pref, code_muni):
    int_code_pref = int(code_pref)
    int_code_muni = int(code_muni)
    tempMesh3 = []
     
    filePath = posixpath.join(os.path.dirname(__file__), "csv", "muni_mesh1.csv")
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)

    for row in rows:
         if int(row["code_pref"]) == int_code_pref and int(row["code_muni"]) == int_code_muni:
              tempMesh3.append(row)

    return tempMesh3


def getMesh3ByPrefMuniCode(code_pref, code_muni):
    int_code_pref = int(code_pref)
    int_code_muni = int(code_muni)
    tempMesh3 = []
     
    filePath = posixpath.join(os.path.dirname(__file__), "csv", "muni_mesh3.csv")
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)

    for row in rows:
         if int(row["code_pref"]) == int_code_pref and int(row["code_muni"]) == int_code_muni:
              tempMesh3.append(row)

    return tempMesh3
