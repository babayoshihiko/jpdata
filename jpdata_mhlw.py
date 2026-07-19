# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils
from .jpdata_settings import jpDataSettings


class jpDataMHLW:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._download_fullpath = ""
        self._lang = "j"
        self.settings = jpDataSettings.instance()
        self._records = None
        self._source = None

    def init(self):
        if self._records is None:
            self.load_records()

    def set_download_folder(self, download_fullpath):
        if not os.path.exists(download_fullpath):
            return False
        if not os.path.exists(posixpath.join(download_fullpath, "MHLW")):
            os.mkdir(posixpath.join(download_fullpath, "MHLW"))
        self._download_fullpath = posixpath.join(download_fullpath, "MHLW")
        return True

    def set_lang(self, lang):
        self._lang = lang[:1].lower()

    def load_records(self):
        self._records = jpDataUtils.get_records_from_csv(
            "MHLW.csv", "name_" + self.settings.lang1
        )

    def get_records(self):
        return self._records

    def get_record(self, name_map, year):
        self._set_source()
        for row in self._source:
            if (
                row.get("name_j") == name_map or row.get("name_e") == name_map
            ) and row.get("year") == year:
                row["subfolder"] = posixpath.join("MHLW", year)
                row["epsg"] = "6668"
                row["encoding"] = "UTF-8"
                row["zip_fullpath"] = posixpath.join(
                    self.settings.folder_path, row["subfolder"], row.get("zip")
                )
                row["shp_fullpath"] = posixpath.join(
                    self.settings.folder_path, row["subfolder"], row.get("shp")
                )
                return row

    def get_years(self, name):
        self._set_source()
        years = []
        for row in self._source:
            if row.get("name_j") == name or row.get("name_e") == name:
                year = row.get("year")
                if year:
                    years.append(year)
        return years

    def get_zip(self, year, name_map, type="urlzip"):
        self._set_source()
        for row in self._source:
            if (
                row.get("name_j") == name_map or row.get("name_e") == name_map
            ) and row.get("year") == year:

                tempSubFolder = posixpath.join("MHLW", year)
                tempUrl = row.get("url")
                tempZip = row.get("zip")
                tempShp = row.get("shp")
                tempAltdir = ""
                tempQml = row.get("qml")
                tempEpsg = "6668"
                tempEncoding = "UTF-8"
                tempLayerName = name_map + " (" + year + ")"

                if type == "urlzip":
                    return tempUrl, tempZip, tempSubFolder
                else:
                    if row.get("code_map", "")[:4] == "LTCI":
                        xField = "経度"
                        yField = "緯度"
                    else:
                        xField = "事業所経度"
                        yField = "事業所緯度"
                    return (
                        tempZip,
                        tempShp,
                        tempAltdir,
                        tempQml,
                        tempEpsg,
                        tempEncoding,
                        tempSubFolder,
                        tempLayerName,
                        xField,
                        yField,
                    )
        return None

    def _set_source(self):
        if self._source is None:
            csv_full_path = posixpath.join(
                os.path.dirname(__file__), "csv", "MHLW_source.csv"
            )
            self._source = jpDataUtils.get_records_from_csv(csv_full_path)
