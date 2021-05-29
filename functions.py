from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
import librosa
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
from pydub import AudioSegment
from os import path
import imagehash
import json
from Song import Song

songs = [Song(),Song()]
def readSong(fname,index):
    if fname.endswith(".wav"):
            songs[index].samples , songs[index].sampling_rate = librosa.load(fname, sr=22050, mono=True, offset=0.0, duration=60)
            songs[index].hashes['Name'] = os.path.basename(fname)
    elif fname.endswith(".mp3"):
            songs[index].hashes['Name'] = os.path.basename(fname)
            new_name = fname.replace('.mp3','.wav')
            AudioSegment.from_mp3(fname).export(new_name, format="wav")
            songs[index].samples, songs[index].sampling_rate = librosa.load(new_name, sr=22050, mono=True, offset=0.0, duration=60)
            os.remove(new_name)
    songs[index].hashed_features()
    
def browseFiles(self,label,index):
    fname = QFileDialog.getOpenFileName(
        self, "Open file", "../", "*.mp3;;" " *.wav;;"
    )
    file_path = fname[0]
    extensionsToCheck = (".mp3", ".wav")
    if fname[0].endswith(extensionsToCheck):
        label.setText(os.path.basename(fname[0]))
        readSong(fname[0],index)
    elif fname[0]!="":
        QMessageBox.critical(self,"Error","Invalid format. Please select a file with a wav or mp3 format.")
        return

def sliderChange(self, slider, label):
    label.setText(str(slider.value()) + " %")

def mixer(self):
    if type(songs[0].samples)==int and type(songs[1].samples)==int:
        QMessageBox.critical(self,"Error","No file selected")
        return 0
    elif type(songs[0].samples)==int:
        return songs[1]
    elif type(songs[1].samples)==int:
        return songs[0]
    else:
        song1 = np.multiply(songs[0].samples, self.slider.value()/100)
        song2 = np.multiply(songs[1].samples, 1 - self.slider.value()/100)

        song = Song()
        song.samples = song1+song2
        song.hashed_features()
        return song

def compareHashes(self):
    song = mixer(self)
    if song==0:
        return
    similars = []
    with open("data.json", "r+") as file:
            dataInFile = json.load(file)
    for i in range (len(dataInFile['songs'])):
        mfcc_index = 1 - (imagehash.hex_to_hash(song.hashes["mfcc"]) - imagehash.hex_to_hash(dataInFile['songs'][i]['mfcc']))/256.0 
        mel_index = 1 - (imagehash.hex_to_hash(song.hashes["mel_spectrogram"]) - imagehash.hex_to_hash(dataInFile['songs'][i]['mel_spectrogram']))/256.0
        similars.append([(mfcc_index + mel_index)/2,os.path.basename(dataInFile['songs'][i]['Name'])])
    constuctTable(self,similars)

def addTableRow(table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1

def constuctTable(self,similars):
    self.table.setRowCount(0)
    similars.sort(key = lambda x:x[0],reverse=True)
    for item in similars:
        addTableRow(self.table,item)