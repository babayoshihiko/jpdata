# -*- coding: utf-8 -*-
from qgis.core import QgsMessageLog, Qgis, QgsCoordinateReferenceSystem
import os, csv
import zipfile


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


def getMapsFromCsv():
    filePath = os.path.join(os.path.dirname(__file__), "csv", "LandNumInfo.csv")
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)
        return rows


def getTilesFromCsv():
    filePath = os.path.join(os.path.dirname(__file__), "csv", "GSI.csv")
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)
        return rows


def findShpFile2(folderPath, shp, altdir, code_pref, code_muni="", name_muni=""):
    shpFile = None
    shpFileTarget = shp.replace("code_pref", code_pref)
    shpFileTarget = shpFileTarget.replace("code_muni", code_muni)
    shpFileTarget = shpFileTarget.replace("name_muni", name_muni)
    altDir = altdir.replace("code_pref", code_pref)
    altDir = altDir.replace("code_muni", code_muni)
    altDir = altDir.replace("name_muni", name_muni)
    if os.path.exists(os.path.join(folderPath, shpFileTarget)):
        shpFile = os.path.join(folderPath, shpFileTarget)
        QgsMessageLog.logMessage(
            "jpDataUtils.findShpFile2: Found 1 " + shpFile, "jpdata", level=Qgis.Warning
        )
    elif os.path.exists(os.path.join(folderPath, altDir, shpFileTarget)):
        shpFile = os.path.join(folderPath, altDir, shpFileTarget)
        QgsMessageLog.logMessage(
            "jpDataUtils.findShpFile2: Found 2 " + shpFile, "jpdata", level=Qgis.Warning
        )
    elif os.path.exists(os.path.join(folderPath, altDir + "\\" + shpFileTarget)):
        shpFile = os.path.join(folderPath, altDir + "\\" + shpFileTarget)
        QgsMessageLog.logMessage(
            "jpDataUtils.findShpFile2: Found 3 " + shpFile, "jpdata", level=Qgis.Warning
        )

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
):
    QgsMessageLog.logMessage("jpDataUtils.unzipAndGetShp", "jpdata", level=Qgis.Warning)
    shpFileName = findShpFile2(
        folder_path, shp_file, altdir, code_pref, code_muni, name_muni
    )
    if shpFileName is not None:
        if not os.path.exists(shpFileName[:-4] + ".prj") and epsg != "":
            crs = QgsCoordinateReferenceSystem(f"EPSG:{epsg}")
            with open(shpFileName[:-4] + ".prj", "w") as prj_file:
                prj_file.write(crs.toWkt())

        return shpFileName
    else:
        zipFileName = zip_file.replace("code_pref", code_pref)
        zipFileName = zipFileName.replace("code_muni", code_muni)
        zipFileName = zipFileName.replace("name_muni", name_muni)

        # Below is a workaround for a zip file with Japanese filenames/foldernames
        if os.path.exists(os.path.join(folder_path, zipFileName)):
            with zipfile.ZipFile(os.path.join(folder_path, zipFileName), "r") as zf:
                # Iterate through each file in the zip
                for zip_info in zf.infolist():
                    # Extract the filename using the correct encoding
                    # (e.g. 'cp932' for Japanese Windows)
                    filename = zip_info.filename.encode("cp437").decode("cp932")
                    # Construct the output file path
                    output_file_path = os.path.join(folder_path, filename)
                    if zip_info.is_dir():
                        # Create directories if they do not exist
                        os.makedirs(output_file_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                        # Extract the file
                        with zf.open(zip_info) as file:
                            with open(output_file_path, "wb") as out_file:
                                out_file.write(file.read())
    shpFileName = findShpFile2(
        folder_path, shp_file, altdir, code_pref, code_muni, name_muni
    )
    if shpFileName is None:
        printLog(
            "jpDataUtils.unzipAndGetShp: Cannot find the file "
            + shp_file
            + " in "
            + folder_path
            + " or in "
            + os.path.join(folder_path, altdir)
        )
    else:
        if not os.path.exists(shpFileName[:-4] + ".prj") and epsg != "":
            crs = QgsCoordinateReferenceSystem(f"EPSG:{epsg}")
            with open(shpFileName[:-4] + ".prj", "w") as prj_file:
                prj_file.write(crs.toWkt())

    return shpFileName


def printLog(message):
    QgsMessageLog.logMessage(message, "jpdata", level=Qgis.Warning)
