from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import librosa
import librosa.display
import os
from librosa.core.harmonic import salience
from librosa.feature.spectral import mfcc, spectral_centroid, spectral_rolloff, tonnetz
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
from pydub import AudioSegment
from os import path
import imagehash
from PIL import Image
import shutil
import json
from Song import Song

songs = [Song(),Song()]
def readSong(fname,index):
    if fname.endswith(".wav"):
            songs[index].samples , songs[index].sampling_rate = librosa.load(fname, sr=22050, mono=True, offset=0.0, duration=60)
            songs[index].hashes['Name'] = fname
    elif fname.endswith(".mp3"):
            songs[index].hashes['Name'] = fname
            new_name = fname.replace('.mp3','.wav')
            AudioSegment.from_mp3(fname).export(new_name, format="wav")
            songs[index].samples, songs[index].samping_rate = librosa.load(new_name, sr=22050, mono=True, offset=0.0, duration=60)
            os.remove(new_name)
    hashed_features(songs[index])
    json_data(songs[index])

def browseFiles(self,label,index):
    fname = QFileDialog.getOpenFileName(
        self, "Open file", "../", "*.mp3;;" " *.wav;;"
    )
    file_path = fname[0]
    extensionsToCheck = (".mp3", ".wav")
    if fname[0].endswith(extensionsToCheck):
        label.setText(os.path.basename(fname[0]))
        readSong(fname[0],index)
    else:
        QMessageBox.critical("Error",text="Invalid format. Please select a file with a wav or mp3 format.")

def hashed_features(song):
    windowType="hann"
    windowSize = 1024
    hop_length = 512

    song.hashes["mfcc"] = str(imagehash.phash(Image.fromarray(librosa.feature.mfcc(song.samples))))
    song.hashes["mel_spectrogram"] = str(imagehash.phash(Image.fromarray(librosa.feature.melspectrogram(song.samples))))

def json_data(song):        
    if os.path.isfile('data.json'):
        with open("data.json", "r+") as file:
            dataInFile = json.load(file)
            dataInFile['songs'].append(song.hashes)
            file.seek(0)
            json.dump(dataInFile, file)
    else:
        data = {}
        data['songs'] = []
        data['songs'].append(song.hashes)
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

def sliderChange(self, slider, label):
    label.setText(str(slider.value()) + " %")


