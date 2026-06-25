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

    def __init__(self):
        self.download_fullpath = ""
        self.lang = "j"
        self.records = None
        self.mhlw_source_csv = "mhlw_source.csv"
        self.source = None

    def init(self):
        if self.records is None:
            self.load_records()

    def set_download_folder(self, download_fullpath):
        if not os.path.exists(posixpath.join(download_fullpath, "MHLW")):
            os.mkdir(posixpath.join(download_fullpath, "MHLW"))
        self.download_fullpath = posixpath.join(download_fullpath, "MHLW")

    def set_lang(self, lang):
        self.lang = lang[:1].lower()

    def load_records(self):
        self.records = jpDataUtils.get_records_from_csv("mhlw.csv", "name_" + self.lang)

    def get_records(self):
        return self.records 

    def get_years(self, name):
        self._set_source()
        years = []
        for row in self.source:
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

    def _set_source(self):
        if self.source is None:
            csv_full_path = posixpath.join(os.path.dirname(__file__), "csv", self.mhlw_source_csv)
            self.source = jpDataUtils.get_records_from_csv(csv_full_path)



    #  UI Handlers
    #
    #
    def populate_years(combo_widget, map_name):
        years = self.get_years(map_name)
        current_year = combo_widget.currentText()
        combo_widget.clear()
        for year in years:
            if year:
                combo_widget.addItem(year)
        # Restore selection if it still exists
        index = combo_widget.findText(current_year)
        if index != -1:
            combo_widget.setCurrentIndex(index)
        else:
            combo_widget.setCurrentIndex(0)

