# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 17:04:34 2019

@author: Admin
"""
import numpy as np
import matplotlib.pyplot as plt
from read_wav_stereo_V5 import readwav

def win_Ham(n,Ns):      #Hamming windowing function (LI Tan, Digital Signal Processing, ch 7.3 p.230)
    w=0.54-0.46*np.cos(2*np.pi*n/Ns)
    return(w)

def window(x):      #general IIR filter
    Nsamples=len(x)
    y=[0]*Nsamples
    for i in range(Nsamples):
        y[i]=win_Ham(i,Nsamples)*x[i]

    return(y)


x=readwav('sound.wav')
nchannels=x[0]
samplerate=x[1]
samplewidth=x[2]
Nfrms=x[3]
time=x[4]
Data=x[5]   #if channels =2 do not use this
print('ch,Fs,sw,length:',x[0:4])
Ts=1/samplerate

t = np.arange(Nfrms)*Ts
#generate test signal
#x=np.sin(2*np.pi*f0*t)+1/3*np.sin(2*np.pi*3*f0*t)

#take DFT and scale results
sp = 2/Nfrms*np.fft.fft(Data)
#freq = np.fft.fftfreq(signal.size(steps), d=timestep)
freq = np.fft.fftfreq(Nfrms,Ts)

#take subset of Data
strt=10000
step=1000   #number of intervals
stp=strt+step
intervals=stp-strt
subDat = Data[strt:stp]

#apply windowing before FFT
subDat=window(subDat)

#    sp = abs(2/intervals*np.fft.fft(subDat))    #z, y=i, linear scale
sp = abs(2/intervals*np.fft.fft(subDat))    #z, y=i, for log scale
k=int(np.trunc(len(sp)/2))  #only first half <Fs/2 contains valid data
sp=sp[0:k]
freq = np.fft.fftfreq(intervals,Ts) #x
freq=freq[0:k]
t = np.arange(step)*Ts
Data = subDat




#plot Data

plt.plot(t,Data)
plt.title('signal(t)')
plt.xlabel('time [s]')
plt.ylabel('Amplitude u(t) ')
plt.show()

#plot spectrum
#plt.plot(freq, sp.real, freq, sp.imag)
plt.plot(freq, abs(sp),'^r')
plt.yscale('log')
plt.title('FFT')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude F ')
plt.show()