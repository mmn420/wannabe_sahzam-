from Song import Song
import os
import librosa
from pydub import AudioSegment
import json


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
    file = Song()
    for filename in os.listdir(directory):
        flag = False
        fname = os.path.join(directory, filename)
        file.hashes["Name"] = os.path.basename(fname)
        if filename.endswith(".mp3"):
            flag = True
            tempPath = fname
            fname = fname.replace(".mp3", ".wav")
            AudioSegment.from_mp3(tempPath).export(fname, format="wav")

        file.samples, file.samping_rate = librosa.load(
            fname, sr=22050, mono=True, offset=0.0, duration=60
        )
        if flag:
            os.remove(fname)
        file.hashed_features()
        json_data(file)
