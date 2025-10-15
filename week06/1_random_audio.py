import pyaudio
import numpy as np

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True, output_device_index=10)

# generate random audio 
while True:
    audio = np.random.rand(44100) * 0.1
    stream.write(audio.astype(np.float32))
    print("Playing 1 second of audio")

    
    

