# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QThread, pyqtSignal
import os
import requests
import zipfile
import logging
from urllib.parse import quote

try:
    import certifi

    DEFAULT_CA = certifi.where()
except ImportError:
    DEFAULT_CA = True  # fallback to system store

# Set up logger (QGIS safe)
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._is_running = True
        self.proxy_server = None
        self.proxy_user = ""
        self.proxy_password = ""
        self.status_message = ""
        self.certificate = True  # default: verify SSL
        self.url = None
        self.file_path = None

    def setProxyServer(self, proxy_server):
        if proxy_server and len(proxy_server) > 10:
            self.proxy_server = proxy_server.strip()
        else:
            self.proxy_server = None

    def getProxyServer(self):
        _proxy_server = self._get_proxies()
        if not _proxy_server:
            return "No proxy set."
        else:
            return _proxy_server["http"]

    def setProxyUser(self, proxy_user):
        self.proxy_user = proxy_user.strip()

    def setProxyPassword(self, proxy_password):
        self.proxy_password = proxy_password.strip()

    def setUrl(self, url):
        self.url = url.strip()

    def setCertificate(self, certificate):
        # certificate can be bool or path
        self.certificate = certificate if certificate else DEFAULT_CA

    def setFilePath(self, file_path):
        self.file_path = file_path.strip()

    def setStatus(self, status_message):
        self.status_message = status_message
        logger.info(status_message)

    def getStatus(self):
        return self.status_message

    def download_wo_thread(self):
        """Simple blocking download (no signals)."""
        if not self.url or not self.file_path:
            self.setStatus("URL or file path not set.")
            return False

        proxies = self._get_proxies()
        try:
            with requests.get(
                self.url,
                stream=True,
                proxies=proxies,
                verify=self.certificate,
                timeout=30,
            ) as r:
                r.raise_for_status()
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                with open(self.file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            self.checkStatus()
            return True
        except Exception as e:
            self.setStatus(f"Download failed: {e}")
            return False

    def run(self):
        """Threaded download with progress signal."""
        if not self.url or not self.file_path:
            self.setStatus("URL or file path not set.")
            return

        proxies = self._get_proxies()

        try:
            with requests.get(
                self.url,
                stream=True,
                proxies=proxies,
                verify=self.certificate,
                timeout=30,
            ) as r:
                r.raise_for_status()
                total_length = r.headers.get("content-length")

                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
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
                            if data:
                                dl += len(data)
                                f.write(data)
                                self.progress.emit(int(100 * dl / total_length))
            self.checkStatus()
            self.finished.emit(True)

        except Exception as e:
            self.setStatus(f"Download failed: {e}")
            self.finished.emit(False)

    def stop(self):
        self._is_running = False
        self.setStatus("Download cancelled and removed: " + str(self.file_path))
        self.remove()

    def remove(self):
        if self.file_path and os.path.exists(self.file_path):
            os.remove(self.file_path)

    def checkStatus(self):
        """Check if downloaded file is valid ZIP."""
        if not self.file_path:
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
                        self.setStatus(
                            "The zipfile exists and is valid: " + self.file_path
                        )
                except Exception:
                    self.setStatus(
                        "The zipfile exists but may be corrupt: " + self.file_path
                    )
        else:
            self.setStatus("The zipfile does not exist: " + self.file_path)

    def _get_proxies(self):
        """Build proxy dict for requests."""
        proxies = None
        if not self.proxy_server:
            return proxies

        user_pass = ""
        if self.proxy_user:
            user_pass = quote(self.proxy_user)
            if self.proxy_password:
                user_pass += ":" + quote(self.proxy_password)
            user_pass += "@"

        if self.proxy_server.lower().startswith("https://"):
            proxy_host = self.proxy_server.replace("https://", "")
        elif self.proxy_server.lower().startswith("http://"):
            proxy_host = self.proxy_server.replace("http://", "")
        else:
            proxy_host = self.proxy_server

        proxies = {
            "http": f"http://{user_pass}{proxy_host}",
            "https": f"http://{user_pass}{proxy_host}",
        }
        return proxies
