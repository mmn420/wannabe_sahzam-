from Song import Song
import os 
import librosa
import numpy as np
from pydub import AudioSegment
import imagehash
from PIL import Image
import json

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

def create_db(directory):
    file = Song()
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            fname=os.path.join(directory, filename)
            file.samples , file.sampling_rate = librosa.load(fname, sr=22050, mono=True, offset=0.0, duration=60)
            file.hashes['Name'] = os.path.basename(fname)
        elif filename.endswith(".mp3"):
            fname=os.path.join(directory, filename)
            file.hashes['Name'] = os.path.basename(fname)
            new_name = fname.replace('.mp3','.wav')
            AudioSegment.from_mp3(fname).export(new_name, format="wav")
            file.samples,file.samping_rate = librosa.load(new_name, sr=22050, mono=True, offset=0.0, duration=60)
            os.remove(new_name)
        file.hashed_features()
        json_data(file)