#https://www.programcreek.com/python/example/93227/scipy.io.wavfile.read
import wave,struct
import matplotlib.pyplot as plt
import numpy as np


def readwav(file):
    # wavio.py
    # Author: Warren Weckesser
    # License: BSD 3-Clause (http://opensource.org/licenses/BSD-3-Clause)
    """
    Read a wav file.

    Returns the frame rate, sample width (in bytes) and a numpy array
    containing the data.

    This function does not read compressed wav files.
    """
    wav = wave.open(file)
    rate = wav.getframerate()
    nchannels = wav.getnchannels()
    sampwidth = wav.getsampwidth()
    nframes = wav.getnframes()  #amount of data available
    data = wav.readframes(nframes)  #read binary data from file
    wav.close()

    fmt=''
    for i in range (0,nframes):
        fmt=fmt+'h'#fmt should contain 'h'for each samples in wave file: 'hhhhh...' 
    t=np.arange(0,nframes/rate,1/rate)  #start,stop, step fill array    
    D=struct.unpack(fmt, data)  #from binary to integer
    return nchannels, rate, sampwidth,nframes,t, D 

x=readwav('sound.wav')
nchannels=x[0]
samplerate=x[1]
samplewidth=x[2]
Nfrms=x[3]
time=x[4]
Data=x[5]
print('ch,Fs,sw,length:',x[0:4])
#As a quick explanation of the format string, the < indicates little-endian data (defined in the spec) and the h 1 signed 16-bit int. 
#in the bracktes indicate range
strt=0
stp=100
plt.plot(time[strt:stp],Data[strt:stp])
#plt.xscale('log')
plt.title('audio')
plt.xlabel('time[s]')
plt.ylabel('Amplitude ')
plt.show()

