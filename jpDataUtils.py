# -*- coding: utf-8 -*-
from qgis.core import QgsMessageLog, Qgis, QgsCoordinateReferenceSystem
from qgis.core import QgsVectorLayer
import os, csv, posixpath
import zipfile


def getYearAs(year, format="year2digit"):
    """year4digit = '2023'
    year2digit = '23'
    yearJP = 'R5'
    yearJP2digit = '05'
    """
    year_as = ""
    if format == "year4digit":
        year_as = str(year)
    elif format == "year2digit":
        year_as = str(year)[2:4]
    elif format == "yearJP":
        if int(year) - 2018 > 0:
            year_as = "R" + str(int(year) - 2018)
        elif int(year) - 1998 > 0:
            year_as = "H" + str(int(year) - 1988)
        else:
            year_as = "H" + str(int(year) - 1925)
    elif format == "yearJP2digit":
        if int(year) - 2018 > 0:
            year_as = str(int(year) - 2018).zfill(2)
        elif int(year) - 1998 > 0:
            year_as = str(int(year) - 1988).zfill(2)
        else:
            year_as = str(int(year) - 1925).zfill(2)
    return year_as


def getPrefNameByCode(pref_code):
    pref_name = ""
    if pref_code == 1:
        pref_name = "北海道"
    elif pref_code == 2:
        pref_name = "青森県"
    elif pref_code == 3:
        pref_name = "岩手県"
    elif pref_code == 4:
        pref_name = "宮城県"
    elif pref_code == 5:
        pref_name = "秋田県"
    elif pref_code == 6:
        pref_name = "山形県"
    elif pref_code == 7:
        pref_name = "福島県"
    elif pref_code == 8:
        pref_name = "茨城県"
    elif pref_code == 9:
        pref_name = "栃木県"
    elif pref_code == 10:
        pref_name = "群馬県"
    elif pref_code == 11:
        pref_name = "埼玉県"
    elif pref_code == 12:
        pref_name = "千葉県"
    elif pref_code == 13:
        pref_name = "東京都"
    elif pref_code == 14:
        pref_name = "神奈川県"
    elif pref_code == 15:
        pref_name = "新潟県"
    elif pref_code == 16:
        pref_name = "富山県"
    elif pref_code == 17:
        pref_name = "石川県"
    elif pref_code == 18:
        pref_name = "福井県"
    elif pref_code == 19:
        pref_name = "山梨県"
    elif pref_code == 20:
        pref_name = "長野県"
    elif pref_code == 21:
        pref_name = "岐阜県"
    elif pref_code == 22:
        pref_name = "静岡県"
    elif pref_code == 23:
        pref_name = "愛知県"
    elif pref_code == 24:
        pref_name = "三重県"
    elif pref_code == 25:
        pref_name = "滋賀県"
    elif pref_code == 26:
        pref_name = "京都府"
    elif pref_code == 27:
        pref_name = "大阪府"
    elif pref_code == 28:
        pref_name = "兵庫県"
    elif pref_code == 29:
        pref_name = "奈良県"
    elif pref_code == 30:
        pref_name = "和歌山県"
    elif pref_code == 31:
        pref_name = "鳥取県"
    elif pref_code == 32:
        pref_name = "島根県"
    elif pref_code == 33:
        pref_name = "岡山県"
    elif pref_code == 34:
        pref_name = "広島県"
    elif pref_code == 35:
        pref_name = "山口県"
    elif pref_code == 36:
        pref_name = "徳島県"
    elif pref_code == 37:
        pref_name = "香川県"
    elif pref_code == 38:
        pref_name = "愛媛県"
    elif pref_code == 39:
        pref_name = "高知県"
    elif pref_code == 40:
        pref_name = "福岡県"
    elif pref_code == 41:
        pref_name = "佐賀県"
    elif pref_code == 42:
        pref_name = "長崎県"
    elif pref_code == 43:
        pref_name = "熊本県"
    elif pref_code == 44:
        pref_name = "大分県"
    elif pref_code == 45:
        pref_name = "宮崎県"
    elif pref_code == 46:
        pref_name = "鹿児島県"
    elif pref_code == 47:
        pref_name = "沖縄県"
    elif pref_code == 52:
        pref_name = "東北地方"
    elif pref_code == 53:
        pref_name = "関東地方"
    elif pref_code == 54:
        pref_name = "甲信越・北陸地方"
    elif pref_code == 55:
        pref_name = "東海地方"
    elif pref_code == 56:
        pref_name = "近畿地方"
    elif pref_code == 57:
        pref_name = "中国地方"
    elif pref_code == 58:
        pref_name = "四国地方"
    elif pref_code == 59:
        pref_name = "九州地方"
    elif pref_code == 81:
        pref_name = "北海道開発局"
    elif pref_code == 82:
        pref_name = "東北地方整備局"
    elif pref_code == 83:
        pref_name = "関東地方整備局"
    elif pref_code == 84:
        pref_name = "北陸地方整備局"
    elif pref_code == 85:
        pref_name = "中部地方整備局"
    elif pref_code == 86:
        pref_name = "近畿地方整備局"
    elif pref_code == 87:
        pref_name = "中国地方整備局"
    elif pref_code == 88:
        pref_name = "四国地方整備局"
    elif pref_code == 89:
        pref_name = "九州地方整備局"

    return pref_name


def getPrefCodeByName(pref_name):
    pref_code = ""
    pref_name = pref_name.strip()
    pref_name = pref_name.replace("県", "")
    if pref_name == "北海道":
        pref_code = "01"
    elif pref_name == "青森":
        pref_code = "02"
    elif pref_name == "岩手":
        pref_code = "03"
    elif pref_name == "宮城":
        pref_code = "04"
    elif pref_name == "秋田":
        pref_code = "05"
    elif pref_name == "山形":
        pref_code = "06"
    elif pref_name == "福島":
        pref_code = "07"
    elif pref_name == "茨城":
        pref_code = "08"
    elif pref_name == "栃木":
        pref_code = "09"
    elif pref_name == "群馬":
        pref_code = "10"
    elif pref_name == "埼玉":
        pref_code = "11"
    elif pref_name == "千葉":
        pref_code = "12"
    elif pref_name == "東京都" or pref_name == "東京":
        pref_code = "13"
    elif pref_name == "神奈川":
        pref_code = "14"
    elif pref_name == "新潟":
        pref_code = "15"
    elif pref_name == "富山":
        pref_code = "16"
    elif pref_name == "石川":
        pref_code = "17"
    elif pref_name == "福井":
        pref_code = "18"
    elif pref_name == "山梨":
        pref_code = "19"
    elif pref_name == "長野":
        pref_code = "20"
    elif pref_name == "岐阜":
        pref_code = "21"
    elif pref_name == "静岡":
        pref_code = "22"
    elif pref_name == "愛知":
        pref_code = "23"
    elif pref_name == "三重":
        pref_code = "24"
    elif pref_name == "滋賀":
        pref_code = "25"
    elif pref_name == "京都府" or pref_name == "京都":
        pref_code = "26"
    elif pref_name == "大阪府" or pref_name == "大阪":
        pref_code = "27"
    elif pref_name == "兵庫":
        pref_code = "28"
    elif pref_name == "奈良":
        pref_code = "29"
    elif pref_name == "和歌山":
        pref_code = "30"
    elif pref_name == "鳥取":
        pref_code = "31"
    elif pref_name == "島根":
        pref_code = "32"
    elif pref_name == "岡山":
        pref_code = "33"
    elif pref_name == "広島":
        pref_code = "34"
    elif pref_name == "山口":
        pref_code = "35"
    elif pref_name == "徳島":
        pref_code = "36"
    elif pref_name == "香川":
        pref_code = "37"
    elif pref_name == "愛媛":
        pref_code = "38"
    elif pref_name == "高知":
        pref_code = "39"
    elif pref_name == "福岡":
        pref_code = "40"
    elif pref_name == "佐賀":
        pref_code = "41"
    elif pref_name == "長崎":
        pref_code = "42"
    elif pref_name == "熊本":
        pref_code = "43"
    elif pref_name == "大分":
        pref_code = "44"
    elif pref_name == "宮崎":
        pref_code = "45"
    elif pref_name == "鹿児島":
        pref_code = "46"
    elif pref_name == "沖縄":
        pref_code = "47"
    elif pref_name == "東北地方":
        pref_code = "52"
    elif pref_name == "関東地方":
        pref_code = "53"
    elif pref_name == "甲信越・北陸地方":
        pref_code = "54"
    elif pref_name == "東海地方":
        pref_code = "55"
    elif pref_name == "近畿地方":
        pref_code = "56"
    elif pref_name == "中国地方":
        pref_code = "57"
    elif pref_name == "四国地方":
        pref_code = "58"
    elif pref_name == "九州地方":
        pref_code = "59"
    elif pref_name == "北海道開発局":
        pref_code = "81"
    elif pref_name == "東北地方整備局":
        pref_code = "82"
    elif pref_name == "関東地方整備局":
        pref_code = "83"
    elif pref_name == "北陸地方整備局":
        pref_code = "84"
    elif pref_name == "中部地方整備局":
        pref_code = "85"
    elif pref_name == "近畿地方整備局":
        pref_code = "86"
    elif pref_name == "中国地方整備局":
        pref_code = "87"
    elif pref_name == "四国地方整備局":
        pref_code = "88"
    elif pref_name == "九州地方整備局":
        pref_code = "89"

    return pref_code


# def getMapsFromCsv():
#     filePath = posixpath.join(os.path.dirname(__file__), "csv", "LandNumInfo.csv")
#     with open(filePath, "r") as f:
#         csvreader = csv.DictReader(f)
#         rows = list(csvreader)
#         return rows


# def getMapsFromCsv2():
#     filePath = posixpath.join(os.path.dirname(__file__), "csv", "LandNumInfo.csv")
#     new_dict = dict()
#
#     with open(filePath, "r") as f:
#         csvreader = csv.DictReader(f)
#         for row in csvreader:
#             new_dict.update({row["name_j"]: row})
#     return new_dict


def getMapsFromCsv2():
    filePath = posixpath.join(os.path.dirname(__file__), "csv", "LandNumInfo.csv")
    new_dict = {}

    with open(filePath, "r", encoding="utf-8") as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            key = row.get("name_j")
            if key:  # only add if key exists
                new_dict[key] = row
    return new_dict


def getTilesFromCsv():
    filePath = posixpath.join(os.path.dirname(__file__), "csv", "GSI.csv")
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)
        return rows


def findShpFile2(folderPath, shp, altdir, code_pref, code_muni="", name_muni=""):
    shpFile = None
    shpFileTarget = replaceCodes(
        shp,
        code_pref_or_mesh1=code_pref,
        code_muni=code_muni,
        name_muni=name_muni,
    )
    altDir = replaceCodes(
        altdir, code_pref_or_mesh1=code_pref, code_muni=code_muni, name_muni=name_muni
    )
    if os.path.exists(posixpath.join(folderPath, shpFileTarget)):
        shpFile = posixpath.join(folderPath, shpFileTarget)
    elif os.path.exists(posixpath.join(folderPath, altDir, shpFileTarget)):
        shpFile = posixpath.join(folderPath, altDir, shpFileTarget)
        printLog("jpDataUtils.findShpFile2: Found in the alternative directory.")
    elif os.path.exists(posixpath.join(folderPath, altDir + "\\" + shpFileTarget)):
        shpFile = posixpath.join(folderPath, altDir + "\\" + shpFileTarget)
        printLog("jpDataUtils.findShpFile2: Found as an errorneous filename.")

    return shpFile


def unzipAndGetShp(
    folder_path,
    zip_file,
    shp_file,
    altdir="",
    code_pref="",
    code_muni="",
    name_muni="",
    epsg="",
    encoding="CP932",
):
    shp_full_path = findShpFile2(
        folder_path, shp_file, altdir, code_pref, code_muni, name_muni
    )

    # --- If shapefile found ---
    if shp_full_path is not None:
        # Create .proj, .qix and .cpg
        _create_proj_qix_cpg(shp_full_path, epsg, encoding)
        return shp_full_path

    # --- Otherwise unzip and retry ---
    zipFileName = zip_file.replace("code_pref", code_pref)
    zipFileName = zipFileName.replace("code_muni", code_muni)
    zipFileName = zipFileName.replace("name_muni", name_muni)

    unzip(folder_path, zipFileName)

    shp_full_path = findShpFile2(
        folder_path, shp_file, altdir, code_pref, code_muni, name_muni
    )

    if shp_full_path is None:
        printLog(
            "jpDataUtils.unzipAndGetShp: Cannot find the file "
            + shp_file
            + " in "
            + folder_path
            + " or in "
            + posixpath.join(folder_path, altdir)
        )
    else:
        # Create .proj, .qix and .cpg
        _create_proj_qix_cpg(shp_full_path, epsg, encoding)

    return shp_full_path


def _create_proj_qix_cpg(shp_full_path, epsg="", encoding="CP932"):
    """Create .proj, .qix and .cpg for a shapefile"""
    if not os.path.exists(shp_full_path[:-4] + ".prj") and epsg != "":
        crs = QgsCoordinateReferenceSystem(f"EPSG:{epsg}")
        with open(shp_full_path[:-4] + ".prj", "w") as prj_file:
            prj_file.write(crs.toWkt())

    if not os.path.exists(shp_full_path[:-4] + ".qix"):
        vl = QgsVectorLayer(shp_full_path, "name", "ogr")
        if vl.isValid():
            vl.dataProvider().createSpatialIndex()

    cpg_path = shp_full_path[:-4] + ".cpg"
    if not os.path.exists(cpg_path):
        with open(cpg_path, "w", encoding="ascii") as f:
            f.write(encoding)


def printLog(message):
    QgsMessageLog.logMessage(str(message), "jpdata", level=Qgis.Warning)


def unzip(folder_path, zip_file):
    zip_path = posixpath.join(folder_path, zip_file)

    if not os.path.exists(zip_path):
        return

    with zipfile.ZipFile(zip_path, "r") as zf:
        for zip_info in zf.infolist():
            
            # --- Correctly decode Japanese filenames from raw bytes ---
            raw_name = zip_info.filename.encode('cp437', errors='ignore')
            try:
                filename = raw_name.decode('cp932')
            except UnicodeDecodeError:
                # fallback: use Python's default-decoded name
                filename = zip_info.filename
            
            # Create safe output path
            output_file_path = posixpath.join(folder_path, filename)

            # Directory handling
            if zip_info.is_dir():
                os.makedirs(output_file_path, exist_ok=True)
                continue

            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            # Extract file
            with zf.open(zip_info) as src, open(output_file_path, "wb") as dst:
                dst.write(src.read())


def replaceCodes(
    text,
    code_map=None,
    code_pref_or_mesh1=None,
    code_muni=None,
    year=None,
    name_muni=None,
):
    if code_map is not None:
        text = text.replace("{code_map}", code_map)
        text = text.replace("code_map", code_map)
    if code_pref_or_mesh1 is not None:
        if (isinstance(code_pref_or_mesh1, str) and len(code_pref_or_mesh1) < 3) or (
            isinstance(code_pref_or_mesh1, int) and code_pref_or_mesh1 < 100
        ):
            code_pref_or_mesh1 = str(code_pref_or_mesh1).zfill(2)
            text = text.replace("{code_pref}", code_pref_or_mesh1)
            text = text.replace("code_pref", code_pref_or_mesh1)
        else:
            code_pref_or_mesh1 = str(code_pref_or_mesh1).zfill(4)
            text = text.replace("{code_mesh1}", code_pref_or_mesh1)
            text = text.replace("code_mesh1", code_pref_or_mesh1)
    if code_muni is not None:
        if (isinstance(code_muni, str) and len(code_muni) < 4) or (
            isinstance(code_muni, int) and code_muni < 1000
        ):
            code_muni = str(code_muni).zfill(3)
            text = text.replace("{code_muni}", code_muni)
            text = text.replace("code_muni", code_muni)
    if year is not None:
        year4digit = getYearAs(year, "year4digit")
        text = text.replace("{year4digit}", year4digit)
        text = text.replace("year4digit", year4digit)
        text = text.replace("{year2digit}", getYearAs(year, "year2digit"))
        text = text.replace("year2digit", getYearAs(year, "year2digit"))
        text = text.replace("{yearJP}", getYearAs(year, "yearJP"))
        text = text.replace("yearJP", getYearAs(year, "yearJP"))
        text = text.replace("{yearJP2digit}", getYearAs(year, "yearJP2digit"))
        text = text.replace("yearJP2digit", getYearAs(year, "yearJP2digit"))
        text = text.replace("{year}", year4digit)
        text = text.replace("year", year4digit)
    if name_muni is not None:
        text = text.replace("{name_muni}", name_muni)
        text = text.replace("name_muni", name_muni)
    return text
