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
                                self.finished.emit(False)
                                return
                            dl += len(data)
                            f.write(data)
                            self.progress.emit(int(100 * dl / total_length))
            self.finished.emit(True)


        except Exception as e:
            self.finished.emit(False)

    def stop(self):
        self._is_running = False
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
