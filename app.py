from PyQt5 import QtWidgets, uic
import functions as tools
import connects as ct
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("app.ui", self)

        openSongs = [self.openButton1, self.openButton2]
        songLabels = [self.song1,self.song2]
        for i in range(2):
            ct.connectButton(self,openSongs[i],songLabels[i],i)
        self.slider.valueChanged.connect(lambda: tools.sliderChange(self, self.slider, self.sliderValue))
        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()