# -*- coding: utf-8 -*-
import requests
import posixpath
import os.path
import zipfile
from qgis import processing
from . import jpDataUtils


def getSubFolder(type_muni):
    if type_muni == 0:
        tempSubFolder = "Census"
    if type_muni == 1:
        tempSubFolder = "Census-SDDSWS"
    elif type_muni == 2:
        tempSubFolder = "Census-HDDSWH"
    elif type_muni == 3:
        tempSubFolder = "Census-QDDSWQ"
    return tempSubFolder


def getZipShp(year, code_pref, code_muni, type_muni=0):
    tempZipFileName = getZipFileName(
        year,
        code_pref,
        code_muni,
        type_muni,
    )
    tempShpFileName = getShpFileName(
        year,
        code_pref,
        code_muni,
        type_muni,
    )
    return tempZipFileName, tempShpFileName


def getZip(year, code_pref, code_muni, type_muni=0):
    tempUrl = getUrl(year, code_pref, code_muni, type_muni)
    tempZip = getZipFileName(year, code_pref, code_muni, type_muni)
    tempSubFolder = getSubFolder(type_muni)
    return tempUrl, tempZip, tempSubFolder


def getUrl(year, code_pref, code_muni, type_muni=0):
    url = None
    if len(code_pref) == 1:
        code_pref = "0" + code_pref

    if type_muni == 0:
        if year == "2020" or year == "2015":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A00200521"
                + year
                + "&code="
                + code_pref
                + code_muni
                + "&coordSys=2&format=shape&downloadType=5&datum=2011"
            )
        else:
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A00200521"
                + year
                + "&code="
                + code_pref
                + code_muni
                + "&coordSys=2&format=shape&downloadType=5&datum=2000"
            )
    elif type_muni == 1:
        url = (
            "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=S&code="
            + code_muni
            + "&coordSys=1&format=shape&downloadType=5"
        )
    elif type_muni == 2:
        url = (
            "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=H&code="
            + code_muni
            + "&coordSys=1&format=shape&downloadType=5"
        )
    elif type_muni == 3:
        url = (
            "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=Q&code="
            + code_muni
            + "&coordSys=1&format=shape&downloadType=5"
        )
    return url


def getZipFileName(year, code_pref, code_muni, type_muni=0):
    zipFileName = None
    if type_muni == 0:
        if len(code_pref) == 1:
            code_pref = "0" + code_pref
        if year == "2020" or year == "2015":
            zipFileName = (
                "A00200521" + year + "XYSWC" + code_pref + code_muni + "-JGD2011.zip"
            )
        else:
            zipFileName = "A00200521" + year + "XYSWC" + code_pref + code_muni + ".zip"
    elif type_muni == 1:
        zipFileName = "SDDSWS" + code_muni + ".zip"
    elif type_muni == 2:
        zipFileName = "HDDSWH" + code_muni + ".zip"
    elif type_muni == 3:
        zipFileName = "QDDSWQ" + code_muni + ".zip"
    return zipFileName


def getShpFileName(year, code_pref, code_muni, type_muni=0):
    shpFileName = None
    if len(code_pref) == 1:
        code_pref = "0" + code_pref
    if type_muni == 0:
        if year == "2020":
            shpFileName = "r2ka" + code_pref + code_muni + ".shp"
        elif year == "2015":
            shpFileName = "h27ka" + code_pref + code_muni + ".shp"
        elif year == "2010":
            shpFileName = "h22ka" + code_pref + code_muni + ".shp"
        elif year == "2005":
            shpFileName = "h17ka" + code_pref + code_muni + ".shp"
        elif year == "2000":
            shpFileName = "h12ka" + code_pref + code_muni + ".shp"
    elif type_muni == 1:
        shpFileName = "MESH0" + code_muni + ".shp"
    elif type_muni == 2:
        shpFileName = "MESH0" + code_muni + ".shp"
    elif type_muni == 3:
        shpFileName = "MESH0" + code_muni + ".shp"
    return shpFileName


def getAttr(year, code_pref, code_muni, type_muni=0):
    tempUrl = getAttrUrl(year, code_pref, code_muni, type_muni)
    tempZip = getAttrZipFileName(year, code_pref, code_muni, type_muni)
    tempSubFolder = getSubFolder(type_muni)
    return tempUrl, tempZip, tempSubFolder


def getAttrUrl(year, code_pref, code_muni, type_muni=0):
    url = None

    if type_muni == 0:
        if len(code_pref) == 1:
            code_pref = "0" + code_pref
        if year == "2020":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T001082&code="
                + code_pref
                + "&downloadType=2"
            )
        elif year == "2015":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000849&code="
                + code_pref
                + "&downloadType=2"
            )
        elif year == "2010":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000573&code="
                + code_pref
                + "&downloadType=2"
            )
        elif year == "2005":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000051&code="
                + code_pref
                + "&downloadType=2"
            )
        elif year == "2000":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000002&code="
                + code_pref
                + "&downloadType=2"
            )
    elif type_muni == 1:
        if year == "2020":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T001140&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2015":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000846&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2010":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000608&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2005":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000148&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2000":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000146&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "1995":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000751&code="
                + code_muni
                + "&downloadType=2"
            )
    elif type_muni == 2:
        if year == "2020":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T001141&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2015":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000847&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2010":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000609&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2005":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000387&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2000":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000386&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "1995":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000752&code="
                + code_muni
                + "&downloadType=2"
            )
    elif type_muni == 3:
        if year == "2020":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T001142&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2015":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000876&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2010":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000649&code="
                + code_muni
                + "&downloadType=2"
            )
        elif year == "2005":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T000652&code="
                + code_muni
                + "&downloadType=2"
            )
    return url


def getAttrZipFileName(year, code_pref, code_muni, type_muni=0):
    zipFileName = None
    if type_muni == 0:
        if len(code_pref) == 1:
            code_pref = "0" + code_pref
        if year == "2020":
            zipFileName = "tblT001082C" + code_pref + ".zip"
        elif year == "2015":
            zipFileName = "tblT000849C" + code_pref + ".zip"
        elif year == "2010":
            zipFileName = "tblT000573C" + code_pref + ".zip"
        elif year == "2005":
            zipFileName = "tblT000051C" + code_pref + ".zip"
        elif year == "2000":
            zipFileName = "tblT000002C" + code_pref + ".zip"
    elif type_muni == 1:
        if year == "2020":
            zipFileName = "tblT001140S" + code_muni + ".zip"
        elif year == "2015":
            zipFileName = "tblT000846S" + code_muni + ".zip"
        elif year == "2010":
            zipFileName = "tblT000608S" + code_muni + ".zip"
        elif year == "2005":
            zipFileName = "tblT000148S" + code_muni + ".zip"
        elif year == "2000":
            zipFileName = "tblT000146S" + code_muni + ".zip"
        elif year == "1995":
            zipFileName = "tblT000751S" + code_muni + ".zip"
    elif type_muni == 2:
        if year == "2020":
            zipFileName = "tblT001141H" + code_muni + ".zip"
        elif year == "2015":
            zipFileName = "tblT000847H" + code_muni + ".zip"
        elif year == "2010":
            zipFileName = "tblT000609H" + code_muni + ".zip"
        elif year == "2005":
            zipFileName = "tblT000387H" + code_muni + ".zip"
        elif year == "2000":
            zipFileName = "tblT000386H" + code_muni + ".zip"
        elif year == "1995":
            zipFileName = "tblT000752H" + code_muni + ".zip"
    elif type_muni == 3:
        if year == "2020":
            zipFileName = "tblT001142Q" + code_muni + ".zip"
        elif year == "2015":
            zipFileName = "tblT000876Q" + code_muni + ".zip"
        elif year == "2010":
            zipFileName = "tblT000649Q" + code_muni + ".zip"
        elif year == "2005":
            zipFileName = "tblT000652Q" + code_muni + ".zip"
    return zipFileName


def getAttrCsvFileName(year, code_pref, code_muni, type_muni=0):
    csvFileName = None
    if type_muni == 0:
        if len(code_pref) == 1:
            code_pref = "0" + code_pref
        if year == "2020":
            csvFileName = "tblT001082C" + code_pref + ".txt"
        elif year == "2015":
            csvFileName = "tblT000849C" + code_pref + ".txt"
        elif year == "2010":
            csvFileName = "tblT000573C" + code_pref + ".txt"
        elif year == "2005":
            csvFileName = "tblT000051C" + code_pref + ".txt"
        elif year == "2000":
            csvFileName = "tblT000002C" + code_pref + ".txt"
    elif type_muni == 1:
        if year == "2020":
            csvFileName = "tblT001140S" + code_muni + ".txt"
        elif year == "2015":
            csvFileName = "tblT000846S" + code_muni + ".txt"
        elif year == "2010":
            csvFileName = "tblT000608S" + code_muni + ".txt"
        elif year == "2005":
            csvFileName = "tblT000148S" + code_muni + ".txt"
        elif year == "2000":
            csvFileName = "tblT000146S" + code_muni + ".txt"
        elif year == "1995":
            csvFileName = "tblT000751S" + code_muni + ".txt"
    elif type_muni == 2:
        if year == "2020":
            csvFileName = "tblT001141H" + code_muni + ".txt"
        elif year == "2015":
            csvFileName = "tblT000847H" + code_muni + ".txt"
        elif year == "2010":
            csvFileName = "tblT000609H" + code_muni + ".txt"
        elif year == "2005":
            csvFileName = "tblT000387H" + code_muni + ".txt"
        elif year == "2000":
            csvFileName = "tblT000386H" + code_muni + ".txt"
        elif year == "1995":
            csvFileName = "tblT000752H" + code_muni + ".txt"
    elif type_muni == 3:
        if year == "2020":
            csvFileName = "tblT001142Q" + code_muni + ".txt"
        elif year == "2015":
            csvFileName = "tblT000876Q" + code_muni + ".txt"
        elif year == "2010":
            csvFileName = "tblT000649Q" + code_muni + ".txt"
        elif year == "2005":
            csvFileName = "tblT000652Q" + code_muni + ".txt"
    return csvFileName


def downloadCsv(folder, year, code_pref, code_muni, type_muni=0):

    attrUrl = getAttrUrl(year, code_pref, code_muni, type_muni)
    attrZip = getAttrZipFileName(year, code_pref, code_muni, type_muni)
    attrCsv = getAttrCsvFileName(year, code_pref, code_muni, type_muni)
    if not os.path.exists(posixpath.join(folder, "Census")):
        os.makedirs(posixpath.join(folder, "Census"), exist_ok=True)
    if type_muni == 0:
        folder_path = posixpath.join(folder, "Census")
    elif type_muni == 1:
        folder_path = posixpath.join(folder, "Census", "SDDSWS")
    elif type_muni == 2:
        folder_path = posixpath.join(folder, "Census", "HDDSWH")
    elif type_muni == 3:
        folder_path = posixpath.join(folder, "Census", "QDDSWQ")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    urlData = requests.get(attrUrl).content
    with open(
        posixpath.join(folder_path, attrZip), mode="wb"
    ) as f:  # wb でバイト型を書き込める
        f.write(urlData)

    # Below is a workaround for a zip file with Japanese filenames/foldernames
    if os.path.exists(posixpath.join(folder_path, attrZip)):
        with zipfile.ZipFile(posixpath.join(folder_path, attrZip), "r") as zf:
            # Iterate through each file in the zip
            for zip_info in zf.infolist():
                # Extract the filename using the correct encoding
                # (e.g. 'cp932' for Japanese Windows)
                filename = zip_info.filename.encode("cp437").decode("cp932")
                # Construct the output file path
                output_file_path = posixpath.join(folder_path, filename)
                if zip_info.is_dir():
                    # Create directories if they do not exist
                    os.makedirs(output_file_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                    # Extract the file
                    with zf.open(zip_info) as file:
                        with open(output_file_path, "wb") as out_file:
                            out_file.write(file.read())


def performJoin(folder, year, shp, csv):
    encoding = "CP932"
    if not folder in shp:
        shp = posixpath.join(folder, shp)
    output = shp[:-4] + "-" + year + ".shp"
    if not folder in csv:
        csv = posixpath.join(folder, csv)
    if csv[-4:] == ".txt":
        if os.path.exists(csv[:-4] + ".csv"):
            csv = csv[:-4] + ".csv"
        else:
            if os.path.exists(csv):
                line_no = 0
                fout = open(csv[:-4] + ".csv", "w+", encoding="UTF-8")
                with open(csv, "r", encoding="CP932") as fp:
                    for line in fp:
                        line_no = line_no + 1
                        if line_no != 2:
                            fout.write(line.replace("*", ""))
                        else:
                            count = line.count(",")
                            if count <= 4:
                                csvt = "String"
                                minus = 0
                            else:
                                csvt = "String,Integer,String,String"
                                minus = 3
                            for _ in range(count - minus):
                                csvt += ",Integer"
                                fout2 = open(csv[:-4] + ".csvt", "w+", encoding="UTF-8")
                                fout2.write(csvt)
                                fout2.close()
                fout.close()
                csv = csv[:-4] + ".csv"
            else:
                return shp, encoding

    # Now all file names are full path

    if not os.path.exists(output):
        # See https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#join-attributes-by-field-value
        # Or type `processing.algorithmHelp("qgis:joinattributestable")`  in QGIS Python console.
        if os.path.exists(shp) and os.path.exists(csv):
            joinInfo = {
                "INPUT": shp,
                "FIELD": "KEY_CODE",
                "INPUT_2": csv,
                "FIELD_2": "KEY_CODE",
                "OUTPUT": output,
            }
            processing.run("qgis:joinattributestable", joinInfo)

    cfg = output[:-4] + ".cpg"
    encoding = "UTF-8"
    if os.path.exists(cfg):
        with open(cfg, "r") as fp:
            for line in fp:
                if "shift_jis" in line.lower():
                    encoding = "CP932"
                    break
                elif "utf-8" in line.lower():
                    break

    return output, encoding
