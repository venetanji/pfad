import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
FORMAT = pyaudio.paInt16
INPUTFORMAT = pyaudio.paFloat32

CHANNELS = 1
RATE = 44100
CHUNK = 1024
ROLLING_WINDOW = 10 * RATE  # 10 seconds rolling window

# Initialize PyAudio
p = pyaudio.PyAudio()
buffer = np.zeros(ROLLING_WINDOW, dtype=np.float32)

# Open stream
stream = p.open(format=INPUTFORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=1)

# Create a figure for plotting
fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
x = np.arange(0, ROLLING_WINDOW)
line, = ax1.plot(x, np.zeros(ROLLING_WINDOW))
ax1.set_ylabel('Amplitude')

# Function to update the plot
def update_plot(frame):
    global buffer
    chunk = stream.read(CHUNK)
    new_data = np.frombuffer(chunk, dtype=np.float32)
    buffer = np.roll(buffer, -len(new_data))
    print(len(buffer))
    line.set_ydata(buffer)
    ax2.clear()
    Pxx, freqs, bins, im = ax2.specgram(buffer, NFFT=1024, Fs=RATE, noverlap=512)
    ax2.set_ylabel('Frequency (Hz)')
    ax2.set_xlabel('Time (s)')
    
    return line, im

# Set up plot to call update function periodically
ani = animation.FuncAnimation(fig, update_plot, blit=False, interval=50)
plt.show()

# Close the stream
while True:
    pass

stream.stop_stream()
stream.close()
p.terminate()