import librosa
import os
import numpy as np
import imagehash
import json
import logging
import logging.config
from getSystemInfo import getSystemInfo
from Song import Song
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from pydub import AudioSegment
from os import path

logging.basicConfig(
    filename="log.txt",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=20,
)
logging.info(f"System info: {json.loads(getSystemInfo())}")

songs = [Song(), Song()]


def readSong(fname, index):
    flag = False
    songs[index].hashes["Name"] = os.path.basename(fname)
    if fname.endswith(".mp3"):
        flag = True
        tempPath = fname
        fname = fname.replace(".mp3", ".wav")
        AudioSegment.from_mp3(tempPath).export(fname, format="wav")

    songs[index].samples, songs[index].sampling_rate = librosa.load(
        fname, sr=22050, mono=True, offset=0.0, duration=60
    )
    logging.info(f"The song's path is {fname}")
    if flag:
        os.remove(fname)
    songs[index].hashed_features()


def browseFiles(self, label, index):
    fname = QFileDialog.getOpenFileName(self, "Open file", "../", "*.mp3;;" " *.wav;;")
    file_path = fname[0]
    extensionsToCheck = (".mp3", ".wav")
    if fname[0].endswith(extensionsToCheck):
        label.setText(os.path.basename(fname[0]))
        readSong(fname[0], index)
    elif fname[0] != "":
        errorMssg(
            self, "Invalid format. Please select a file with a wav or mp3 format."
        )
        logging.warning(f"User selected a different format {fname[0]}")
        return


def mixer(self):
    if np.all(songs[0].samples == 0) and np.all(songs[1].samples == 0):
        errorMssg(self, "Please select at least one file")
        logging.critical("No file selected.")
        return 0
    else:
        song1 = (
            songs[0].samples
            if np.all(songs[1].samples == 0)
            else np.multiply(songs[0].samples, self.slider.value() / 100)
        )
        song2 = (
            songs[1].samples
            if np.all(songs[0].samples == 0)
            else np.multiply(songs[1].samples, 1 - self.slider.value() / 100)
        )
        logging.info(f"First song's samples: {song1}")
        logging.info(f"Second song's samples: {song2}")        
        song = Song()
        song.samples = song1 + song2
        song.hashed_features()
        return song


def compareHashes(self):
    song = mixer(self)
    if song == 0:
        return
    similars = []
    with open("data.json", "r+") as file:
        dataInFile = json.load(file)
    for i in range(len(dataInFile["songs"])):
        mfcc_index = (
            1
            - (
                imagehash.hex_to_hash(song.hashes["mfcc"])
                - imagehash.hex_to_hash(dataInFile["songs"][i]["mfcc"])
            )
            / 256.0
        )
        mel_index = (
            1
            - (
                imagehash.hex_to_hash(song.hashes["mel_spectrogram"])
                - imagehash.hex_to_hash(dataInFile["songs"][i]["mel_spectrogram"])
            )
            / 256.0
        )
        spectrogram_index = (
            1
            - (
                imagehash.hex_to_hash(song.hashes["spectrogram"])
                - imagehash.hex_to_hash(dataInFile["songs"][i]["spectrogram"])
            )
            / 256.0
        )
        similars.append(
            [
                (mfcc_index + mel_index + spectrogram_index) / 3,
                os.path.basename(dataInFile["songs"][i]["Name"]),
            ]
        )
    constuctTable(self, similars)


def addTableRow(table, row_data):
    row = table.rowCount()
    table.setRowCount(row + 1)
    col = 0
    for item in row_data:
        if type(item) == float:
            item = round(item, 7)
        cell = QTableWidgetItem(str(item))
        table.setItem(row, col, cell)
        col += 1


def constuctTable(self, similars):
    self.table.setRowCount(0)
    similars.sort(key=lambda x: x[0], reverse=True)
    for item in similars:
        addTableRow(self.table, item)


def errorMssg(self, txt):
    QMessageBox.critical(self, "Error", txt)


def closeSong(self, label, index):
    songs[index] = Song()
    label.setText("SELECTED FILE NAME")


def sliderChange(self, slider, label):
    label.setText(str(slider.value()) + " %")
