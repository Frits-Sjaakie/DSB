import os.path
import wave
import numpy as np
# compatibility with Python 3
# from future import print_function, division, unicode_literals

# Created input file with:
# mpg123  -w 20130509talk.wav 20130509talk.mp3

def get_audiofiles(folder):
    i = 0
    directory = __file__
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    audiofiles_dir = directory + "\\" + folder
    return audiofiles_dir, os.listdir(audiofiles_dir)

directory, audiofiles = get_audiofiles("audiofiles")
x = 1
for file in audiofiles:
    print(f"{x}. {file}")
    x += 1

print("--------------------------------------------")
chosen_file = int(input("Kies een audiobestand: ")) - 1
file = directory + "\\" + audiofiles[chosen_file]

wr = wave.open(file, 'r')
par = list(wr.getparams()) # Get the parameters from the input.
# This file is stereo, 2 bytes/sample, 44.1 kHz.
par[3] = 0 # The number of samples will be set by writeframes.

# Open the output file
ww = wave.open('filteredtest.wav', 'w')
ww.setparams(tuple(par)) # Use the same parameters as the input file.

Highpass = 2200 # Remove lower frequencies.
Lowpass = 15000 # Remove higher frequencies.

sz = wr.getframerate() # Read and process 1 second at a time.
c = int(wr.getnframes()/sz) # whole file
for num in range(c):
    print('Processing {}/{} s'.format(num+1, c))
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2] # left and right channel
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
    lf[:Highpass], rf[:Highpass] = 0, 0 # High Pass >2.2kHz
    lf[55:66], rf[55:66] = 0, 0 # Notch filter 55-66Hz
    lf[Lowpass:], rf[Lowpass:] = 0,0 # Low Pass <15kHz
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
    #ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
    ns = np.column_stack((left, right)).ravel().astype(np.int16)
    ww.writeframes(ns.tostring())
# Close the files.
wr.close()
ww.close()