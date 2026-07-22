# -*- coding: utf-8 -*-
from qgis.core import QgsMessageLog, Qgis, QgsCoordinateReferenceSystem
from qgis.core import QgsVectorLayer
import csv, os, posixpath
from .compatibility import MESSAGE_WARNING
from . import jpdata_unzip
import unicodedata

DEBUG_MODE = True

PREF_NAMES = {
    "j": {
        1: "北海道",
        2: "青森県",
        3: "岩手県",
        4: "宮城県",
        5: "秋田県",
        6: "山形県",
        7: "福島県",
        8: "茨城県",
        9: "栃木県",
        10: "群馬県",
        11: "埼玉県",
        12: "千葉県",
        13: "東京都",
        14: "神奈川県",
        15: "新潟県",
        16: "富山県",
        17: "石川県",
        18: "福井県",
        19: "山梨県",
        20: "長野県",
        21: "岐阜県",
        22: "静岡県",
        23: "愛知県",
        24: "三重県",
        25: "滋賀県",
        26: "京都府",
        27: "大阪府",
        28: "兵庫県",
        29: "奈良県",
        30: "和歌山県",
        31: "鳥取県",
        32: "島根県",
        33: "岡山県",
        34: "広島県",
        35: "山口県",
        36: "徳島県",
        37: "香川県",
        38: "愛媛県",
        39: "高知県",
        40: "福岡県",
        41: "佐賀県",
        42: "長崎県",
        43: "熊本県",
        44: "大分県",
        45: "宮崎県",
        46: "鹿児島県",
        47: "沖縄県",
        52: "東北地方",
        53: "関東地方",
        54: "甲信越・北陸地方",
        55: "東海地方",
        56: "近畿地方",
        57: "中国地方",
        58: "四国地方",
        59: "九州地方",
        81: "北海道開発局",
        82: "東北地方整備局",
        83: "関東地方整備局",
        84: "北陸地方整備局",
        85: "中部地方整備局",
        86: "近畿地方整備局",
        87: "中国地方整備局",
        88: "四国地方整備局",
        89: "九州地方整備局",
    },
    "e": {
        1: "Hokkaido",
        2: "Aomori",
        3: "Iwate",
        4: "Miyagi",
        5: "Akita",
        6: "Yamagata",
        7: "Fukushima",
        8: "Ibaraki",
        9: "Tochigi",
        10: "Gunma",
        11: "Saitama",
        12: "Chiba",
        13: "Tokyo",
        14: "Kanagawa",
        15: "Niigata",
        16: "Toyama",
        17: "Ishikawa",
        18: "Fukui",
        19: "Yamanashi",
        20: "Nagano",
        21: "Gifu",
        22: "Shizuoka",
        23: "Aichi",
        24: "Mie",
        25: "Shiga",
        26: "Kyoto",
        27: "Osaka",
        28: "Hyogo",
        29: "Nara",
        30: "Wakayama",
        31: "Tottori",
        32: "Shimane",
        33: "Okayama",
        34: "Hiroshima",
        35: "Yamaguchi",
        36: "Tokushima",
        37: "Kagawa",
        38: "Ehime",
        39: "Kochi",
        40: "Fukuoka",
        41: "Saga",
        42: "Nagasaki",
        43: "Kumamoto",
        44: "Oita",
        45: "Miyazaki",
        46: "Kagoshima",
        47: "Okinawa",
        52: "Tohoku",
        53: "Kanto",
        54: "Koshinetsu and Hokuriku",
        55: "Tokai",
        56: "Kinki",
        57: "Chugoku",
        58: "Shikoku",
        59: "Kyushu",
        81: "Hokkaido Regional Development Bureau",
        82: "Tohoku Regional Development Bureau",
        83: "Kanto Regional Development Bureau",
        84: "Hokuriku Regional Development Bureau",
        85: "Chubu Regional Development Bureau",
        86: "Kinki Regional Development Bureau",
        87: "Chugoku Regional Development Bureau",
        88: "Shikoku Regional Development Bureau",
        89: "Kyushu Regional Development Bureau",
    },
}


def printLog(message):
    QgsMessageLog.logMessage(str(message), "jpdata", level=MESSAGE_WARNING)


def printDebugLog(message):
    if DEBUG_MODE:
        printLog("DEBUG: ")
        printLog(message)

def getYearAs(year, format="year2digit"):
    """year4digit = '2023'
    year2digit = '23'
    yearJP = 'R5'
    yearJP2digit = '05'
    """
    try:
        if format == "year4digit":
            return str(year)

        elif format == "year2digit":
            return str(year)[2:4]

        elif format == "yearJP":
            if int(year) - 2018 > 0:
                return "R" + str(int(year) - 2018)
            elif int(year) - 1998 > 0:
                return "H" + str(int(year) - 1988)
            else:
                return "S" + str(int(year) - 1925)

        elif format == "yearJP2digit":
            if int(year) - 2018 > 0:
                return str(int(year) - 2018).zfill(2)
            elif int(year) - 1998 > 0:
                return str(int(year) - 1988).zfill(2)
            else:
                return str(int(year) - 1925).zfill(2)

        return str(year)

    except Exception:
        return year


def getPrefNameByCode(pref_code, lang="j"):
    pref_name = PREF_NAMES.get(lang, PREF_NAMES["e"]).get(pref_code, "")
    return pref_name


def getPrefCodeByName(pref_name):
    pref_code = ""
    pref_name = pref_name.strip()
    pref_name = pref_name.replace("県", "")
    if pref_name == "北海道" or pref_name == "Hokkaido":
        pref_code = "01"
    elif pref_name == "青森" or pref_name == "Aomori":
        pref_code = "02"
    elif pref_name == "岩手" or pref_name == "Iwate":
        pref_code = "03"
    elif pref_name == "宮城" or pref_name == "Miyagi":
        pref_code = "04"
    elif pref_name == "秋田" or pref_name == "Akita":
        pref_code = "05"
    elif pref_name == "山形" or pref_name == "Yamagata":
        pref_code = "06"
    elif pref_name == "福島" or pref_name == "Fukushima":
        pref_code = "07"
    elif pref_name == "茨城" or pref_name == "Ibaraki":
        pref_code = "08"
    elif pref_name == "栃木" or pref_name == "Tochigi":
        pref_code = "09"
    elif pref_name == "群馬" or pref_name == "Gunma":
        pref_code = "10"
    elif pref_name == "埼玉" or pref_name == "Saitama":
        pref_code = "11"
    elif pref_name == "千葉" or pref_name == "Chiba":
        pref_code = "12"
    elif pref_name == "東京都" or pref_name == "東京" or pref_name == "Tokyo":
        pref_code = "13"
    elif pref_name == "神奈川" or pref_name == "Kanagawa":
        pref_code = "14"
    elif pref_name == "新潟" or pref_name == "Niigata":
        pref_code = "15"
    elif pref_name == "富山" or pref_name == "Toyama":
        pref_code = "16"
    elif pref_name == "石川" or pref_name == "Ishikawa":
        pref_code = "17"
    elif pref_name == "福井" or pref_name == "Fukui":
        pref_code = "18"
    elif pref_name == "山梨" or pref_name == "Yamanashi":
        pref_code = "19"
    elif pref_name == "長野" or pref_name == "Nagano":
        pref_code = "20"
    elif pref_name == "岐阜" or pref_name == "Gifu":
        pref_code = "21"
    elif pref_name == "静岡" or pref_name == "Shizuoka":
        pref_code = "22"
    elif pref_name == "愛知" or pref_name == "Aichi":
        pref_code = "23"
    elif pref_name == "三重" or pref_name == "Mie":
        pref_code = "24"
    elif pref_name == "滋賀" or pref_name == "Shiga":
        pref_code = "25"
    elif pref_name == "京都府" or pref_name == "京都" or pref_name == "Kyoto":
        pref_code = "26"
    elif pref_name == "大阪府" or pref_name == "大阪" or pref_name == "Osaka":
        pref_code = "27"
    elif pref_name == "兵庫" or pref_name == "Hyogo":
        pref_code = "28"
    elif pref_name == "奈良" or pref_name == "Nara":
        pref_code = "29"
    elif pref_name == "和歌山" or pref_name == "Wakayama":
        pref_code = "30"
    elif pref_name == "鳥取" or pref_name == "Tottori":
        pref_code = "31"
    elif pref_name == "島根" or pref_name == "Shimane":
        pref_code = "32"
    elif pref_name == "岡山" or pref_name == "Okayama":
        pref_code = "33"
    elif pref_name == "広島" or pref_name == "Hiroshima":
        pref_code = "34"
    elif pref_name == "山口" or pref_name == "Yamaguchi":
        pref_code = "35"
    elif pref_name == "徳島" or pref_name == "Tokushima":
        pref_code = "36"
    elif pref_name == "香川" or pref_name == "Kagawa":
        pref_code = "37"
    elif pref_name == "愛媛" or pref_name == "Ehime":
        pref_code = "38"
    elif pref_name == "高知" or pref_name == "Kochi":
        pref_code = "39"
    elif pref_name == "福岡" or pref_name == "Fkuoka":
        pref_code = "40"
    elif pref_name == "佐賀" or pref_name == "Saga":
        pref_code = "41"
    elif pref_name == "長崎" or pref_name == "Nagasaki":
        pref_code = "42"
    elif pref_name == "熊本" or pref_name == "Kumamoto":
        pref_code = "43"
    elif pref_name == "大分" or pref_name == "Oita":
        pref_code = "44"
    elif pref_name == "宮崎" or pref_name == "Miyazaki":
        pref_code = "45"
    elif pref_name == "鹿児島" or pref_name == "Kagoshima":
        pref_code = "46"
    elif pref_name == "沖縄" or pref_name == "Okinawa":
        pref_code = "47"
    elif pref_name == "東北地方" or pref_name == "Tohoku":
        pref_code = "52"
    elif pref_name == "関東地方" or pref_name == "Kanto":
        pref_code = "53"
    elif pref_name == "甲信越・北陸地方" or pref_name == "Koshinetsu and Hokuriku":
        pref_code = "54"
    elif pref_name == "東海地方" or pref_name == "Tokai":
        pref_code = "55"
    elif pref_name == "近畿地方" or pref_name == "Kinki":
        pref_code = "56"
    elif pref_name == "中国地方" or pref_name == "Chugoku":
        pref_code = "57"
    elif pref_name == "四国地方" or pref_name == "Shikoku":
        pref_code = "58"
    elif pref_name == "九州地方" or pref_name == "Kyushu":
        pref_code = "59"
    elif pref_name == "北海道開発局" or pref_name == "Hokkaido Regional Development Bureau":
        pref_code = "81"
    elif pref_name == "東北地方整備局" or pref_name == "Tohoku Regional Development Bureau":
        pref_code = "82"
    elif pref_name == "関東地方整備局" or pref_name == "Kanto Regional Development Bureau":
        pref_code = "83"
    elif pref_name == "北陸地方整備局" or pref_name == "Hokuriku Regional Development Bureau":
        pref_code = "84"
    elif pref_name == "中部地方整備局" or pref_name == "Chubu Regional Development Bureau":
        pref_code = "85"
    elif pref_name == "近畿地方整備局" or pref_name == "Kinki Regional Development Bureau":
        pref_code = "86"
    elif pref_name == "中国地方整備局" or pref_name == "Chugoku Regional Development Bureau":
        pref_code = "87"
    elif pref_name == "四国地方整備局" or pref_name == "Shikoku Regional Development Bureau":
        pref_code = "88"
    elif pref_name == "九州地方整備局" or pref_name == "Kyushu Regional Development Bureau":
        pref_code = "89"
    return pref_code


def get_records_from_csv(csvfile, key_column=None, encoding="utf-8-sig"):
    if not os.path.isabs(csvfile):
        csvfile = posixpath.join(os.path.dirname(__file__), "csv", csvfile)
    new_dict = {}
    with open(csvfile, "r", encoding=encoding) as f:
        csvreader = csv.DictReader(f)
        if key_column is not None:
            for row in csvreader:
                key = row.get(key_column)
                if key:  # only add if key exists
                    new_dict[key] = row
            return new_dict
        else:
            return list(csvreader) 


def getMapsFromCsv2(lang="j"):
    return get_records_from_csv("LandNumInfo.csv", "name_" + lang)


def getTilesFromCsv():
    filePath = posixpath.join(os.path.dirname(__file__), "csv", "GSI.csv")
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)
        return rows


def findShpFile2(folderPath, year, shp, altdir, code_pref, code_muni="", name_muni=""):
    shpFile = None
    shpFileTarget = replaceCodes(
        shp,
        year=year,
        code_pref_or_mesh1=code_pref,
        code_muni=code_muni,
        name_muni=name_muni,
    )
    altDir = replaceCodes(
        altdir, year=year, code_pref_or_mesh1=code_pref, code_muni=code_muni, name_muni=name_muni
    )
    folderPath = unicodedata.normalize("NFC", folderPath)
    shpFileTarget = unicodedata.normalize("NFC", shpFileTarget)
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
    year,
    zip_file,
    shp_file,
    altdir="",
    code_pref="",
    code_muni="",
    name_muni="",
    epsg="",
    encoding="CP932",
):
    zip_to_folder = zip_file[:-4]

    def try_find(base):
        path = findShpFile2(base, year, shp_file, altdir, code_pref, code_muni, name_muni)
        if path:
            _create_proj_qix_cpg(path, epsg, encoding)
            return path
        return None

    # --- Find shp ---
    for base in [folder_path, posixpath.join(folder_path, zip_to_folder)]:
        result = try_find(base)
        if result:
            return result

    # --- if not, unzip ---
    zipFileName = replaceCodes(zip_file, 
                               code_pref_or_mesh1=code_pref,
                               code_muni=code_muni,
                               name_muni=name_muni)

    unzip(folder_path, zipFileName)

    # --- Find shp again ---
    for base in [folder_path, posixpath.join(folder_path, zip_to_folder)]:
        result = try_find(base)
        if result:
            return result

    # --- if not, log ---
    printLog(
        f"jpDataUtils.unzipAndGetShp: Cannot find {shp_file} "
        f"in {folder_path} or {posixpath.join(folder_path, altdir)}"
    )
    return None


def _create_proj_qix_cpg(shp_full_path, epsg="", encoding="CP932"):
    if shp_full_path[:-4] != ".shp":
        return
    
    """Create .proj, .qix and .cpg for a shapefile"""
    if not os.path.exists(shp_full_path[:-4] + ".prj") and epsg != "":
        crs = QgsCoordinateReferenceSystem(f"EPSG:{epsg}")
        with open(shp_full_path[:-4] + ".prj", "w") as prj_file:
            prj_file.write(crs.toWkt())

    if not os.path.exists(shp_full_path[:-4] + ".qix"):
        vl = QgsVectorLayer(shp_full_path, "name", "ogr")
        if vl.isValid():
            vl.dataProvider().createSpatialIndex()

    if not os.path.exists(cpg_path):
        cpg_path = shp_full_path[:-4] + ".cpg"
        with open(cpg_path, "w", encoding="ascii") as f:
            f.write(encoding)


def unzip(folder_path, zip_file):
    return jpdata_unzip.unzip_qgis_safe(folder_path, zip_file)


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

def count_invalid_geometry(layer):
    """Check the geometry validity of a given vector layer."""
    if isinstance(layer, QgsVectorLayer):
        count = 0
        for feature in layer.getFeatures():
            if not feature.geometry().isGeosValid():
                count = count + 1
    return count

def unique_list(given_list, sort= False):
    if sort:
        return sorted(dict.fromkeys(given_list))
    else:
        return list(dict.fromkeys(given_list))


    #unique_list = []
    #for x in given_list:
    #    if x not in unique_list:
    #        unique_list.append(x)
    #return unique_list



