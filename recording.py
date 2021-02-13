'''
RECORDING METHOD
'''

import pyaudio
import os
import wave
import sys
import time
import RPi.GPIO as GPIO

BUTTON_GPIO = 16 #GPIO to stop the recording

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^9 samples for buffer
record_secs = 30 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'audio.wav' # name of .wav file
MACADD = sys.argv[1]

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pressed = False

audio = pyaudio.PyAudio() # create pyaudio instantiation
print(f"Device sample rate: {audio.get_device_info_by_index(1)['defaultSampleRate']}")

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)

player = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,output = True, \
                    frames_per_buffer=chunk)


print("recording")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk, exception_on_overflow=False)
    frames.append(data)
    player.write(data,chunk)

    # stop recording when the button is pressed
    if not GPIO.input(BUTTON_GPIO):
        if not pressed:
            print("Button pressed!")
            pressed = True
            break
        # button not pressed (or released)
    else:
        pressed = False

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()

os.system(f"obexftp --nopath -noconn --uuid none --bluetooth {MACADD} --channel 12 -put {wav_output_filename}")
