# i18n.py
import os
from qgis.PyQt.QtCore import (
    QCoreApplication,
    QSettings,
    QTranslator,
    QT_VERSION_STR
)


class TR:

    @staticmethod
    def X3_MESH():
        return QCoreApplication.translate("jpData", "3rd Mesh")

    @staticmethod
    def X4_MESH():
        return QCoreApplication.translate("jpData", "4th Mesh")

    @staticmethod
    def X5_MESH():
        return QCoreApplication.translate("jpData", "5th Mesh")

    @staticmethod
    def X6_MESH():
        return QCoreApplication.translate("jpData", "6th Mesh")

    @staticmethod
    def ADDRESS():
        return QCoreApplication.translate("jpData", "Address")

    @staticmethod
    def ADDRESS_MISSING():
        return QCoreApplication.translate(
            "jpData",
            "Address data is missing"
        )

    @staticmethod
    def ADD_TO_MAP():
        return QCoreApplication.translate("jpData", "Add to Map")

    @staticmethod
    def ADD_TO_MAP_TOOLTIP():
        return QCoreApplication.translate(
            "jpData",
            "Add Shapefile as a Layer to Map on QGIS"
        )

    @staticmethod
    def CANCEL():
        return QCoreApplication.translate("jpData", "Cancel")

    @staticmethod
    def CANCELLED():
        return QCoreApplication.translate("jpData", "...Cancelled")

    @staticmethod
    def CENSUS():
        return QCoreApplication.translate("jpData", "Census")

    @staticmethod
    def CENSUS_TYPE_TOOLTIP():
        return QCoreApplication.translate(
            "jpData",
            "Nieghbourhood: population of cho, aza, etc.<br />3rd Mesh: 1 km mesh<br />4th Mesh: 500 m mesh<br />5th Mesh: 250 m mesh",
        )

    @staticmethod
    def CENSUS_YEAR_TOOLTIP():
        return QCoreApplication.translate(
            "jpData",
            "Nieghbourhood: Since 2000<br />1st throught 3rd: Since 1995<br />5th Mesh: Since2005<br />6th Mesh: Since2015",
        )

    @staticmethod
    def CHOOSE_FOLDER():
        return QCoreApplication.translate("jpData", "Choose Folder")

    @staticmethod
    def CHOOSE_FOLDER_INIT():
        return QCoreApplication.translate(
            "jpData",
            "Choose folder for zip/shp files"
        )

    @staticmethod
    def CHOOSE_MAP_TYPE():
        return QCoreApplication.translate("jpData", "Choose a map type")

    @staticmethod
    def CHOOSE_MESH():
        return QCoreApplication.translate("jpData", "Choose a mesh code")

    @staticmethod
    def CHOOSE_MUNICIPALITY():
        return QCoreApplication.translate(
            "jpData",
            "Choose a municipality"
        )

    @staticmethod
    def CHOOSE_PREFECTURE():
        return QCoreApplication.translate(
            "jpData",
            "Choose a prefecture"
        )

    @staticmethod
    def CHOOSE_PREFECTURE_REGION():
        return QCoreApplication.translate(
            "jpData",
            "Choose a prefecture or region"
        )

    @staticmethod
    def DONE():
        return QCoreApplication.translate("jpData", "...Done")

    @staticmethod
    def DOWNLOAD():
        return QCoreApplication.translate("jpData", "Download")

    @staticmethod
    def DOWNLOAD_CENSUS():
        return QCoreApplication.translate(
            "jpData",
            "Download census data by city"
        )

    @staticmethod
    def DOWNLOAD_LNI():
        return QCoreApplication.translate(
            "jpData",
            "Download Land Numerical Information data"
        )

    @staticmethod
    def GSI_TILES():
        return QCoreApplication.translate("jpData", "GSI Tiles")

    @staticmethod
    def GSI_TILES_TOOLTIP():
        return QCoreApplication.translate(
            "jpData",
            "Add GSI xyz tile server to Map on QGIS"
        )

    @staticmethod
    def JUMP():
        return QCoreApplication.translate("jpData", "Jump")

    @staticmethod
    def LANDNUMINFO():
        return QCoreApplication.translate("jpData", "LandNumInfo")

    @staticmethod
    def NATIONWIDE():
        return QCoreApplication.translate("jpData", "Nation-wide")

    @staticmethod
    def NEIGHBOURHOOD():
        return QCoreApplication.translate("jpData", "Neighbourhood")

    @staticmethod
    def RUN():
        return QCoreApplication.translate("jpData", "Run")

    @staticmethod
    def SETTING():
        return QCoreApplication.translate("jpData", "Setting")

    @staticmethod
    def SETTING_BACKGROUND():
        return QCoreApplication.translate(
            "jpData",
            "Turn off background download"
        )

    @staticmethod
    def SETTING_GEOMETRY():
        return QCoreApplication.translate(
            "jpData",
            "Check geometry validity when adding layers"
        )

    @staticmethod
    def WEB():
        return QCoreApplication.translate("jpData", "Web")

    @staticmethod
    def WEB_TOOLTIP():
        return QCoreApplication.translate(
            "jpData",
            "Open the webpage with the standard browser"
        )

    @staticmethod
    def YEAR():
        return QCoreApplication.translate("jpData", "Year")

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


    def setup_translation(plugin_dir, plugin_name):
        locale = QSettings().value('locale/userLocale')[0:2]

        qt_major = QT_VERSION_STR.split('.')[0]

        locale_path = os.path.join(
            plugin_dir,
            'i18n',
            f'qt{qt_major}',
            f'{plugin_name}_{locale}.qm'
        )

        if os.path.exists(locale_path):
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)
            return translator

        return None