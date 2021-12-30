import os.path
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math


def select_file(zoekopdracht):
    directory, audiofiles = get_audiofiles(zoekopdracht)  # Vraag alle bestanden op en de map naam
    referentie = False
    x = 1
    for file in audiofiles:  # print alle bestanden in de map
        print(f"{x}. {file}")
        x += 1
    if zoekopdracht == "referenties":
        print("\r\nAls geen referentie gewenst is, typ 0.")
    print("--------------------------------------------")
    chosen_file = int(input("Kies uit " + zoekopdracht + ": ")) - 1  # kies audio bestand aan de hadn van nummer
    if (chosen_file + 1) != 0:
        title = audiofiles[chosen_file]
        audio_file = directory + "\\" + title
        input_file = wave.open(audio_file, 'r')
        audio_data = get_audio_data(input_file)
        referentie = True
    else:
        title = "none selected"
        input_file = "none selected"
        audio_data = "none selected"
    return directory, title, input_file, audio_data, referentie

def get_audio_data(audio):
    audio_data = {}  # dictionary voor audio parameters
    parameters = list(audio.getparams())  # Get the parameters from the input.
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)

    audio_data["nchannels"] = parameters[0]
    audio_data["sampwidth"] = parameters[1]
    audio_data["framerate"] = parameters[2]
    audio_data["nframes"]   = parameters[3]  # aantal samples wordt bepaald door "writeframes" functie
    audio_data["comptype"]  = parameters[4]
    audio_data["compname"]  = parameters[5]
    # This file is stereo, 2 bytes/sample, 44.1 kHz.
    # paramters[3] = 0  # The number of samples will be set by writeframes.

    waveformdata = audio.readframes(audio_data["nframes"])
    fmt = ''
    for i in range(0, audio_data["nframes"]):
        fmt = fmt + 'h'  # fmt should contain 'h'for each samples in wave file: 'hhhhh...'

    if audio_data["nchannels"] == 2:
        fmt = fmt + fmt

    audio_data["time"] = np.arange(0, audio_data["nframes"] / audio_data["framerate"],
                                   1 / audio_data["framerate"])  # start,stop, step fill array
    audio_data["amplitude"] = struct.unpack(fmt, waveformdata)  # from binary to integer
    return audio_data


def get_audiofiles(folder):
    i = 0
    directory = __file__
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    audiofiles_dir = directory + "\\" + folder
    return audiofiles_dir, os.listdir(audiofiles_dir)


def plot_tijd(audio_data, timestamp, plot_title):
    plot_data = []
    if audio_data["nchannels"] == 2:
        plot_data.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 1])
        plot_data.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 0])
    else:
        plot_data.append(audio_data["amplitude"])

    x_start = 0
    x_stop = int(np.trunc(audio_data["nframes"]))

    print(x_start)
    print(x_stop)
    print(audio_data["time"][x_start])
    print(audio_data["time"][x_stop])
    print(plot_data[x_start])
    print(plot_data[x_stop])

    plt.plot(audio_data["time"][x_start:x_stop], plot_data[x_start:x_stop])
    # plt.xscale('log')
    # plt.yscale('log')
    plt.title(plot_title + " - " + timestamp)
    plt.xlabel('time [s]')
    plt.ylabel('Amplitude')
    plt.show()


def plot_freqentie(plot_data, timestamp, plot_title):
    y_as = []
    x_as = []
    x = 1

    for f in plot_data:
        y_as.append(f)  #Verdeel data in variabele netjes over een nieuwe array
        x_as.append(x)  #Tel uit hoeveel frequenties het bestand bevat en stop in array voor lengte van x-as
        x = x + 1

    x_start = 1
    x_stop = 20000
    plt.plot(x_as[x_start:x_stop], y_as[x_start:x_stop])
    #plt.xscale('log')
    plt.yscale('log')
    plt.title(plot_title + " - " + timestamp)
    plt.xlabel('Freqency [Hz]')
    plt.ylabel('Amplitude')
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

    return new_file_dir, audio_file


def HighPass(leftFourier, rightFourier, fk):
    # stel alle frequenties tussen 0Hz en de kantelfrequentie gelijk aan 0
    leftFourier[:fk], rightFourier[:fk] = 0, 0
    return leftFourier, rightFourier


def LowPass(leftFourier, rightFourier, fk):
    # stel alle frequenties tussen 20kHz en de kantelfrequentie gelijk aan 0
    leftFourier[fk:], rightFourier[fk:] = 0, 0# stel alle frequenties tussen 20kHz en de kantelfrequentie gelijk aan 0
    return leftFourier, rightFourier


def BandSper(leftFourier, rightFourier, fkLow, fkHigh):
    # stel alle frequenties tussen de kantelfrequenties gelijk aan 0
    leftFourier[fkLow:fkHigh], rightFourier[fkLow:fkHigh] = 0, 0
    return leftFourier, rightFourier


def inv_fourier_transform(leftFourier, rightFourier):
    # inverse FFT zodat er weer audio gemaakt van wordt
    nl, nr = np.fft.irfft(leftFourier), np.fft.irfft(rightFourier)
    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
    return ns


def main():
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(timestamp)

    # inladen van "vervuilde" audio
    directory, title, input_file, audio_data, referentie = select_file("audiofiles")
    print("\r\n\r\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n\r\n")
    # inladen van "vervuilde" audio
    ref_directory, ref_title, ref_file, ref_audio_data, referentie = select_file("referenties")

    #data voor plot audio in tijd
    plot_tijd(audio_data, timestamp, "Waveform pre-filter")

    directory, output_file = make_new_file(title, directory, audio_data)
    duration = int(audio_data["nframes"] / audio_data["framerate"])  # whole file
    if referentie == True:
        ref_duration = int(ref_audio_data["nframes"] / ref_audio_data["framerate"])

        if ref_duration < duration:
            print("refduration < duration")
            ref_frame = int(ref_duration / 2)
        elif ref_duration > duration:
            print("refduration > duration")
            ref_frame = int((ref_duration / duration) * 2)
        elif ref_duration == duration:
            ref_frame = int(ref_duration / 2)

        print("duration: ", duration)
        print("ref_duration: ", ref_duration)
        print("ref_frame: ", ref_frame)

    for num in range(duration):
        print(f'Processing {num + 1}/{duration} s')
        data = np.fromstring(input_file.readframes(audio_data["framerate"]), dtype=np.int16)
        l_data, r_data = data[0::2], data[1::2]  # left and right channel

        # FFT zodat filters toegepast kunnen worden. Zodra in het frequentiedomein dan kunnen de filters worden
        # toegepast per frequentie. Per seconde wordt er gekeken welke frequenties zich in de samples bevinden.
        leftFourier, rightFourier = np.fft.rfft(l_data), np.fft.rfft(r_data)

        # Filters
        leftFourier, rightFourier = HighPass(leftFourier, rightFourier, 2200)
        leftFourier, rightFourier = LowPass(leftFourier, rightFourier, 15000)
        #leftFourier, rightFourier = BandSper(leftFourier, rightFourier, 55, 66)

        if num == int(duration / 2):
            print("sample")
            frequency_prefilter_data = np.fft.rfft(l_data)
            frequency_postfilter_data = leftFourier

        # inverse FFT zodat er weer audio gemaakt van wordt. Conversie van frequentiedomein naar tijdsdomein.
        new_l_data, new_right_data = np.fft.irfft(leftFourier), np.fft.irfft(rightFourier)
        new_wav_data = np.column_stack((new_l_data, new_right_data)).ravel().astype(np.int16)

        output_file.writeframes(new_wav_data.tostring())

        # referentiegeluid plot sample verkrijgen
        if referentie == True:
            ref_data = np.fromstring(ref_file.readframes(ref_audio_data["framerate"]), dtype=np.int16)
            if num == ref_frame:
                print("refsample")
                frequency_ref_data = np.fft.rfft(ref_data)

    plot_freqentie(frequency_prefilter_data, timestamp, "FFT pre-filter data left channel")
    plot_freqentie(frequency_postfilter_data, timestamp, "FFT post-filter data left channel")
    if referentie == True:
        plot_freqentie(frequency_ref_data, timestamp, "FFT referentie vogel")
        ref_file.close()


    input_file.close()
    output_file.close()

    print(f"New file made at: {directory}")

if __name__ == '__main__':
    main()


