from createdb import create_db
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSettings
import functions as tools
import connects as ct
import sys
import os


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("app.ui", self)
        self.settings = QSettings("DSP", "Shazam")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
            self.slider.setValue(int(self.settings.value("slider")))
            self.sliderValue.setText(self.settings.value("sliderValue"))
        except:
            pass
        closeSongs = [self.close1, self.close2]
        openSongs = [self.openButton1, self.openButton2]
        songLabels = [self.song1, self.song2]
        for i in range(2):
            ct.connectButton(self, openSongs[i], songLabels[i], i)
            ct.connectClose(self, closeSongs[i], songLabels[i], i)
        ct.connectSearch(self, self.searchButton)
        ct.connectSlider(self, self.slider, self.sliderValue)

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())
        self.settings.setValue("slider", self.slider.value())
        self.settings.setValue("sliderValue", self.sliderValue.text())


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
# create_db("C:/Users/momen/Downloads/Music")
app.exec_()
