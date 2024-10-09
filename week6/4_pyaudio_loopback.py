import pyaudio

# Parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open input stream
input_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      input_device_index=1,
                      frames_per_buffer=CHUNK)

# Open output stream
output_stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       output=True,
                       frames_per_buffer=CHUNK)

print("Loopback started. Press Ctrl+C to stop.")

try:
    while True:
        data = input_stream.read(CHUNK)
        output_stream.write(data)
except KeyboardInterrupt:
    print("Loopback stopped.")

# Close streams
input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()

# Terminate PyAudio
p.terminate()