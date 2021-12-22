# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 17:04:34 2019

@author: Admin
"""
import numpy as np
import matplotlib.pyplot as plt

#example 1
print('example 1:')
x = np.arange(5)
print(x)
print(np.fft.fft(x))


#example 2
print('example 2:')
f0=10
T=1/f0
N=2**4  #for fastest FFT, N is power of 2
Ts=T/N

t = np.arange(N)*Ts
#generate test signal
x=np.sin(2*np.pi*f0*t)+1/3*np.sin(2*np.pi*3*f0*t)

#take DFT and scale results
sp = 2/N*np.fft.fft(x)
freq = np.fft.fftfreq(N,Ts)
#freq = np.fft.fftfreq(signal.size(steps), d=timestep)
#plt.subplot(2,1,1)

plt.plot(t,x)
plt.title('signal(t)')
plt.xlabel('time [s]')
plt.ylabel('Amplitude u(t) ')
plt.show()
#plt.subplot(2,1,2)
#plt.plot(freq, sp.real, freq, sp.imag)
plt.plot(freq, abs(sp),'^r')
#plt.xscale('log')
plt.title('FFT')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude F ')
plt.show()