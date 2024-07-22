# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QThread, pyqtSignal
import os
import requests


class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self):
        QThread.__init__(self)
        self._is_running = True

    def setUrl(self, url):
        self.url = url

    def setFilePath(self, file_path):
        self.file_path = file_path
    
    def setStatus(self, status_message):
        self.status_message = status_message

    def getStatus(self):
        return self.status_message

    def run(self):
        if self.url is None or self.file_path is None:
            return
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total_length = r.headers.get('content-length')

                with open(self.file_path, 'wb') as f:
                    if total_length is None:  # no content length header
                        f.write(r.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in r.iter_content(chunk_size=4096):
                            if not self._is_running:
                                self.setStatus('Download cancelled.')
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
        self._is_running = False
        self.remove()
    
    def remove(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def checkStatus(self):
        if os.path.exists(self.file_path):
            if os.stat(self.file_path).st_size == 0:
                self.setStatus('The zipfile exists but the filesize is zero.')
            else:
                try:
                    ret = self.file_path.testzip()
                    if ret is not None:
                        self.setStatus('The zipfile exists with a problem.')
                    else:
                        self.setStatus('The zipfile exists.')
                except Exception as ex:
                    self.setStatus('The zipfile exists but is corrupt.')
        else:
            self.setStatus('The zipfile does not exist.')
