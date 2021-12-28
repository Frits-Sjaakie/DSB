import os.path
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
import math

# compatibility with Python 3
# from future import print_function, division, unicode_literals

# Created input file with:
# mpg123  -w 20130509talk.wav 20130509talk.mp3


def get_audiofiles(folder): #Vraag alle bestanden op en de map naam
    i = 0
    directory = __file__
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    audiofiles_dir = directory + "\\" + folder
    return audiofiles_dir, os.listdir(audiofiles_dir)

def get_audio_data(file):
    audio_read = wave.open(file, 'r')
    audio_data = {} #dictionary voor audio parameters
    parameters = list(audio_read.getparams())  # Get the parameters from the input.
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    audio_data["nchannels"] = parameters[0]
    audio_data["sampwidth"] = parameters[1]
    audio_data["rate"]      = parameters[2]
    audio_data["nframes"]   = parameters[3] = 0 # aantal samples wordt bepaald door "writeframes" functie
    # This file is stereo, 2 bytes/sample, 44.1 kHz.
    #paramters[3] = 0  # The number of samples will be set by writeframes.
    return audio_read, parameters, audio_data

def plot_audio(title, audio_data, plot_data):
    strt = 0
    stp = int(np.trunc(audio_data["nframes"]))
    plt.plot(audio_data["time"][strt:stp], plot_data[strt:stp])
    # plt.xscale('log')
    plt.title(title)
    plt.xlabel('time[s]')
    plt.ylabel('Amplitude')
    plt.show()

def make_new_file(new_file_name, directory, parameters):
    # Open the output file
    i = 0
    #directory = __file__
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    new_file_dir = (directory + "\\" + "Python_made_audiofiles" + "\\" + new_file_name)
    audio_write = wave.open(new_file_dir, "w")
    audio_write.setparams(tuple(parameters))  # Use the same parameters as the input file.
    return(audio_write)

def HighPass(leftFourier, rightFourier, fk):
    leftFourier[:fk], rightFourier[:fk] = 0, 0
    return leftFourier, rightFourier

def LowPass(leftFourier, rightFourier, fk):
    leftFourier[fk:], rightFourier[fk:] = 0, 0
    return leftFourier, rightFourier

def BandSper(leftFourier, rightFourier, fkLow, fkHigh):
    leftFourier[fkLow:fkHigh], rightFourier[fkLow:fkHigh] = 0, 0
    return leftFourier, rightFourier


def proces_audio(audio_read, audio_write):
    sz = audio_read.getframerate()  # Read and process 1 second at a time.
    c = int(audio_read.getnframes() / sz)  # whole file
    for num in range(c):
        print('Processing {}/{} s'.format(num + 1, c))
        da = np.fromstring(audio_read.readframes(sz), dtype=np.int16)
        left, right = da[0::2], da[1::2]  # left and right channel
        leftFourier, rightFourier = np.fft.rfft(left), np.fft.rfft(right)  # FFT zodat filters toegepast kunnen worden
        fk = 2200
        leftFourier, rightFourier = HighPass(leftFourier, rightFourier, fk)
        fk = 15000
        leftFourier, rightFourier = LowPass(leftFourier, rightFourier, fk)
        fkLow = 55
        fkHigh = 66
        leftFourier, rightFourier = BandSper(leftFourier, rightFourier, fkLow, fkHigh)
        nl, nr = np.fft.irfft(leftFourier), np.fft.irfft(rightFourier)  # inverse FFT zodat er weer audio gemaakt van wordt
        ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
        # ns = np.column_stack((left, right)).ravel().astype(np.int16)
        audio_write.writeframes(ns.tostring())

def main():
    directory, audiofiles = get_audiofiles("audiofiles") #Vraag alle bestanden op en de map naam
    x = 1
    for file in audiofiles: #print alle bestanden in de map
        print(f"{x}. {file}")
        x += 1

    print("--------------------------------------------")
    chosen_file = int(input("Kies een audiobestand: ")) - 1 #kies audio bestand aan de hadn van nummer
    title = audiofiles[chosen_file]
    file = directory + "\\" + title

    audio_read, parameters, audio_data = get_audio_data(file)

    '''
    plot_data = []
    if audio_data["nchannels"] == 2:
        plot_data.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 1])
        plot_data.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 0])
    else:
        plot_data.append(audio_data["amplitude"])
    '''

    audio_write = make_new_file(title, directory, parameters)
    proces_audio(audio_read, audio_write)

    audio_read.close()
    audio_write.close()



'''

Highpass = 2200 # Remove lower frequencies.
Lowpass = 15000 # Remove higher frequencies.

sz = wav_read.getframerate() # Read and process 1 second at a time.
c = int(wav_read.getnframes()/sz) # whole file
for num in range(c):
    print('Processing {}/{} s'.format(num+1, c))
    da = np.fromstring(wav_read.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2] # left and right channel
    lf, rf = np.fft.rfft(left), np.fft.rfft(right) # FFT zodat filters toegepast kunnen worden
    lf[:Highpass], rf[:Highpass] = 0, 0 # High Pass >2.2kHz
    lf[55:66], rf[55:66] = 0, 0 # Notch filter 55-66Hz
    lf[Lowpass:], rf[Lowpass:] = 0,0 # Low Pass <15kHz
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf) # inverse FFT zodat er weer audio gemaakt van wordt
    #ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
    ns = np.column_stack((left, right)).ravel().astype(np.int16)
    wav_write.writeframes(ns.tostring())
# Close the files.
wav_read.close()
wav_write.close()
'''

if __name__ == '__main__':
    main()