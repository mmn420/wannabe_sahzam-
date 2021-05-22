from PyQt5 import QtWidgets, uic
# import shazam as tools
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("app.ui", self)
        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()