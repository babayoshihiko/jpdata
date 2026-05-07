# i18n.py
from qgis.PyQt.QtCore import QCoreApplication


class TR:
    X3_MESH = QCoreApplication.translate("jpData", "3rd Mesh")
    X4_MESH = QCoreApplication.translate("jpData", "4th Mesh")
    X5_MESH = QCoreApplication.translate("jpData", "5th Mesh")
    X6_MESH = QCoreApplication.translate("jpData", "6th Mesh")

    ADDRESS = QCoreApplication.translate("jpData", "Address")
    ADDRESS_MISSING = QCoreApplication.translate("jpData", "Address data is missing")
    ADD_TO_MAP = QCoreApplication.translate("jpData", "Add to Map")
    ADD_TO_MAP_TOOLTIP = QCoreApplication.translate(
        "jpData", "Add Shapefile as a Layer to Map on QGIS"
    )
    CANCEL = QCoreApplication.translate("jpData", "Cancel")
    CANCELLED = QCoreApplication.translate("jpData", "...Cancelled")
    CENSUS = QCoreApplication.translate("jpData", "Census")
    CENSUS_TYPE_TOOLTIP = QCoreApplication.translate(
        "jpData",
        "Nieghbourhood: population of cho, aza, etc.<br />3rd Mesh: 1 km mesh<br />4th Mesh: 500 m mesh<br />5th Mesh: 250 m mesh",
    )
    CENSUS_YEAR_TOOLTIP = QCoreApplication.translate(
        "jpData",
        "Nieghbourhood: Since 2000<br />1st throught 3rd: Since 1995<br />5th Mesh: Since2005<br />6th Mesh: Since2015",
    )
    CHOOSE_FOLDER = QCoreApplication.translate("jpData", "Choose Folder")
    CHOOSE_FOLDER_INIT = QCoreApplication.translate(
        "jpData", "Choose folder for zip/shp files"
    )
    CHOOSE_MAP_TYPE = QCoreApplication.translate("jpData", "Choose a map type")
    CHOOSE_MESH = QCoreApplication.translate("jpData", "Choose a mesh code")
    CHOOSE_MUNICIPALITY = QCoreApplication.translate("jpData", "Choose a municipality")
    CHOOSE_PREFECTURE = QCoreApplication.translate("jpData", "Choose a prefecture")
    CHOOSE_PREFECTURE_REGION = QCoreApplication.translate(
        "jpData", "Choose a prefecture or region"
    )
    DONE = QCoreApplication.translate("jpData", "...Done")
    DOWNLOAD = QCoreApplication.translate("jpData", "Download")
    DOWNLOAD_CENSUS = QCoreApplication.translate(
        "jpData", "Download census data by city"
    )
    DOWNLOAD_LNI = QCoreApplication.translate(
        "jpData", "Download Land Numerical Information data"
    )
    GSI_TILES = QCoreApplication.translate("jpData", "GSI Tiles")
    GSI_TILES_TOOLTIP = QCoreApplication.translate(
        "jpData", "Add GSI xyz tile server to Map on QGIS"
    )
    JUMP = QCoreApplication.translate("jpData", "Jump")
    LANDNUMINFO = QCoreApplication.translate("jpData", "LandNumInfo")
    NATIONWIDE = QCoreApplication.translate("jpData", "Nation-wide")
    NEIGHBOURHOOD = QCoreApplication.translate("jpData", "Neighbourhood")
    RUN = QCoreApplication.translate("jpData", "Run")
    SETTING = QCoreApplication.translate("jpData", "Setting")
    SETTING_BACKGROUND = QCoreApplication.translate(
        "jpData", "Turn off background download"
    )
    SETTING_GEOMETRY = QCoreApplication.translate(
        "jpData", "Check geometry validity when adding layers"
    )
    WEB = QCoreApplication.translate("jpData", "Web")
    WEB_TOOLTIP = QCoreApplication.translate(
        "jpData", "Open the webpage with the standard browser"
    )
    YEAR = QCoreApplication.translate("jpData", "Year")

    @staticmethod
    def CANNOT_FIND_FILE(name):
        template = QCoreApplication.translate("jpData", "Cannot find file: %1")
        return template.replace("%1", str(name))

    @staticmethod
    def CANNOT_FIND_FILE_LAYER(name):
        template = QCoreApplication.translate(
            "jpData", "Cannot find the file for layer: %1"
        )
        return template.replace("%1", str(name))

    @staticmethod
    def CANNOT_LOAD_LAYER(name):
        template = QCoreApplication.translate("jpData", "Cannot load the layer: %1")
        return template.replace("%1", str(name))

    @staticmethod
    def DOWNLOADING(name):
        template = QCoreApplication.translate("jpData", "Downloading: %1")
        return template.replace("%1", str(name))

    @staticmethod
    def FILE_EXISTS(name):
        template = QCoreApplication.translate("jpData", "The file already exists: %1")
        return template.replace("%1", str(name))

    @staticmethod
    def INVALID_EPSG(value):
        template = QCoreApplication.translate(
            "jpData", "Invalid EPSG: %1. Uses default instead."
        )
        return template.replace("%1", str(value))

    @staticmethod
    def INVALID_GEOM(value):
        template = QCoreApplication.translate(
            "jpData", "The layer has %1 invalid geometries."
        )
        return template.replace("%1", str(value))
