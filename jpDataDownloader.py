# -*- coding: utf-8 -*-
import urllib.request
from qgis.PyQt.QtWidgets import QApplication, QWidget, QProgressBar
import sys
 
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
            download_percentage = readed_data * 100 / totalsize
            if self._progressBar is not None:
                self._progressBar.setValue(download_percentage)
            QApplication.processEvents()

    # method to download any file using urllib
    def Download(self, url, filename, progressBar):
        self._progressBar = progressBar
        urllib.request.urlretrieve(url, filename, self.Handle_Progress)
        self._progressBar.setValue(100)
