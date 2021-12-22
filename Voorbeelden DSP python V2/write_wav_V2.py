# https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave
# working with sound files
import wave, struct, math, random
# what object struct is:
# https://www.journaldev.com/17401/python-struct-pack-unpack
# used for binary files
sampleRate = 44100.0 # hertz
duration = 1.0 # seconds
freq = 4400.0 # hertz
obj = wave.open('sound.wav','wb')
obj.setnchannels(2) # mono 1, for stereo 2
obj.setsampwidth(2)
obj.setframerate(sampleRate)
duration =2 #seconds
N=round(duration*sampleRate) #no of samples
Ts=1/sampleRate #sample time in s
maxint=32767-1
for i in range(N):
    value = round(maxint*math.sin(2*math.pi*freq*i*Ts)) #data should be integer
    #print(value)
    #random.randint(-32767, 32767)
    data = struct.pack('<h', value)
    obj.writeframesraw( data )
obj.close()