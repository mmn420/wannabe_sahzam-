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
import imagehash
from PIL import Image
import shutil
import json

class Song:
    def __init__(self, name, samples, sampling_rate, spectrogram, features):
        self.name = name
        self.samples = samples
        self.sampling_rate = sampling_rate
        self.spectrogram = spectrogram
        self.hashes = {}

def readSong(self, fname):
    if fname.endswith(".wav"):
            self.samples , self.sampling_rate = librosa.load(fname, sr=22050, mono=True, offset=0.0, duration=60)
            self.hashes['Name'] = fname
    elif fname.endswith(".mp3"):
            self.hashes['Name'] = fname
            new_name = fname.replace('.mp3','.wav')
            AudioSegment.from_mp3(fname).export(new_name, format="wav")
            self.samples, self.samping_rate = librosa.load(new_name, sr=22050, mono=True, offset=0.0, duration=60)
            shutil.move(new_name, dst=f"{os.getcwd()}\temp")

def browseFiles(self):
    fname = QFileDialog.getOpenFileName(
        self, "Open file", "../", "*.mp3;;" " *.wav;;"
    )
    file_path = fname[0]
    extensionsToCheck = (".mp3", ".wav")
    if fname[0].endswith(extensionsToCheck):
        readSong(fname[0])
    else:
        QMessageBox.critical("Error",text="Invalid format. Please select a file with a wav or mp3 format.")

def hashed_features(self, samples, sampling_rate):
    windowType="hann"
    windowSize = 1024
    hop_length = 512

    self.hashes["Chromagram"] = str(imagehash.phash(Image.fromarray(librosa.feature.chroma_stft(samples, n_fft=windowSize, hop_length=hop_length, window=windowType))))
    self.hashes["mfcc"] = str(imagehash.phash(Image.fromarray(librosa.feature.mfcc(samples, sr=sampling_rate))))
    self.hashes["tonnal_centroid"] = str(imagehash.phash(Image.fromarray(librosa.feature.tonnetz(samples))))
    self.hashes["tonnetz"] = str(imagehash.phash(Image.fromarray(librosa.feature.chroma_cens(samples, hop_length=hop_length))))
    self.hashes["mel_spectrogram"] = str(imagehash.phash(Image.fromarray(librosa.feature.melspectrogram(samples, n_fft=windowSize, hop_length=hop_length, window=windowType))))

def json_data(self):        
    if os.path.isfile('data.json'):
        with open("data.json", "r+") as file:
            dataInFile = json.load(file)
            dataInFile['songs'].append(self.hashes)
            file.seek(0)
            json.dump(dataInFile, file)
    else:
        data = {}
        data['songs'] = []
        data['songs'].append(self.hashes)
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)


