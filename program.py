import os.path
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
import math

Highpass = 2200  # Remove lower frequencies.
Lowpass = 15000  # Remove higher frequencies.


def get_audio_data(audio):
    audio_data = {}  # dictionary voor audio parameters
    parameters = list(audio.getparams())  # Get the parameters from the input.
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)

    audio_data["nchannels"] = parameters[0]
    audio_data["sampwidth"] = parameters[1]
    audio_data["framerate"] = parameters[2]
    audio_data["nframes"] = parameters[3]  # aantal samples wordt bepaald door "writeframes" functie
    audio_data["comptype"] = parameters[4]
    audio_data["compname"] = parameters[5]
    # This file is stereo, 2 bytes/sample, 44.1 kHz.
    # paramters[3] = 0  # The number of samples will be set by writeframes.
    return audio_data


def get_audiofiles(folder):
    i = 0
    directory = __file__
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    audiofiles_dir = directory + "\\" + folder
    return audiofiles_dir, os.listdir(audiofiles_dir)


def plot_audio(title, audio_data, plot_data):
    strt = 0
    stp = int(np.trunc(audio_data["nframes"]))
    plt.plot(audio_data["time"][strt:stp], plot_data[strt:stp])
    # plt.xscale('log')
    plt.title(title)
    plt.xlabel('time[s]')
    plt.ylabel('Amplitude ')
    plt.show()


def make_new_file(file_name, directory, audio_data):
    # Open the output file
    i = 0
    # directory = __file__
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    new_file_dir = (directory + "\\" + "Python_made_audiofiles" + "\\" + file_name)
    audio_file = wave.open(new_file_dir, "w")

    audio_file.setnchannels(audio_data["nchannels"])
    audio_file.setsampwidth(audio_data["sampwidth"])
    audio_file.setframerate(audio_data["framerate"])
    audio_file.setnframes(audio_data["nframes"])
    audio_file.setcomptype(audio_data["comptype"], audio_data["compname"])

    return audio_file


def HighPass(leftFourier, rightFourier, fk):
    leftFourier[:fk], rightFourier[:fk] = 0, 0
    return leftFourier, rightFourier


def LowPass(leftFourier, rightFourier, fk):
    leftFourier[fk:], rightFourier[fk:] = 0, 0
    return leftFourier, rightFourier


def BandSper(leftFourier, rightFourier, fkLow, fkHigh):
    leftFourier[fkLow:fkHigh], rightFourier[fkLow:fkHigh] = 0, 0
    return leftFourier, rightFourier


def inv_fourier_transform():
    nl, nr = np.fft.irfft(leftFourier), np.fft.irfft(
        rightFourier)  # inverse FFT zodat er weer audio gemaakt van wordt
    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)


def frourier_transform():
    pass


def save_file():
    pass


def main():
    directory, audiofiles = get_audiofiles("audiofiles")  # Vraag alle bestanden op en de map naam
    x = 1
    for file in audiofiles:  # print alle bestanden in de map
        print(f"{x}. {file}")
        x += 1

    print("--------------------------------------------")
    chosen_file = int(input("Kies een audiobestand: ")) - 1  # kies audio bestand aan de hadn van nummer
    title = audiofiles[chosen_file]
    audio_file = directory + "\\" + title

    input_file = wave.open(audio_file, 'r')

    audio_data = get_audio_data(input_file)

    # plot_data = []
    # if audio_data["nchannels"] == 2:
    #     plot_data.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 1])
    #     plot_data.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 0])
    # else:
    #     plot_data.append(audio_data["amplitude"])

    output_file = make_new_file(title, directory, audio_data)

    duration = int(audio_data["nframes"] / audio_data["framerate"])  # whole file

    for num in range(duration):
        print('Processing {}/{} s'.format(num + 1, duration))
        data = np.fromstring(input_file.readframes(audio_data["framerate"]), dtype=np.int16)
        left, right = data[0::2], data[1::2]  # left and right channel
        leftFourier, rightFourier = np.fft.rfft(left), np.fft.rfft(right)  # FFT zodat filters toegepast kunnen worden
        fk = 2200
        leftFourier, rightFourier = HighPass(leftFourier, rightFourier, fk)
        fk = 15000
        leftFourier, rightFourier = LowPass(leftFourier, rightFourier, fk)
        fkLow = 55
        fkHigh = 66
        leftFourier, rightFourier = BandSper(leftFourier, rightFourier, fkLow, fkHigh)
        nl, nr = np.fft.irfft(leftFourier), np.fft.irfft(
            rightFourier)  # inverse FFT zodat er weer audio gemaakt van wordt
        ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
        # ns = np.column_stack((left, right)).ravel().astype(np.int16)
        output_file.writeframes(ns.tostring())

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    main()
