import asyncio
import pyaudio
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 128
ROLLING_WINDOW = 4 * RATE  # 10 seconds rolling window

# Initialize PyAudio
p = pyaudio.PyAudio()
audio_queue = asyncio.Queue()
global buffer
buffer = np.zeros(ROLLING_WINDOW, dtype=np.int16)

# Callback function for input stream
def input_callback(in_data, frame_count, time_info, status):
    audio_queue.put_nowait(in_data)
    return (None, pyaudio.paContinue)

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=1,
                stream_callback=input_callback)

# Async function to process audio data
def process_audio():
    global buffer
    print("Loopback started. Press Ctrl+C to stop.")
    while True:
        if audio_queue.empty():
            time.sleep(0.01)
            continue
        else:
            data = audio_queue.get_nowait()
            waveform = np.frombuffer(data, dtype=np.int16)
            buffer = np.roll(buffer, -len(waveform))
            buffer[-len(waveform):] = waveform
        
  


def update_plot():
    fig, ax = plt.subplots()
    x = np.arange(0, ROLLING_WINDOW)
    line, = ax.plot(x, np.zeros(ROLLING_WINDOW))
    ax.set_ylabel('Amplitude')
    ax.set_ylim(-2**12, 2**12)

    def update_frame(frame):
        global buffer
        new_data = np.frombuffer(buffer, dtype=np.int16)
        line.set_ydata(new_data)
        return line,

    anim = animation.FuncAnimation(fig, update_frame, blit=False, interval=50)
    plt.show()


# Run the event loop
async def main():
    # run process audio in separate thread
    asyncio.get_running_loop().run_in_executor(None, process_audio)
    update_plot()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
finally:
    # Stop and close streams
    stream.stop_stream()
    stream.close()
    p.terminate()