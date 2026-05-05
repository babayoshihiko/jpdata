# -*- coding: utf-8 -*-
import requests
import posixpath
import os
import zipfile
from qgis import processing
from . import jpDataUtils


def _get_string_for_mesh(type_muni):
    mapping = ["", "S", "H", "Q", "E"]
    if 0 <= type_muni < len(mapping):
        return mapping[type_muni]
    return ""

def _get_code_for_mesh(year, type_muni=0, add_type_string = False):
    mapping = {
        0: {
            "2020": "001082", 
            "2015": "000849", 
            "2010": "000573", 
            "2005": "000051", 
            "2000": "000002"},
        1: {
            "2020": "001140", 
            "2015": "000846", 
            "2010": "000608", 
            "2005": "000148", 
            "2000": "000146", 
            "1995": "000751"},
        2: {
            "2020": "001141", 
            "2015": "000847", 
            "2010": "000609", 
            "2005": "000387", 
            "2000": "000386", 
            "1995": "000752"},
        3: {
            "2020": "001142", 
            "2015": "000876", 
            "2010": "000649", 
            "2005": "000652"},
        4: {
            "2020": "001231", 
            "2015": "001218"}
    }
    return mapping.get(type_muni, {}).get(str(year))

def get_subfolder_qml(type_muni, year):
    if type_muni == 0:
        tempSubFolder = "Census"
        tempQmlFile = "Census-" + year + ".qml"
    if type_muni == 1:
        tempSubFolder = "Census-SDDSWS"
        tempQmlFile = "Census-SDDSWS-" + year + ".qml"
    elif type_muni == 2:
        tempSubFolder = "Census-HDDSWH"
        tempQmlFile = "Census-HDDSWH-" + year + ".qml"
    elif type_muni == 3:
        tempSubFolder = "Census-QDDSWQ"
        tempQmlFile = "Census-QDDSWQ-" + year + ".qml"
    elif type_muni == 4:
        tempSubFolder = "Census-EDDSWE"
        tempQmlFile = "Census-EDDSWE-" + year + ".qml"
    return tempSubFolder, tempQmlFile


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
    tempSubFolder, tmpQmlFile = get_subfolder_qml(type_muni, year)
    return tempUrl, tempZip, tempSubFolder


def getUrl(year, code_pref, code_muni, type_muni=0):
    code_pref = str(code_pref).zfill(2)
    if type_muni == 0:
        datum = "2011" if year in ["2020", "2015"] else "2000"
        
        return (
            f"https://www.e-stat.go.jp/gis/statmap-search/data?"
            f"dlserveyId=A00200521{year}&"
            f"code={code_pref}{code_muni}&"
            f"coordSys=2&format=shape&downloadType=5&datum={datum}"
        )
    survey_char = _get_string_for_mesh(type_muni)
    
    if not survey_char:
        return None

    return (
        f"https://www.e-stat.go.jp/gis/statmap-search/data?"
        f"dlserveyId={survey_char}&"
        f"code={code_muni}&"
        f"coordSys=1&format=shape&downloadType=5"
    )


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
    elif type_muni == 4:
        zipFileName = "EDDSWE" + code_muni + ".zip"
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
    elif type_muni >= 1:
        shpFileName = "MESH0" + code_muni + ".shp"
    return shpFileName


def getAttr(year, code_pref, code_muni, type_muni=0):
    tempUrl = getAttrUrl(year, code_pref, code_muni, type_muni)
    tempZip = getAttrZipFileName(year, code_pref, code_muni, type_muni)
    tempSubFolder, tmpQmlFile = get_subfolder_qml(type_muni, year)
    return tempUrl, tempZip, tempSubFolder


def getAttrUrl(year, code_pref, code_muni, type_muni=0):
    if type_muni == 0:
        code_pref = str(code_pref).zfill(2)
    _code = _get_code_for_mesh(year, type_muni)
    if not _code:
        return None
    url = (
        f"https://www.e-stat.go.jp/gis/statmap-search/data?"
        f"statsId={_code}&"
        f"code={code_pref}&"
        f"downloadType=2"
    )
    return url


def _get_base_filename(year, code_pref, code_muni, type_muni):
    mesh_code = _get_code_for_mesh(year, type_muni)
    if not mesh_code:
        return None
    if type_muni == 0:
        suffix = f"C{str(code_pref).zfill(2)}"
    else:
        char = _get_string_for_mesh(type_muni)
        suffix = f"{char}{code_muni}"
    return f"tblT{mesh_code}{suffix}"

def getAttrZipFileName(year, code_pref, code_muni, type_muni=0):
    base = _get_base_filename(year, code_pref, code_muni, type_muni)
    return f"{base}.zip" if base else None

def getAttrCsvFileName(year, code_pref, code_muni, type_muni=0):
    base = _get_base_filename(year, code_pref, code_muni, type_muni)
    return f"{base}.txt" if base else None


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
    ) as f:  # "wb" can write bytes 
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




def performJoin(folder, year, shp_name, csv_name):
    import os
    import posixpath
    import processing
    from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsCoordinateTransformContext

    # 1. パスの解決
    folder = folder.replace('\\', '/')
    shp_path = posixpath.join(folder, shp_name) if not posixpath.isabs(shp_name) else shp_name.replace('\\', '/')
    csv_path = posixpath.join(folder, csv_name) if not posixpath.isabs(csv_name) else csv_name.replace('\\', '/')
    output_path = shp_path[:-4] + "-" + year + ".shp"

    # --- 2. CSVをUTF-8に変換 (2行目削除 & .csvt作成) ---
    csv_utf8 = csv_path[:-4] + ".csv"
    if not os.path.exists(csv_utf8):
        with open(csv_path, "r", encoding="CP932") as fin, \
             open(csv_utf8, "w", encoding="UTF-8") as fout:
            for i, line in enumerate(fin):
                if i == 1:
                    count = line.count(",")
                    csvt = "String,Integer,String,String" + ",Integer" * (count - 3) if count > 4 else "String" + ",Integer" * count
                    with open(csv_utf8 + "t", "w", encoding="UTF-8") as f_csvt:
                        f_csvt.write(csvt)
                    continue
                fout.write(line.replace("*", ""))

    # --- 3. レイヤオブジェクトを明示的に作成 (ここでエンコーディングを固定) ---
    # 元のSHPを読み込み、CP932であることを強制
    lyr_shp = QgsVectorLayer(shp_path, "base_shp", "ogr")
    lyr_shp.setProviderEncoding("CP932")
    lyr_shp.dataProvider().setEncoding("CP932")

    # 変換後のCSVを読み込み、UTF-8であることを強制
    lyr_csv = QgsVectorLayer(csv_utf8, "data_csv", "ogr")
    lyr_csv.setProviderEncoding("UTF-8")
    lyr_csv.dataProvider().setEncoding("UTF-8")

    if not lyr_shp.isValid() or not lyr_csv.isValid():
        raise Exception("レイヤの読み込みに失敗しました。パスを確認してください。")

    # --- 4. Join実行 (パスではなくオブジェクトを渡す) ---
    join_params = {
        "INPUT": lyr_shp,
        "FIELD": "KEY_CODE",
        "INPUT_2": lyr_csv,
        "FIELD_2": "KEY_CODE",
        "OUTPUT": "TEMPORARY_OUTPUT" # 一旦メモリに持たせる
    }
    result = processing.run("qgis:joinattributestable", join_params)
    joined_layer = result["OUTPUT"]

    # --- 5. 最終的なUTF-8 Shapefileとして書き出し ---
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.fileEncoding = "UTF-8"
    options.driverName = "ESRI Shapefile"

    QgsVectorFileWriter.writeAsVectorFormatV2(
        joined_layer, 
        output_path, 
        QgsCoordinateTransformContext(), 
        options
    )

    # --- 6. .cpgファイルを確実に作成 ---
    with open(output_path[:-4] + ".cpg", "w") as f:
        f.write("UTF-8")

    # メモリ解放
    del lyr_shp
    del lyr_csv

    return output_path, "UTF-8"





def performJoin_old(folder, year, shp, csv):
    shp_encoding = "CP932"  # The encoding for shp
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
                # The encoding for csv
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

                            with open(csv[:-4] + ".csvt", "w", encoding="UTF-8") as fout2:
                                fout2.write(csvt)
                fout.close()
                csv = csv[:-4] + ".csv"
            else:
                return shp, shp_encoding

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
    
            vl = QgsVectorLayer(output, "joined", "ogr")

            options = QgsVectorFileWriter.SaveVectorOptions()
            options.fileEncoding = "UTF-8"

            QgsVectorFileWriter.writeAsVectorFormatV2(
                vl,
                output,
                QgsCoordinateTransformContext(),
                options
            )

    cfg = output[:-4] + ".cpg"
    if os.path.exists(cfg):
        with open(cfg, "r") as fp:
            for line in fp:
                if "shift_jis" in line.lower():
                    shp_encoding = "CP932"
                    break
                elif "utf-8" in line.lower():
                    break

    return output, shp_encoding


def set_year_items(combo_widget, first_year=2000):
    """
    Populate the census year ComboBox based on the first available year.
    Census data is generated every 5 years from 2020.
    """
    # Save current selection to restore it later
    current_year = combo_widget.currentText()
    
    try:
        start_year = 2020
        target_year = int(first_year)
        
        if target_year > start_year:
            years = [str(start_year)]
        else:
            # Generate years: [2020, 2015, ..., target_year]
            years = [str(y) for y in range(start_year, target_year - 1, -5)]
    except (ValueError, TypeError):
        years = ["2020"]

    # Update UI
    combo_widget.blockSignals(True)
    combo_widget.clear()
    if years:
        combo_widget.addItems(years)
    
    # Restore selection if it still exists
    index = combo_widget.findText(current_year)
    if index != -1:
        combo_widget.setCurrentIndex(index)
    else:
        combo_widget.setCurrentIndex(0)
    
    combo_widget.blockSignals(False)


