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
            songs[index].hashes['Name'] = os.path.basename(fname)
    elif fname.endswith(".mp3"):
            songs[index].hashes['Name'] = os.path.basename(fname)
            new_name = fname.replace('.mp3','.wav')
            AudioSegment.from_mp3(fname).export(new_name, format="wav")
            songs[index].samples, songs[index].samping_rate = librosa.load(new_name, sr=22050, mono=True, offset=0.0, duration=60)
            os.remove(new_name)
    hashed_features(songs[index])
    # json_data(songs[index])
    compareHashes(songs[index])

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
        return

def hashed_features(song):
    windowType="hann"
    windowSize = 1024
    hop_length = 512

    song.hashes["mfcc"] = str(imagehash.phash(Image.fromarray(librosa.feature.mfcc(song.samples)), hash_size=16))
    song.hashes["mel_spectrogram"] = str(imagehash.phash(Image.fromarray(librosa.feature.melspectrogram(song.samples)), hash_size=16))

def json_data(song):        
    if os.path.isfile('data.json'):
        with open("data.json", "r+") as file:
            dataInFile = json.load(file)
            dataInFile['songs'].append(song.hashes)
            file.seek(0)
            json.dump(dataInFile, file, indent=4)
    else:
        data = {}
        data['songs'] = []
        data['songs'].append(song.hashes)
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

def sliderChange(self, slider, label):
    label.setText(str(slider.value()) + " %")

def compareHashes(song):
    with open("data.json", "r+") as file:
            dataInFile = json.load(file)
    for i in range (len(dataInFile['songs'])):
        mfcc_index = 1 - (imagehash.hex_to_hash(song.hashes["mfcc"]) - imagehash.hex_to_hash(dataInFile['songs'][i]['mfcc']))/256.0 
        mel_index = 1 - (imagehash.hex_to_hash(song.hashes["mel_spectrogram"]) - imagehash.hex_to_hash(dataInFile['songs'][i]['mel_spectrogram']))/256.0
        print (os.path.basename(dataInFile['songs'][i]['Name']) , (mfcc_index + mel_index)/2)




