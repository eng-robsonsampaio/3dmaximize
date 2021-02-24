import pyaudio
import time
import wave
import sys
import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt

CHANNELS = 1
RATE = 44100
CHUNK = 4096
FORMAT = pyaudio.paInt16

p = pyaudio.PyAudio()

#wave file
AUDIO_FRAME = []

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_test(data, cutoff, fs, order=5):
    w = cutoff/fs/2
    b, a = butter(order, w, btype='low', analog=False)
    out_data = filtfilt(b, a, data)
    print(type(out_data))
    return out_data

def callback(in_data, frame_count, time_info, flag):
#    out_data =  butter_lowpass_filter(in_data, cutoff=10000, fs=RATE)
    out_data = butter_test(data=in_data, cutoff=1000, fs=RATE, order=5)
    AUDIO_FRAME.append(out_data)
    return (out_data, pyaudio.paContinue)


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                input_device_index=1,
                output_device_index=1,
                stream_callback=callback,
                frames_per_buffer=CHUNK)

stream.start_stream()

while stream.is_active():
    time.sleep(5)
    stream.stop_stream()

stream.close()
p.terminate()
print(f"Audio size:{np.size(AUDIO_FRAME)}")
wavefile = wave.open("audio.wav",'wb')
wavefile.setnchannels(CHANNELS)
wavefile.setsampwidth(p.get_sample_size(FORMAT))
wavefile.setframerate(RATE)
wavefile.writeframes(b''.join(AUDIO_FRAME))
wavefile.close()
