# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils
from qgis.core import QgsMessageLog, Qgis
# QgsMessageLog.logMessage(str(len(self._code_pref_muni)), "jpdata", Qgis.Info)

# The CSV contains the codes and names of prefs and munis in Japan
#
# code_dantai	code_region	code_pref	code_muni	name_pref	name_muni	name_muni_kana


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
        self._lang = "j"
        self._download_fullpath = ""

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


    def _getMuniFromPrefCode(self, code_pref):
        self._load_code_pref_muni()
        # No city name on top. For selecting prefecture only.
        filtered_rows = [""]
        for row in self._code_pref_muni:
            if len(row) >= 2 and row["code_pref"] == code_pref:
                filtered_rows.append(row)
        return filtered_rows

    def _getMuniFromPrefName(self, name_pref):
        self._load_code_pref_muni()
        # No city name on top. For selecting prefecture only.
        filtered_rows = [""]
        from qgis.core import QgsMessageLog, Qgis
        
        for row in self._code_pref_muni:
            QgsMessageLog.logMessage("checking " + row["name_muni_j"], "jpdata", Qgis.Info)
            if row["name_pref_" + self._lang] == name_pref:
                filtered_rows.append(row["name_muni_" + self._lang])
        return filtered_rows


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
                and row["name_pref"] == name_pref
                and row["name_muni"] == name_muni
            ):
                row["code_pref"] = row["code_pref"].zfill(2)
                return row


    def get_all_designated_cities(self, year=2024, lang="j"):
        """Return all the designated cities"""
        year_int = int(year)
        # The current list as of 2026
        if lang == "ja":
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
