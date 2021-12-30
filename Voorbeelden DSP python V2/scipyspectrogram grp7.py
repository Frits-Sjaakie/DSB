# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 18:50:08 2021

@author: RNDAdmin
"""

from scipy.io import wavfile # scipy library to read wav files
import numpy as np

import matplotlib.pyplot as plt
AudioName = "sound.wav" # Audio File
#AudioName = “sample.wav" # Audio File

fs,Audiodata = wavfile.read(AudioName)


# Plot the audio signal in time
plt.plot(Audiodata)
plt.title('Audio signal in time',size=16)

# spectrum
from scipy.fftpack import fft # fourier transform
n= len(Audiodata)
AudioFreq = fft(Audiodata)
AudioFreq = AudioFreq[0:int(np.ceil((n + 1) / 2.0))] #Half of the spectrum
MagFreq = np.abs(AudioFreq) # Magnitude
MagFreq = MagFreq / float(n)
# power spectrum
MagFreq = MagFreq**2
if n % 2 > 0: # ffte odd
    MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
else:# fft even
    MagFreq[1:len(MagFreq) - 1] = MagFreq[1:len(MagFreq) -1] * 2

plt.figure()

freqAxis = np.arange(0,int(np.ceil((n+1)/2.0)), 1.0) * (fs / n);
plt.title(AudioName)

plt.plot(freqAxis/1000.0, 10*np.log10(MagFreq)) #Power spectrum
plt.xlabel( 'Frequency (kHz)'); plt.ylabel('Power spectrum (dB)');

#Spectrogram

from scipy import signal

N = 512 #Number of point in the fft

f, t, Sxx = signal.spectrogram(Audiodata, fs,window = signal. blackman(N) ,nfft=N)
plt.figure()

plt.pcolormesh(t, f,10*np.log10(Sxx)) # dB spectrogram

#plt.peolormesh(t, f,5xx) # Lineal spectrogram

plt.ylabel( 'Frequency [Hz]')

plt.xlabel('Time [seg]')

plt.title('Spectrogram of a filtered common swift',size=16);

plt.show()

