# -*- coding: utf-8 -*-
import os, csv
from . import jpDataUtils

def getYearsByMapCode(code_map, name_pref = None):
    file_path = os.path.join(os.path.dirname(__file__), 'csv', 'LandNumInfo_' + code_map + '.csv')
    years = []
    with open(file_path, 'r') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2 and name_pref is None:
                years.append(row['year'])
            elif len(row) >= 2 and row['availability'] == name_pref:
                years.append(row['year'])
    unique_years = []
    for x in years:
        if x not in unique_years:
            unique_years.append(x)
    return unique_years

def getUrlCodeZipByPrefName(code_map, name_pref, year):
    #name_pref = jpDataUtils.getPrefNameByCode(code_pref)
    file_path = os.path.join(os.path.dirname(__file__), 'csv', 'LandNumInfo_' + code_map + '.csv')
    filtered_rows = []
    x = {'year': '',
         'url': '', 
         'code_map': code_map,
         'zip': '',
         'shp': '',
         'altdir': ''}
    with open(file_path, 'r') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            if len(row) >= 2 and row['availability'] == name_pref and row['year'] == year:
                x['year'] = row['year']
                x['url'] = row['url']
                x['zip'] = row['zip']
                x['shp'] = row['shp']
                x['altdir'] = row['altdir']
    return x

def getUrlCodeZip_W05(code_pref):
    x = {'year': '',
         'url': '', 
         'code_map': 'W05',
         'zip': '',
         'shp': ''}
    int_code_pref = int(code_pref)
    if int_code_pref in [ 1,25,26,27,28,29,30 ]:
        x['year'] = '2009'
        x['url'] = 'https://nlftp.mlit.go.jp/ksj/gml/data/W05/W05-09/W05-09_' + code_pref + '_GML.zip'
        x['zip'] = 'W05-09_' + code_pref + '_GML.zip'
        x['shp'] = 'W05-09_' + code_pref + '-g_Stream.shp'
        x['altdir'] = 'W05-09_' + code_pref + '-g_GML'
    elif int_code_pref in [ 8,9,10,11,12,13,14,19,20,21,22,23,24,31,32,33,34,35 ]:
        x['year'] = '2008'
        x['url'] = 'https://nlftp.mlit.go.jp/ksj/gml/data/W05/W05-08/W05-08_' + code_pref + '_GML.zip'
        x['zip'] = 'W05-08_' + code_pref + '_GML.zip'
        x['shp'] = 'W05-08_' + code_pref + '-g_Stream.shp'
        x['altdir'] = 'W05-08_' + code_pref + '-g_GML'
    elif int_code_pref in [ 2,3,4,5,6,7,15,16,17,18,40,41,42,43,44,45,46,47 ]:
        x['year'] = '2007'
        x['url'] = 'https://nlftp.mlit.go.jp/ksj/gml/data/W05/W05-07/W05-07_' + code_pref + '_GML.zip'
        x['zip'] = 'W05-07_' + code_pref + '_GML.zip'
        x['shp'] = 'W05-07_' + code_pref + '-g_Stream.shp'
        x['altdir'] = 'W05-07_' + code_pref + '-g_GML'
    elif int_code_pref in [ 36,37,38,39 ]:
        x['year'] = '2006'
        x['url'] = 'https://nlftp.mlit.go.jp/ksj/gml/data/W05/W05-06/W05-06_' + code_pref + '_GML.zip'
        x['zip'] = 'W05-06_' + code_pref + '_GML.zip'
        x['shp'] = 'W05-06_' + code_pref + '-g_Stream.shp'
        x['altdir'] = 'W05-06_' + code_pref + '-g_GML'
    
    return x
