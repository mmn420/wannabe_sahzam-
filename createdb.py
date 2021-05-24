from Song import Song
import os 
import librosa
import numpy as np
from pydub import AudioSegment
import imagehash
from PIL import Image
import json
from functions import hashed_features, json_data

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
        hashed_features(file)
        json_data(file)
    
