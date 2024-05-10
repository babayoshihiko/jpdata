# -*- coding: utf-8 -*-
import urllib.request
from PyQt5.QtWidgets import *
import sys
 
class Downloader(QWidget):
 
    def __init__(self):
        super().__init__()

    def setProgressBar (self, progressBar):
        self._progressBar = progressBar

    def SetUrl (self, url, filename):
        self._url = url
        self._filename = filename

    # when push button is pressed, this method is called
    def Handle_Progress(self, blocknum, blocksize, totalsize):

        ## calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self._progressBar.setValue(download_percentage)
            QApplication.processEvents()

    # method to download any file using urllib
    def Download(self, url, filename):

        # Downloading using urllib
        urllib.request.urlretrieve(url, filename, self.Handle_Progress)
