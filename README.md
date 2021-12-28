# Shazam Replica
# Introduction 
Fingerprinting is basically to identify a signal based on a short sample for it which usually has its intrinsic features and thus these intrinsic features can be used to identify the different varieties or flavors of the signal. Several applications can be directly spotted for such technique. For example:

# Description:
Generate the spectrogram for selected songs (3 spectrograms for: the song, the music and the vocals).
Note: the spectrogram will always be generated for the first 1 min of the song regardless of its length. This will reduce the computation a little and will also guarantee that all calculations will be done on the same period in all the songs.
 
For each spectrogram:
Extract the main features in each spectrogram (Do you search for which features to look for and how to extract them). Collect them in some file along with your spectrogram.
Use hash functions to hash the collected features into a shorter sequence. Please, make sure to use perceptual hash not regular hash. Do your search for the different hash types mentioned here.
Both outputs from the previous two items are the fingerprint for each song.
 
Now, given any sound file (either song, or vocals, or music), the program should be able to generate its spectrogram features and be able to list the closest songs to it from the shared folder. The program should be able to generate some similarity index to each song then sort them and output the sorting list along with each similarity check in a nice table in the GUI.
 
The program should be able to take two files, make a weighted average of them (there should be a slider to control the weighting percentage). Then, the software should treat the new summation as a new file and search for the closest songs to it. The selected songs have higher similarity index.
