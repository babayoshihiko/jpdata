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

    # For Tokyo (13) Year 2025
    #   url: https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13000-24.0a.zip
    #   zip: 13000-24.0a.zip   ({code_pref}000-{year2digit-1}.0a.zip)
    #   csv: 13_2025.csv       ({code_pref}_{year4digit}.csv) 

    def get_url(rowself, pref_code, year=2024):
        year2digit = str(year - 1)[:2]
        return (
            "https://nlftp.mlit.go.jp/isj/dls/data/" + year2digit + ".0a/"
            + str(pref_code).zfill(2)
            + "000-" + year2digit + ".0a.zip"
        )

    def get_zip(rowself, pref_code, year=2024):
        year2digit = str(year - 1)[:2]
        return str(pref_code).zfill(2) + "000-" + year2digit + ".0a.zip"

    def get_csv_fullpath(rowself, pref_code, year=2024):
        year4digit = str(year)[:4]
        year2digit = str(year - 1)[:2]
        fullpath = posixpath.join(
            folder,
            "Addr",
            str(pref_code).zfill(2) + "000-" + year2digit + ".0a",
            str(pref_code).zfill(2) + "_" + year4digit + ".csv",
        )
        if os.path.exists(os.path.normpath(fullpath)):
            return fullpath
        else:
            return None

    def _load_csv(pref_code, year=2024, encoding="cp932"):
        pref_code = str(pref_code).zfill(2)
        if self._current_pref == pref_code:
            return
        year4digit = str(year)[:4]
        year2digit = str(year - 1)[:2]
        csvfullpath = get_csv_fullpath(year, pref_code)
        if csvfullpath:
            self._current_pref = pref_code
            self._addr = jpDataUtils.get_records_from_csv(csvfullpath)


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

    # def get_munis_by_pref(pref_name):
    #     Muni = jpDataMuni.instance()
    #     rows = self.get_munis(pref_name)
    #     return rows

    def _get_towns_by_municode(self, folder, pref_name, city_name):
        pref_code = jpDataUtils.getPrefCodeByName(pref_name)
        rows = _load_csv(folder, pref_code)
        if rows is None:
            return False

        towns = [row[2] for row in rows if len(row) > 2 and row[1] == city_name]
        return sorted(set(towns))


    def _get_details_by_town(self, folder, pref_name, city_name, town_name):
        pref_code = jpDataUtils.getPrefCodeByName(pref_name)
        rows = _load_csv(folder, pref_code)
        if rows is None:
            return False

        details = [
            row[4]
            for row in rows
            if len(row) > 5 and row[1] == city_name and row[2] == town_name
        ]
        return sorted(set(details))


    def unzip_addr_data(self, year):
        for pref_code in range(1, 48):
            if os.path.exists(
                posixpath.join(self._download_fullpath, self.get_zip(year, pref_code))
            ) and not os.path.exists(
                posixpath.join(self._download_fullpath, self.get_csv_fullpath(year, pref_code))
            ):
                jpDataUtils.unzip(self._download_fullpath, self.get_zip(year, pref_code))


    def get_lonlat_by_addr(self, name_pref, name_muni, name_town, detail_code):
        jpDataUtils.printDebugLog(name_town)
        if not name_town:
            rows = self._code_pref_muni
            if rows is None:
                return (None, None)

            for row in rows:
                if (
                    row["name_pref_" + self._lang] == name_pref
                    and row["name_muni_" + self._lang] == name_muni
                ):
                    return (float(row["X"]), float(row["Y"]))  # lon, lat
        else:
            pref_code = jpDataUtils.getPrefCodeByName(pref_name)
            rows = self._load_csv(folder, pref_code)
            if rows is None:
                return (None, None)

            for row in rows:
                if (
                    row[1] == name_muni
                    and row[2] == name_town
                    and row[4] == detail_code
                ):
                    return (float(row[9]), float(row[8]))  # lon, lat
        return (None, None)

