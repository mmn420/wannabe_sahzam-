from Song import Song
import os
import librosa
from pydub import AudioSegment
import json
from functions import readSong


def json_data(song):
    if os.path.isfile("data.json"):
        with open("data.json", "r+") as file:
            dataInFile = json.load(file)
            dataInFile["songs"].append(song.hashes)
            file.seek(0)
            json.dump(dataInFile, file, indent=4)
    else:
        data = {}
        data["songs"] = []
        data["songs"].append(song.hashes)
        with open("data.json", "w") as outfile:
            json.dump(data, outfile, indent=4)


def create_db(directory):
    for filename in os.listdir(directory):
        fname = os.path.join(directory, filename)
        json_data(readSong(fname))
