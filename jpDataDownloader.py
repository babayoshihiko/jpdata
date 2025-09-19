# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QThread, pyqtSignal
import os
import requests
import zipfile
from urllib.parse import quote


class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self):
        QThread.__init__(self)
        self._is_running = True
        self.proxy_server = None
        self.proxy_user = ""
        self.proxy_password = ""
        self.status_message = ""
        self.certificate = False


    def setProxyServer(self, proxy_server):
        if len(proxy_server) > 10:
            self.proxy_server = proxy_server
        else:
            self.proxy_server = None

    def setProxyUser(self, proxy_user):
        self.proxy_user = proxy_user.strip()

    def setProxyPassword(self, proxy_password):
        self.proxy_password = proxy_password.strip()

    def setUrl(self, url):
        self.url = url

    def setCertificate(self, certificate):
        self.certificate = certificate

    def setFilePath(self, file_path):
        self.file_path = file_path

    def setStatus(self, status_message):
        self.status_message = status_message

    def getStatus(self):
        return self.status_message

    def download_wo_thread(self):
        if self.url is None or self.file_path is None:
            return
        proxies = self._get_proxies()

        with requests.get(self.url, stream=True, verify=self.certificate) as r:
            r.raise_for_status()
            with open(self.file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def run(self):
        if self.url is None or self.file_path is None:
            return
        proxies = self._get_proxies()

        try:
            with requests.get(self.url, stream=True, proxies=proxies, verify=self.certificate) as r:
                r.raise_for_status()
                total_length = r.headers.get("content-length")

                with open(self.file_path, "wb") as f:
                    if total_length is None:  # no content length header
                        f.write(r.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in r.iter_content(chunk_size=4096):
                            if not self._is_running:
                                self.finished.emit(False)
                                return
                            dl += len(data)
                            f.write(data)
                            self.progress.emit(int(100 * dl / total_length))
            self.checkStatus()
            self.finished.emit(True)

        except Exception as e:
            self.setStatus(str(e))
            self.finished.emit(False)

    def stop(self):
        self.setStatus("Download cancelled and removed: " + self.file_path)
        self._is_running = False
        self.remove()

    def remove(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def checkStatus(self):
        if self.file_path is None:
            self.setStatus("The zipfile has not been defined.")
            return
        if os.path.exists(self.file_path):
            if os.stat(self.file_path).st_size == 0:
                self.setStatus(
                    "The zipfile exists but the filesize is zero: " + self.file_path
                )
            else:
                try:
                    ret = zipfile.ZipFile(self.file_path).testzip()
                    if ret is not None:
                        self.setStatus(
                            "The zipfile exists with a problem: " + self.file_path
                        )
                    else:
                        self.setStatus("The zipfile exists: " + self.file_path)
                except Exception as ex:
                    self.setStatus(
                        "The zipfile exists but may be corrupt: " + self.file_path
                    )
        else:
            self.setStatus("The zipfile does not exist:" + self.file_path)

    def _get_proxies():
        proxies = None
        _proxy_user_password = ""
        if self.url is None or self.file_path is None:
            return
        if self.proxy_server is not None:
            if self.proxy_user != "":
                _proxy_user_password = quote(self.proxy_user) + ":" + (quote(self.proxy_password) + "@"


            if self.proxy_server[:8].lower() = "https://":
                _proxy_server = self.proxy_server.replace("https://", "")
                proxies = {
                    "http": "http://" + _proxy_user_password + _proxy_server,
                    "https": "http://" + _proxy_user_password + _proxy_server,
                }
            else:
                _proxy_server = self.proxy_server.replace("http://", "")
                proxies = {
                    "http": "http://" + _proxy_user_password + _proxy_server,
                    "https": "http://" + _proxy_user_password + _proxy_server,
                }

        return proxies
