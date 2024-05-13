# -*- coding: utf-8 -*-
from qgis.core import QgsMessageLog, Qgis
from qgis.PyQt.QtWidgets import QApplication, QWidget, QProgressBar
import sys
import urllib.request
import zipfile
 
class Downloader(QWidget):
 
    def __init__(self):
        super().__init__()

    def setProgressBar (self, progressBar):
        self._progressBar = progressBar

    # when push button is pressed, this method is called
    def Handle_Progress(self, blocknum, blocksize, totalsize):

        ## calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = int(readed_data * 100 / totalsize)
            if self._progressBar is not None:
                self._progressBar.setValue(download_percentage)
            QApplication.processEvents()

    # method to download any file using urllib
    def Download(self, url, filename, progressBar):
        self._progressBar = progressBar
        self._progressBar.setValue(0)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                content_type = response.headers.get('Content-Type')
                if content_type == 'application/zip':
                    urllib.request.urlretrieve(url, filename, self.Handle_Progress)
                    self._progressBar.setValue(100)
                    try:
                        with zipfile.ZipFile(filename, 'r') as zip_ref:
                            # Check if the zipfile is readable
                            zip_ref.testzip()
                            return True
                    except zipfile.BadZipFile:
                        QgsMessageLog.logMessage('The downloaded zipfile is corrupt.', 'jpdata', level=Qgis.Warning)
                        return False  # Zipfile is corrupt
        except urllib.error.URLError as e:
            QgsMessageLog.logMessage(str(e) + ' (' + url + ')', 'jpdata', level=Qgis.Warning)
            return False  # Zipfile is corrupt

