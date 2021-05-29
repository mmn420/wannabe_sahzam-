import functions as tools

def connectSlider(self,slider,value):
    slider.valueChanged.connect(lambda: tools.sliderChange(self, slider, value))

def connectButton(self,button,label,index):
    button.clicked.connect(lambda: tools.browseFiles(self,label,index))

def connectSearch(self,button):
    button.clicked.connect(lambda: tools.compareHashes(self))