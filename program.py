import os.path
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
import math


def get_audio(filename):
    audio_data = {}
    with wave.open(filename, mode=None) as audio:
        audio_data["rate"] = audio.getframerate()
        audio_data["nchannels"] = audio.getnchannels()
        audio_data["sampwidth"] = audio.getsampwidth()
        audio_data["nframes"] = audio.getnframes()
        data = audio.readframes(audio_data["nframes"])

        fmt = ''
        for i in range(0, audio_data["nframes"]):
            fmt = fmt + 'h'  # fmt should contain 'h'for each samples in wave file: 'hhhhh...'

        if audio_data["nchannels"] == 2:
            fmt = fmt + fmt

        audio_data["time"] = np.arange(0, audio_data["nframes"] / audio_data["rate"],
                                       1 / audio_data["rate"])  # start,stop, step fill array
        audio_data["amplitude"] = struct.unpack(fmt, data)  # from binary to integer

    audio.close()
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


def save_wav_file(file_name, audio_data):
    # Open up a wav file
    i = 0
    directory = __file__
    while i < 1:
        directory = os.path.abspath(os.path.join(directory, os.pardir))
        i += 1
    wav_dir = directory + "\\" + "Python_made_audiofiles" + "\\" + file_name
    wav_file = wave.open(wav_dir, "w")

    freq1 = 100.0  # hertz
    freq2 = 500

    wav_file.setnchannels(audio_data['nchannels'])  # mono 1, for stereo 2
    wav_file.setsampwidth(2)
    wav_file.setframerate(audio_data['rate'])
    maxint = 32767 - 1
    N = audio_data["nframes"]  # no of samples

    Ts = 1 / (audio_data['rate'] * audio_data['nchannels'])  # sample time in s- should be halved for stereo

    if (N % 2) != 0:
        N += 1

    for i in range(N):
        value1 = round(maxint * i / N * math.sin(2 * math.pi * freq1 * i * Ts))  # data should be integer
        value2 = round(maxint * (N - i) / N * math.sin(2 * math.pi * freq2 * i * Ts))  # data should be integer
        # value1 = round(1*maxint*math.sin(2*math.pi*freq1*i*Ts) ) #data should be integer
        # value2 = round(1*maxint*math.sin(2*math.pi*freq2*i*Ts)) #data should be integer
        # samples are alternately written to Left or Right
        # this produces low tone right and high left
        # maxint*i/N sets increasing volume
        if (i % 2) == 0:
            value = value2
        else:
            value = value1
        # print(value)
        # random.randint(-32767, 32767)
        data = struct.pack('<h', value)
        wav_file.writeframes(data)
    wav_file.close()

    return


def main():
    directory, audiofiles = get_audiofiles("audiofiles")
    x = 1
    for file in audiofiles:
        print(f"{x}. {file}")
        x += 1

    print("--------------------------------------------")
    chosen_file = int(input("Kies een audiobestand: ")) - 1

    file = directory + "\\" + audiofiles[chosen_file]
    audio_data = get_audio(file)

    plot_data = []
    if audio_data["nchannels"] == 2:
        plot_data.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 1])
        plot_data.append([audio_data["amplitude"][i] for i in range(len(audio_data["amplitude"])) if i % 2 == 0])
    else:
        plot_data.append(audio_data["amplitude"])

    title = audiofiles[chosen_file]
    x = 1
    for i in plot_data:
        plot_audio(title + " " + str(x), audio_data, i)
        x += 1

    # Save new file with changes
    save_wav_file(title, audio_data)


if __name__ == '__main__':
    main()
