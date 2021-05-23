import functions as tools

def connectButton(self,button,label,index):
    button.clicked.connect(lambda: tools.browseFiles(self,label,index))