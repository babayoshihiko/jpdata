# -*- coding: utf-8 -*-
from qgis.core import QgsMessageLog, Qgis
import os, csv
import zipfile

def getPrefNameByCode(pref_code):
    pref_name = u''
    if pref_code == 1:
        pref_name = u'北海道'
    elif pref_code == 2:
        pref_name = u'青森県'
    elif pref_code == 3:
        pref_name = u'岩手県'
    elif pref_code == 4:
        pref_name = u'宮城県'
    elif pref_code == 5:
        pref_name = u'秋田県'
    elif pref_code == 6:
        pref_name = u'山形県'
    elif pref_code == 7:
        pref_name = u'福島県'
    elif pref_code == 8:
        pref_name = u'茨城県'
    elif pref_code == 9:
        pref_name = u'栃木県'
    elif pref_code == 10:
        pref_name = u'群馬県'
    elif pref_code == 11:
        pref_name = u'埼玉県'
    elif pref_code == 12:
        pref_name = u'千葉県'
    elif pref_code == 13:
        pref_name = u'東京都'
    elif pref_code == 14:
        pref_name = u'神奈川県'
    elif pref_code == 15:
        pref_name = u'新潟県'
    elif pref_code == 16:
        pref_name = u'富山県'
    elif pref_code == 17:
        pref_name = u'石川県'
    elif pref_code == 18:
        pref_name = u'福井県'
    elif pref_code == 19:
        pref_name = u'山梨県'
    elif pref_code == 20:
        pref_name = u'長野県'
    elif pref_code == 21:
        pref_name = u'岐阜県'
    elif pref_code == 22:
        pref_name = u'静岡県'
    elif pref_code == 23:
        pref_name = u'愛知県'
    elif pref_code == 24:
        pref_name = u'三重県'
    elif pref_code == 25:
        pref_name = u'滋賀県'
    elif pref_code == 26:
        pref_name = u'京都府'
    elif pref_code == 27:
        pref_name = u'大阪府'
    elif pref_code == 28:
        pref_name = u'兵庫県'
    elif pref_code == 29:
        pref_name = u'奈良県'
    elif pref_code == 30:
        pref_name = u'和歌山県'
    elif pref_code == 31:
        pref_name = u'鳥取県'
    elif pref_code == 32:
        pref_name = u'島根県'
    elif pref_code == 33:
        pref_name = u'岡山県'
    elif pref_code == 34:
        pref_name = u'広島県'
    elif pref_code == 35:
        pref_name = u'山口県'
    elif pref_code == 36:
        pref_name = u'徳島県'
    elif pref_code == 37:
        pref_name = u'香川県'
    elif pref_code == 38:
        pref_name = u'愛媛県'
    elif pref_code == 39:
        pref_name = u'高知県'
    elif pref_code == 40:
        pref_name = u'福岡県'
    elif pref_code == 41:
        pref_name = u'佐賀県'
    elif pref_code == 42:
        pref_name = u'長崎県'
    elif pref_code == 43:
        pref_name = u'熊本県'
    elif pref_code == 44:
        pref_name = u'大分県'
    elif pref_code == 45:
        pref_name = u'宮崎県'
    elif pref_code == 46:
        pref_name = u'鹿児島県'
    elif pref_code == 47:
        pref_name = u'沖縄県'
    
    return pref_name

def getPrefCodeByName(pref_name):
    pref_code = u''
    if pref_name == u'北海道':
        pref_code = u'01'
    elif pref_name == u'青森県':
        pref_code = u'02'
    elif pref_name == u'岩手県':
        pref_code = u'03'
    elif pref_name == u'宮城県':
        pref_code = u'04'
    elif pref_name == u'秋田県':
        pref_code = u'05'
    elif pref_name == u'山形県':
        pref_code = u'06'
    elif pref_name == u'福島県':
        pref_code = u'07'
    elif pref_name == u'茨城県':
        pref_code = u'08'
    elif pref_name == u'栃木県':
        pref_code = u'09'
    elif pref_name == u'群馬県':
        pref_code = u'10'
    elif pref_name == u'埼玉県':
        pref_code = u'11'
    elif pref_name == u'千葉県':
        pref_code = u'12'
    elif pref_name == u'東京都':
        pref_code = u'13'
    elif pref_name == u'神奈川県':
        pref_code = u'14'
    elif pref_name == u'新潟県':
        pref_code = u'15'
    elif pref_name == u'富山県':
        pref_code = u'16'
    elif pref_name == u'石川県':
        pref_code = u'17'
    elif pref_name == u'福井県':
        pref_code = u'18'
    elif pref_name == u'山梨県':
        pref_code = u'19'
    elif pref_name == u'長野県':
        pref_code = u'20'
    elif pref_name == u'岐阜県':
        pref_code = u'21'
    elif pref_name == u'静岡県':
        pref_code = u'22'
    elif pref_name == u'愛知県':
        pref_code = u'23'
    elif pref_name == u'三重県':
        pref_code = u'24'
    elif pref_name == u'滋賀県':
        pref_code = u'25'
    elif pref_name == u'京都府':
        pref_code = u'26'
    elif pref_name == u'大阪府':
        pref_code = u'27'
    elif pref_name == u'兵庫県':
        pref_code = u'28'
    elif pref_name == u'奈良県':
        pref_code = u'29'
    elif pref_name == u'和歌山県':
        pref_code = u'30'
    elif pref_name == u'鳥取県':
        pref_code = u'31'
    elif pref_name == u'島根県':
        pref_code = u'32'
    elif pref_name == u'岡山県':
        pref_code = u'33'
    elif pref_name == u'広島県':
        pref_code = u'34'
    elif pref_name == u'山口県':
        pref_code = u'35'
    elif pref_name == u'徳島県':
        pref_code = u'36'
    elif pref_name == u'香川県':
        pref_code = u'37'
    elif pref_name == u'愛媛県':
        pref_code = u'38'
    elif pref_name == u'高知県':
        pref_code = u'39'
    elif pref_name == u'福岡県':
        pref_code = u'40'
    elif pref_name == u'佐賀県':
        pref_code = u'41'
    elif pref_name == u'長崎県':
        pref_code = u'42'
    elif pref_name == u'熊本県':
        pref_code = u'43'
    elif pref_name == u'大分県':
        pref_code = u'44'
    elif pref_name == u'宮崎県':
        pref_code = u'45'
    elif pref_name == u'鹿児島県':
        pref_code = u'46'
    elif pref_name == u'沖縄県':
        pref_code = u'47'
        
    return pref_code

def getMapsFromCsv():
    filePath = os.path.dirname(__file__) + '/csv/LandNumInfo_Full.csv'
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)
        return rows

def getTilesFromCsv():
    filePath = os.path.dirname(__file__) + '/csv/GSI.csv'
    with open(filePath, "r") as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)
        return rows

def findShpFile2(folderPath, shp, altdir, code_pref, code_muni = '', name_muni = ''):
    shpFile = None
    shpFileTarget = shp.replace('code_pref', code_pref)
    shpFileTarget = shpFileTarget.replace('code_muni', code_muni)
    shpFileTarget = shpFileTarget.replace('name_muni', name_muni)
    altDir = altdir.replace('code_pref', code_pref)
    altDir = altDir.replace('code_muni', code_muni)
    altDir = altDir.replace('name_muni', name_muni)
    if os.path.exists(folderPath + '/' + shpFileTarget):
        shpFile = folderPath + '/' + shpFileTarget
    elif os.path.exists(folderPath + '/' + altDir + '/' + shpFileTarget):
        shpFile = folderPath + '/' + altDir + '/' + shpFileTarget
    elif os.path.exists(folderPath + '/' + altDir + '\\' + shpFileTarget):
        shpFile = folderPath + '/' + altDir + '\\' + shpFileTarget
    return shpFile

def unzipAndGetShp(folder_path, zip_file, shp_file, altdir = '', code_pref = '', code_muni = '', name_muni = ''):
    shpFileName = findShpFile2(folder_path, shp_file, altdir, code_pref, code_muni, name_muni)
    if shpFileName is None:
        zipFileName = zip_file.replace('code_pref', code_pref)
        zipFileName = zipFileName.replace('code_muni', code_muni)
        zipFileName = zipFileName.replace('name_muni', name_muni)
        # Below is a workaround for a zip file with Japanese filenames/foldernames
        if os.path.exists(folder_path + '/' + zipFileName):
            with zipfile.ZipFile(folder_path + '/' + zipFileName, 'r') as zf:
                # Iterate through each file in the zip
                for zip_info in zf.infolist():
                    # Extract the filename using the correct encoding (e.g. 'cp932' for Japanese Windows)
                    filename = zip_info.filename.encode('cp437').decode('cp932')
                    # Construct the output file path
                    output_file_path = folder_path + '/' + filename
                    if zip_info.is_dir():
                        # Create directories if they do not exist
                        os.makedirs(output_file_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                        # Extract the file
                        with zf.open(zip_info) as file:
                            with open(output_file_path, 'wb') as out_file:
                                out_file.write(file.read())
    shpFileName = findShpFile2(folder_path, shp_file, altdir, code_pref, code_muni, name_muni)
    if shpFileName is None:
        QgsMessageLog.logMessage('Cannot find the file ' + shp_file, 'jpdata', level=Qgis.Warning)
    
    return shpFileName

