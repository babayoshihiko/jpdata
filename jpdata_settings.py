# -*- coding: utf-8 -*-
from qgis.core import QgsSettings


class jpDataSettings:
    """
    Plugin settings wrapper.
    """

    _instance = None
    PREFIX = "jpdata"

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._settings = QgsSettings()

        # Session only (not persisted)
        self.proxy_user = ""
        self.proxy_password = self.proxy_user
        self.current_tab = 0
        self.lang2 = self.locale
        self.lang1 = self.lang2[:1]

    # ------------------------------------------------------------------
    # Persistent settings
    # ------------------------------------------------------------------

    @property
    def folder_path(self):
        return self._settings.value(
            f"{self.PREFIX}/FolderPath",
            "",
            type=str,
        )

    @folder_path.setter
    def folder_path(self, value):
        self._settings.setValue(
            f"{self.PREFIX}/FolderPath",
            value,
        )

    @property
    def geometry_check(self):
        return self._settings.value(
            f"{self.PREFIX}/General/GeometryCheck",
            True,
            type=bool,
        )

    @geometry_check.setter
    def geometry_check(self, value):
        self._settings.setValue(
            f"{self.PREFIX}/General/GeometryCheck",
            value,
        )

    @property
    def proxy_server(self):
        return self._settings.value(
            f"{self.PREFIX}/ProxyServer",
            "",
            type=str,
        )

    @proxy_server.setter
    def proxy_server(self, value):
        self._settings.setValue(
            f"{self.PREFIX}/ProxyServer",
            value,
        )

    # ------------------------------------------------------------------
    # Read only (QGIS)
    # ------------------------------------------------------------------

    @property
    def locale(self):
        locale = self._settings.value(
            "locale/userLocale",
            "en",
            type=str,
        )
        return locale.lower()[:2]
