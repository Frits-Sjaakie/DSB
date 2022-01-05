import os.path
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math

def select_file(zoekopdracht):
    # Geef keuze opties voor bestanden en return gekozen bestand
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
        audio_data, waveformdata = get_audio_data(input_file)
        referentie = True
    else:
        title = "none selected"
        input_file = "none selected"
        audio_data = "none selected"
        referentie = False
        waveformdata = ''
    return directory, title, input_file, audio_data, waveformdata, referentie

def amplitude_data(waveformdata, audio_data):
    fmt = ''
    for i in range(0, audio_data["nframes"]):
        fmt = fmt + 'h'  # fmt should contain 'h'for each samples in wave file: 'hhhhh...'

    if audio_data["nchannels"] == 2:
        fmt = fmt * 2
    audio_data["time"] = np.arange(0, audio_data["nframes"] / audio_data["framerate"],
                                   1 / audio_data["framerate"])  # start,stop, step fill array
    audio_data["amplitude"] = struct.unpack(fmt, waveformdata)  # from binary to integer
    return(audio_data)


def get_audio_data(audio):
    # Audiodata in gekozen bestand lezen
    audio_data = {}  # dictionary voor audio parameters
    parameters = list(audio.getparams())  # defineer variabelen uit audiofile
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    # converteer naar dictionary voor makkelijker opvragen van data in het programma
    audio_data["nchannels"] = parameters[0]
    audio_data["sampwidth"] = parameters[1]
    audio_data["framerate"] = parameters[2]
    audio_data["nframes"] = parameters[3]  # aantal samples wordt bepaald door "writeframes" functie
    audio_data["comptype"] = parameters[4]
    audio_data["compname"] = parameters[5]

    # Amplitude data maken voor amplitude vs tijd plot
    waveformdata = audio.readframes(audio_data["nframes"])
    audio_data = amplitude_data(waveformdata, audio_data)
    return audio_data, waveformdata


def get_audiofiles(folder):
    # Return alle bestandsnamen in doel map
    i = 0
    directory = __file__
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    audiofiles_dir = directory + "\\" + folder
    return audiofiles_dir, os.listdir(audiofiles_dir)


def plot_tijd(audio_data, timestamp, plot_title):
    # Plot de amplitude vs de tijd in een grafiek
    left_amplitude = []
    right_amplitude = []
    if audio_data["nchannels"] == 2:
        left_amplitude.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 1])
        right_amplitude.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 0])
    else:
        left_amplitude.append(audio_data["amplitude"])

    index = 0
    time_plotdata = []
    left_plotdata = []
    right_plotdata = []
    for value in audio_data["time"]:
        time_plotdata.append(value)
        left_plotdata.append(left_amplitude[0][index])
        if(audio_data["nchannels"] == 2):
            right_plotdata.append(right_amplitude[0][index])
        index = index + 1
        if index >= len(audio_data["time"]):
            break

    x_start = 0
    x_stop = len(time_plotdata)

    n = 1
    while n <= audio_data["nchannels"]:
        # plt.xscale('log')
        # plt.yscale('log')
        if n == 1:
            plt.plot(time_plotdata[x_start:x_stop], left_plotdata[x_start:x_stop])
            plt.title(plot_title + " left channel - " + timestamp)
        elif n == 2:
            plt.plot(time_plotdata[x_start:x_stop], right_plotdata[x_start:x_stop])
            plt.title(plot_title + " right channel - " + timestamp)
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()
        n = n + 1


def plot_freqentie(plot_data, timestamp, plot_title):
    # Plot de amplitude vs de frequentie in een grafiek
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
    # Maak een nieuw bestand aan om gefilterde audiodata in op te slaan
    i = 0
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    new_file_dir = (directory + "\\" + "Python_made_audiofiles" + "\\" + file_name)
    audio_file = wave.open(new_file_dir, "w")

    # Stel parameters van nieuwe bestand in aan de hand van de parameters van het ingelezen bestand
    audio_file.setnchannels(audio_data["nchannels"])
    audio_file.setsampwidth(audio_data["sampwidth"])
    audio_file.setframerate(audio_data["framerate"])
    audio_file.setnframes(audio_data["nframes"])
    audio_file.setcomptype(audio_data["comptype"], audio_data["compname"])

    return new_file_dir, audio_file


def HighPass(Fourier, fk):
    # Stel alle frequenties tussen 0Hz en de kantelfrequentie gelijk aan 0
    Fourier[:fk] = 0
    return Fourier


def LowPass(Fourier, fk):
    # Stel alle frequenties tussen 20kHz en de kantelfrequentie gelijk aan 0
    Fourier[fk:] = 0
    return Fourier


def BandSper(Fourier, fkLow, fkHigh):
    # Stel alle frequenties tussen de kantelfrequenties gelijk aan 0
    Fourier[fkLow:fkHigh] = 0
    return Fourier


def main():
    # Maak een timestamp voor de grafieken. Maakt het onderscheiden van programma loops makkelijker
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    # Data vergaring uit bestanden


    # Inladen van "vervuilde" audio
    directory, title, input_file, audio_data, waveformdata, referentie = select_file("audiofiles")

    # Aanmaken van nieuw bestand voor output data
    output_file, output_file_title = make_new_file(title, directory, audio_data)

    # Inladen van referentie file
    print("\r\n\r\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n\r\n")
    ref_directory, ref_title, ref_file, ref_audio_data, ref_waveformdata, referentie = select_file("referenties")

    # Plot amplitude vs tijd na filtering
    plot_tijd(audio_data, timestamp, "Waveform pre-filter")
    if referentie == True:
        # Als gekozen is voor een referentie, maak ook een amplitude vs tijd plot hiervan
        plot_tijd(ref_audio_data, timestamp, "Waveform referentie geluid")


    # Verwerking van vervuilde audio


    new_waveformdata = []

    # Bepaal sample met maximale amplitude
    max_value = max(audio_data["amplitude"])
    max_value_index = audio_data["amplitude"].index(max_value)

    # Bepaal in welke seconde deze sample zit
    if audio_data["nchannels"] == 2:
        max_value_frame = int(max_value_index / (audio_data["framerate"] * 4))
    else:
        max_value_frame = int(max_value_index / (audio_data["framerate"] * 2))
    print("max_value_frame: ", max_value_frame + 1)

    # Toepassen van filters op seconde basis
    duration = int(audio_data["nframes"] / audio_data["framerate"])
    for num in range(duration):
        print(f'Processing {num + 1}/{duration} s')

        # Bereken intervallen zodat per seconde een FFT wordt gemaakt
        if audio_data["nchannels"] == 2:
            start_frame = num * (audio_data["framerate"] * 4)
            stop_frame = (num * (audio_data["framerate"] * 4)) + (audio_data["framerate"] * 4)
        else:
            start_frame = num * (audio_data["framerate"] * 2)
            stop_frame = (num * (audio_data["framerate"] * 2)) + (audio_data["framerate"] * 2)

        # Lees data in uit "waveformdata"
        data = np.fromstring(waveformdata[start_frame:stop_frame], dtype=np.int16)

        # Inlezen van data gescheiden in links en rechts. Bij geen stereo, gebruik alleen linker kanaal
        if audio_data["nchannels"] == 2:
            l_data, r_data = data[0::2], data[1::2]  # left and right channel
        else:
            l_data = data

        # FFT linker kanaal
        leftFourier = np.fft.rfft(l_data)

        # Kantelfrequenties voor filters. Gelden voor links en ook voor rechts indien aanwezig.
        # single bird
        fk_hp1 = 5000
        fk_lp1 = 7500
        #multiple bird
        #fk_hp1 = 2200
        #fk_lp1 = 15000

        # Filters linker kanaal
        leftFourier = HighPass(leftFourier, fk_hp1)
        leftFourier = LowPass(leftFourier, fk_lp1)
        #leftFourier = BandSper(leftFourier, fk_bp1l, fk_bp1h)

        #data voor FFT plot linker kanaal
        if num == max_value_frame:
            print("SAMPLE LEFT!")
            left_frequency_prefilter_data = np.fft.rfft(l_data)
            left_frequency_postfilter_data = leftFourier

        # Inverse FFT left channel
        new_l_data = np.fft.irfft(leftFourier)

        if audio_data["nchannels"] == 2:
            # FFT rechter kanaal
            rightFourier = np.fft.rfft(r_data)

            # Filters rechter kanaal
            rightFourier = HighPass(rightFourier, fk_hp1)
            rightFourier = LowPass(rightFourier, fk_lp1)
            #rightFourier = BandSper(rightFourier, fk_bp1l, fk_bp1h)


            # Data voor FFT post-filter plot rechter kanaal
            if num == max_value_frame:
                print("SAMPLE RIGHT!")
                right_frequency_prefilter_data = np.fft.rfft(r_data)
                right_frequency_postfilter_data = rightFourier

            # Inverse FFT rechter kanaal
            new_r_data = np.fft.irfft(rightFourier)

        # Voeg data samen in 1 variabel voor opslaan in geval van stereo
        if audio_data["nchannels"] == 2:
            new_wav_data = np.column_stack((new_l_data, new_r_data)).ravel().astype(np.int16)
        else:
            new_wav_data = np.column_stack(new_l_data).ravel().astype(np.int16)

        # Converteer output van FFT naar een list van integers
        new_wav_data_list = new_wav_data.tolist()
        for n in new_wav_data_list:
            new_waveformdata.append(n)

        # Sla data op in nieuw bestand
        output_file_title.writeframes(new_wav_data.tostring())

    # FFT plot van pre-filter en post-filter data
    plot_freqentie(left_frequency_prefilter_data, timestamp, "FFT pre-filter data left channel")
    plot_freqentie(left_frequency_postfilter_data, timestamp, "FFT post-filter data left channel")
    if audio_data["nchannels"] == 2:
        plot_freqentie(right_frequency_prefilter_data, timestamp, "FFT pre-filter data right channel")
        plot_freqentie(right_frequency_postfilter_data, timestamp, "FFT post-filter data right channel")

    # Sluit bestanden
    input_file.close()
    output_file_title.close()

    # Plot amplitude vs tijd na filtering
    filtered_audio_data, filtered_waveformdata = get_audio_data(wave.open(output_file, 'r'))
    filtered_audio_data = amplitude_data(filtered_waveformdata, filtered_audio_data)
    plot_tijd(filtered_audio_data, timestamp, "Waveform post-filter")


    # Verwerking van referentiedata als er een referentiebestand is gekozen. Anders sla over en sluit programma


    if referentie == True:
        ref_duration = int(ref_audio_data["nframes"] / ref_audio_data["framerate"])

        # Bepaal sample met maximale amplitude
        max_value = max(ref_audio_data["amplitude"])
        max_value_index = ref_audio_data["amplitude"].index(max_value)

        # Bepaal in welke seconde deze sample zit
        if ref_audio_data["nchannels"] == 2:
            max_value_ref_frame = int(max_value_index / (ref_audio_data["framerate"] * 4))
        else:
            max_value_ref_frame = int(max_value_index / (ref_audio_data["framerate"] * 2))
        print("max_value_ref_frame: ", max_value_ref_frame + 1)

        # Referentiegeluid plot sample verkrijgen
        for ref_num in range(ref_duration):
            print(f'Processing {ref_num + 1}/{ref_duration} s')
            # Bereken intervallen zodat per seconde een FFT wordt gemaakt
            if ref_audio_data["nchannels"] == 2:
                ref_start_frame = ref_num * (ref_audio_data["framerate"] * 4)
                ref_stop_frame = (ref_num * (ref_audio_data["framerate"] * 4)) + (ref_audio_data["framerate"] * 4)
            else:
                ref_start_frame = ref_num * (ref_audio_data["framerate"] * 2)
                ref_stop_frame = (ref_num * (ref_audio_data["framerate"] * 2)) + (ref_audio_data["framerate"] * 2)

            # Als referentie frame is bereikt, lees data uit "ref_waveformdata"
            if ref_num == max_value_ref_frame:
                print("SAMPLE!")
                # Inlezen van data gescheiden in links en rechts. Bij geen stereo, gebruik alleen linker kanaal
                ref_data = np.fromstring(ref_waveformdata[ref_start_frame:ref_stop_frame], dtype=np.int16)
                if audio_data["nchannels"] == 2:
                    # Als audiobestand is stereo, verdeel data in links en rechts. Anders gebruik alleen links
                    ref_l_data, ref_r_data = ref_data[0::2], ref_data[1::2]
                else:
                    ref_l_data = ref_data

        # Altijd FFT en plot links
        ref_left_frequency_data = np.fft.rfft(ref_l_data)
        plot_freqentie(ref_left_frequency_data,timestamp, "FFT referentie vogel left channel")

        # Als stereo, dan ook rechts
        if ref_audio_data["nchannels"] == 2:
            ref_right_frequency_data = np.fft.rfft(ref_r_data)
            plot_freqentie(ref_right_frequency_data,  timestamp, "FFT referentie vogel right channel")

        # Sluit referentie bestand
        ref_file.close()

    # Print directory van nieuwe file
    print(f"\r\n\r\nGefilterde audiobestand staat in de map: {output_file}")

if __name__ == '__main__':
    main()