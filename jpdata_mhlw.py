# -*- coding: utf-8 -*-
import os, csv, posixpath
from . import jpDataUtils


class jpDataMHLW:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, download_fullpath, lang="j"):
        self.download_fullpath = ""
        self.set_download_folder(download_fullpath)
        self.mhlw_source_csv = "mhlw_source.csv"
        self.lang = lang
        self.records = []

    def set_download_folder(self, download_fullpath):
        if not os.path.exists(posixpath.join(download_fullpath, "MHLW")):
            os.mkdir(posixpath.join(download_fullpath, "MHLW"))
        self.download_fullpath = posixpath.join(download_fullpath, "MHLW")

    def load_records(self):
        self.records = jpDataUtils.get_records_from_csv("mhlw.csv", "name_" + self.lang)

    def get_records(self):
        return self.records 

    def get_years(self, name):
        filePath = posixpath.join(os.path.dirname(__file__), "csv", self.mhlw_source_csv)
        years = []
        with open(filePath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("name_j") == name or row.get("name_e") == name:
                    year = row.get("year")
                    if year:
                        years.append(year)
        return years

    def get_zip(
        self, year, name_map, type="urlzip"
    ):
        filePath = posixpath.join(os.path.dirname(__file__), "csv", self.mhlw_source_csv)
        with open(filePath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row.get("name_j") == name_map or row.get("name_e") == name_map) and row.get("year") == year:

                    tempSubFolder = posixpath.join("MHLW",year)
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
                        if row.get("code_map","")[:4] == "LTCI":
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
                            yField
                        )
        return None