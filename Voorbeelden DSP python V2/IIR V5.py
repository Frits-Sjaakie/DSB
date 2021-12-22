"""
Created on Wed Oct  9 16:04:29 2019

@author: Admin
"""
import numpy as np

import matplotlib.pyplot as plt

def IIR_filter(x,a,b):      #general IIR filter
    Nsamples=len(x)
    y=[0]*Nsamples
    Na=len(a)
    Nb=len(b)
    for i in range(Nb,Nsamples):
        sumbx=0
        for j in range(0,Nb):
            if i-j>=0:
                sumbx+=b[j]*x[i-j]
        sumay=0
        for k in range(1,Na):
            if i-k>=0:
                sumay+=a[k]*y[i-k]
        y[i]=(sumbx-sumay)/a[0]
    return(y)        

#main
frq=1
Fs=100
Ts=1/Fs
periods=5
intervals=round(periods/frq/Ts)
print(intervals)
t = np.linspace(0, periods/frq,intervals )  #generate times
x = np.sin(2*np.pi*frq*t)                   #generate signal
#x = x + np.random.randn(len(t)) * 0.08     #add noise

#set reverse and forward coefficients for a and b
#                    -1              -M
#        b[0] + b[1]z  + ... + b[M] z
#Y(z) = -------------------------------- X(z)
#                    -1              -N
#        a[0] + a[1]z  + ... + a[N] z

#simple low pass Euler
w_co=2*np.pi*1

a=np.array([1+w_co*Ts,-1])      #a0, a1..an;filling it by hand, 1.0 is not allowed
b=np.array([w_co*Ts])           #b0,b1,...bm

y = IIR_filter(x,a,b)
plt.figure
plt.plot(t, x,'r',t,y,'b')
#plt.plot(t, x, 'b--', t, xn, 'r', t, y, 'r^')
plt.legend(['signal','fitlered'])
plt.grid(True)
plt.show()
print('coefficients numerator B: ',b)
print('coefficients denominator A: ',a)

