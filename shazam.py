import librosa
import librosa.display
from os import path
from librosa.core.harmonic import salience
from librosa.feature.spectral import mfcc, spectral_centroid, spectral_rolloff
import numpy as np
import matplotlib.pyplot as plt
from numpy import lib
from scipy import signal as sig
from pydub import AudioSegment
import imagehash
from PIL import Image

windowType="hann"
windowSize = 1024
hop_length = 512

def get_features(samples, windowType, sampling_rate, hop_length, windowSize):
    zero_crossings = librosa.feature.zero_crossing_rate(samples, hop_length=hop_length)
    spectral_centroid = librosa.feature.spectral_centroid(samples, window=windowType, n_fft=windowSize)
    spectral_rolloff = librosa.feature.spectral_rolloff(samples, window=windowType, n_fft=windowSize)
    mfcc = librosa.feature.mfcc(samples, sr=sampling_rate)


# AudioSegment.ffmpeg = path.abspath("C:\ffmpeg-4.4-full_build\bin")
# AudioSegment.from_mp3("test.mp3").export("test.wav", format="wav")
samples, sampling_rate = librosa.load("test.wav", sr=22050, mono=True, offset=0.0, duration=60)
#display waveform

plt.figure(figsize=(14, 5))
librosa.display.waveplot(samples, sr=sampling_rate)
# print(librosa.feature.spectral_centroid(samples))
# print(librosa.feature.spectral(samples))
# print(Image.fromarray(librosa.feature.spectral_centroid(samples), mode='RGB'))
#display Spectrogram
X = librosa.stft(samples, n_fft=windowSize, hop_length=hop_length, window=windowType)
Xdb = librosa.amplitude_to_db(abs(X))
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sampling_rate, x_axis='time', y_axis='hz') 
print(str(imagehash.phash(Image.fromarray(librosa.feature.spectral_centroid(samples)))))
print(Image.fromarray(((np.reshape(librosa.feature.spectral_centroid(samples),(-1, 2))))))
plt.colorbar()
plt.show()