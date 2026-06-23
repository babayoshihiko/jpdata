# -*- coding: utf-8 -*-
import os
import csv
import posixpath
from . import jpDataUtils


class JPDataMHLW:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # --------------------------------------------------
    # init（UIなし）
    # --------------------------------------------------

    def init(self, download_dir):

        self.download_dir = download_dir

        self.df_mhlw = jpDataUtils.get_map_list_from_csv("mhlw.csv")
        self.mhlw_source_csv = "mhlw_source.csv"


    # --------------------------------------------------
    # selection logic（UIから呼ばれる）
    # --------------------------------------------------


    def get_names(self, lang="j"):
        return self.df_mhlw 


    def get_years(self, name_j, lang="j"):
        filePath = posixpath.join(os.path.dirname(__file__), "csv", self.mhlw_source_csv)
        years = []
        with open(filePath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("name_j") == name_j or row.get("name_e") == name_j :
                    year = row.get("year")
                    if year:
                        years.append(year)
        return years


    def get_zip(
        self, year, name_map, type="urlzip", lang="j"
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