import imagehash
import librosa
from PIL import Image

class Song:
    def __init__(self):
        self.name = ""
        self.samples = 0
        self.sampling_rate = 0
        self.hashes = {}
    
    def hashed_features(self):
        self.hashes["mfcc"] = str(imagehash.phash(Image.fromarray(librosa.feature.mfcc(self.samples)), hash_size=16))
        self.hashes["mel_spectrogram"] = str(imagehash.phash(Image.fromarray(librosa.feature.melspectrogram(self.samples)), hash_size=16))