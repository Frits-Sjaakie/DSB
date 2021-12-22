# https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave
# working with sound files
import wave, struct, math
# what object struct is:
# https://www.journaldev.com/17401/python-struct-pack-unpack
# used for binary files
sampleRate = 44100.0 # hertz
duration = 1 # seconds
freq1 = 100.0 # hertz
freq2 = 500
obj = wave.open('sound.wav','wb')
chnls=2
obj.setnchannels(chnls) # mono 1, for stereo 2
obj.setsampwidth(2)
obj.setframerate(sampleRate)
maxint=32767-1
N=chnls*round(duration*sampleRate) #no of samples
Ts=1/(sampleRate*chnls) #sample time in s- should be halved for stereo
if (N % 2) != 0:
    N+=1

for i in range(N):
    value1 = round(maxint*i/N*math.sin(2*math.pi*freq1*i*Ts) ) #data should be integer
    value2 = round(maxint*(N-i)/N*math.sin(2*math.pi*freq2*i*Ts)) #data should be integer
    #value1 = round(1*maxint*math.sin(2*math.pi*freq1*i*Ts) ) #data should be integer
    #value2 = round(1*maxint*math.sin(2*math.pi*freq2*i*Ts)) #data should be integer
# samples are alternately written to Left or Right
# this produces low tone right and high left
# maxint*i/N sets increasing volume    
    if (i % 2) == 0:
        value=value2
    else:
        value=value1
    #print(value)
    #random.randint(-32767, 32767)
    data = struct.pack('<h', value)
    obj.writeframesraw( data )
obj.close()

