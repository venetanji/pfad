import pyaudio
import numpy as np

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)

# generate random audio 
while True:
    audio = np.random.rand(44100)
    stream.write(audio.astype(np.float32))
    print("Playing 1 second of audio")

    wait = input("Press any key to continue")

