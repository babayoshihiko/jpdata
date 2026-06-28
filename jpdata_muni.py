# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils
from qgis.core import QgsMessageLog, Qgis
# QgsMessageLog.logMessage(str(len(self._code_pref_muni)), "jpdata", Qgis.Info)

# The default CSV files are: code_pref_muni.csv and muni_mesh1.csv.
#
# Additionally, the address CSV files can be downloaded and saved in FOLDER/Addr.
# 


class jpDataMuni:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._code_pref_muni = None
        self._muni_mesh1 = None
        self._addr = None
        self._current_pref = ""
        self._lang = "j"
        self._download_fullpath = ""
        self._year = 2025

    def set_download_folder(self, download_fullpath):
        if not os.path.exists(posixpath.join(download_fullpath, "Addr")):
            os.mkdir(posixpath.join(download_fullpath, "Addr"))
        self._download_fullpath = posixpath.join(download_fullpath, "Addr")

    def set_lang(self, lang):
        self._lang = lang[:1].lower()

    def _load_code_pref_muni(self):
        if self._code_pref_muni is None:
            self._code_pref_muni = jpDataUtils.get_records_from_csv("code_pref_muni.csv")

    def _load_code_muni_meshi1(self):
        if self._muni_mesh1 is None:
            self._muni_mesh1 = jpDataUtils.get_records_from_csv("muni_mesh1.csv")

    def get_munis(self, name_pref):
        return self._getMuniFromPrefName(name_pref)
    
    def get_towns(self, name_pref, name_muni):
        self._load_csv(name_pref)
        rows = self._addr
        if rows is None:
            return None
        filtered_rows = []
        for row in rows:
            if row["都道府県名"] == name_pref and row["市区町村名"] == name_muni:
                filtered_rows.append(row["大字・丁目名"])
        return jpDataUtils.unique_list(filtered_rows)


    def get_details(self, name_pref, name_muni, name_town):
        self._load_csv(name_pref)
        rows = self._addr
        if rows is None:
            return None
        filtered_rows = []
        for row in rows:
            if row["都道府県名"] == name_pref and row["市区町村名"] == name_muni and row["大字・丁目名"] == name_town:
                filtered_rows.append(row["街区符号・地番"])
        return jpDataUtils.unique_list(filtered_rows)

    # For Tokyo (13) Year 2025
    #   url: https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13000-24.0a.zip
    #   zip: 13000-24.0a.zip   ({code_pref}000-{year2digit-1}.0a.zip)
    #   csv: 13_2025.csv       ({code_pref}_{year4digit}.csv) 

    def get_url(self, code_pref, year=None):
        if year is None:
            year = self._year
        year2digit = str(int(year) - 1)[2:]
        return (
            "https://nlftp.mlit.go.jp/isj/dls/data/" + year2digit + ".0a/"
            + str(code_pref).zfill(2)
            + "000-" + year2digit + ".0a.zip"
        )

    def get_zip(self, code_pref, year=None):
        if year is None:
            year = self._year
        year2digit = str(int(year) - 1)[2:]
        return str(code_pref).zfill(2) + "000-" + year2digit + ".0a.zip"

    def get_csv_fullpath(self, code_pref, year=None):
        if year is None:
            year = self._year
        year4digit = str(year)[:4]
        year2digit = str(int(year) - 1)[2:]
        fullpath = posixpath.join(
            self._download_fullpath,
            str(code_pref).zfill(2) + "000-" + year2digit + ".0a",
            str(code_pref).zfill(2) + "_" + year4digit + ".csv",
        )
        if os.path.exists(fullpath):
            return fullpath
        else:
            return None

    def _load_csv(self, name_pref, year=None, encoding="cp932"):
        code_pref = jpDataUtils.getPrefCodeByName(name_pref)
        if self._current_pref == code_pref:
            return
        if year is None:
            year = self._year
        year4digit = str(year)[:4]
        year2digit = str(int(year) - 1)[2:]
        csvfullpath = self.get_csv_fullpath(code_pref)
        if not csvfullpath:
            self.unzip_addr_data(code_pref)
        if csvfullpath:
            self._current_pref = code_pref
            self._addr = jpDataUtils.get_records_from_csv(csvfullpath, encoding=encoding)


    def _getMuniFromPrefName(self, name_pref):
        self._load_code_pref_muni()
        # No city name on top. For selected prefecture only.
        filtered_rows = []
        for row in self._code_pref_muni:
            if row["name_pref_" + self._lang] == name_pref:
                filtered_rows.append(row["name_muni_" + self._lang])
        return jpDataUtils.unique_list(filtered_rows)


    def _getMesh1FromPrefName(self, name_muni):
        self._load_code_muni_meshi1()
        filtered_rows = []
        for row in self._muni_mesh1:
            if len(row) >= 2 and row["name_muni"] == name_muni:
                filtered_rows.append(row)
        return filtered_rows

    def _getMesh3FromPrefName(self, name_muni):
        filePath = posixpath.join(os.path.dirname(__file__), "csv", "muni_mesh3.csv")
        filtered_rows = []
        with open(filePath, "r") as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
                if len(row) >= 2 and row["name_muni"] == name_muni:
                    filtered_rows.append(row)
        return filtered_rows

    def get_code_muni(self, name_pref, name_muni):
        row = self._getRowFromNames(name_pref, name_muni)
        return row["code_muni"]

    def _getRowFromNames(self, name_pref, name_muni):
        self._load_code_pref_muni()
        for row in self._code_pref_muni:
            if (
                len(row) >= 2
                and row["name_pref_" + self._lang] == name_pref
                and row["name_muni_" + self._lang] == name_muni
            ):
                row["code_pref"] = row["code_pref"].zfill(2)
                return row

    def get_all_designated_cities(self, year=None):
        """Return all the designated cities"""
        if year is None:
            year = self._year
        year_int = int(year)
        # The current list as of 2026
        if self._lang == "j":
            cities = {
                "札幌市", "仙台市", "千葉市", "さいたま市", "横浜市", "川崎市",
                "相模原市", "新潟市", "静岡市", "浜松市", "名古屋市", "京都市",
                "大阪市", "堺市", "神戸市", "岡山市", "広島市", "福岡市",
                "北九州市", "熊本市"
            }
        else:
            cities = {
                "Sapporo", "Sendai", "Chiba", "Saitama", "Yokohama", "Kawasaki",
                "Sagamihara", "Niigata", "Shizuoka", "Hamamatsu", "Nagoya", "Kyoto",
                "Osaka", "Sakai", "Kobe", "Okayama", "Hiroshima", "Fukuoka",
                "Kitakyushu", "Kumamoto"
            }

        # Discard cities by year
        if year_int < 2012:
            cities.discard("熊本市")
            cities.discard("Kumamoto")
        if year_int < 2010:
            cities.discard("相模原市")
            cities.discard("Sagamihara")
        if year_int < 2009:
            cities.discard("岡山市")
            cities.discard("Okayama")

        return cities

    def unzip_addr_data(self, code_pref, year=None):
        jpDataUtils.unzip(self._download_fullpath, self.get_zip(code_pref))


    def get_lonlat_by_addr(self, name_pref, name_muni, name_town, detail_code):
        if name_muni == "" or name_muni == "---":
            return self._get_lonlat_by_pref(name_pref)
        elif name_town == "" or name_town == "---":
            return self._get_lonlat_by_muni(name_pref, name_muni)
        elif detail_code == "" or detail_code == "---":
            return self._get_lonlat_by_town(name_pref, name_muni, name_town)
        else:
            return self._get_lonlat_by_detail(name_pref, name_muni, name_town, detail_code)
        return (None, None)

    def _get_lonlat_by_pref(self, name_pref):
        rows = self._code_pref_muni
        if rows is None:
            return (None, None)
        for row in rows:
            if (
                row["name_pref_" + self._lang] == name_pref
                and row["name_muni_" + self._lang] == ""
            ):
                return (float(row["X"]), float(row["Y"]))

    def _get_lonlat_by_muni(self, name_pref, name_muni):
        rows = self._code_pref_muni
        if rows is None:
            return (None, None)
        for row in rows:
            if (
                row["name_pref_" + self._lang] == name_pref
                and row["name_muni_" + self._lang] == name_muni
            ):
                if row["X"].isdigit() and row["Y"].isdigit():
                    return (float(row["X"]), float(row["Y"]))
                else:
                    return (None, None)


    def _get_lonlat_by_town(self, name_pref, name_muni, name_town):
        self._load_csv(name_pref)
        rows = self._addr
        if rows is None:
            return (None, None)
        for row in rows:
            if (
                row[1] == name_muni
                and row[2] == name_town
                and row[4] == ""
            ):
                return (float(row[9]), float(row[8]))

    def _get_lonlat_by_detail(self, name_pref, name_muni, name_town, detail_code):
        self._load_csv(name_pref)
        rows = self._addr
        if rows is None:
            return (None, None)
        for row in rows:
            if (
                row[1] == name_muni
                and row[2] == name_town
                and row[4] == detail_code
            ):
                return (float(row[9]), float(row[8]))

    def get_projections(self):
        dict_projection = {
            0: {"j": "正距方位図法", "e": "Azimuthal Equidistant"},
            1: {"j": "ランベルト正積方位図法", "e": "Lambert Azimuthal Equal Area"},
            2: {"j": "正射図法", "e": "Orthographic"},
        }
        projections = []
        for row in dict_projection.values():
            projections.append(row.get(self._lang, ""))
        return projections

    def get_proj_string(self, i, lat, lon):
        if lat is None or lon is None:
            return
        proj_strings = {
            0: "+proj=aeqd +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m +no_defs",
            1: "+proj=laea +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m +no_defs",
            2: "+proj=ortho +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m +no_defs"
        }
        proj_string = proj_strings[i]
        proj_string = proj_string.replace("{lat}", str(lat))
        proj_string = proj_string.replace("{lon}", str(lon))
        return proj_string
