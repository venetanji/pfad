import asyncio
import pyaudio

# Parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()

# Create asyncio queues
global input_queue, output_queue
input_queue = asyncio.Queue()
output_queue = asyncio.Queue()

# Callback function for input stream
def input_callback(in_data, frame_count, time_info, status):
    input_queue.put_nowait(in_data)
    return (None, pyaudio.paContinue)

# Callback function for output stream
def output_callback(in_data, frame_count, time_info, status):
    try:
        data = output_queue.get_nowait()
    except asyncio.QueueEmpty:
        data = b'\x00' * CHUNK * 2  # Silence if no data available
    return (data, pyaudio.paContinue)

# Open input stream
input_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      input_device_index=1,
                      frames_per_buffer=CHUNK,
                      stream_callback=input_callback)

# Open output stream
output_stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       output=True,
                       frames_per_buffer=CHUNK,
                       stream_callback=output_callback)

async def process_audio():
    print("Loopback started. Press Ctrl+C to stop.")
    try:
        while True:
            if input_queue.empty():
                await asyncio.sleep(0.1)
                continue
            data = await input_queue.get()
            await output_queue.put(data)
    except asyncio.CancelledError:
        print("Loopback stopped.")

# Start streams
input_stream.start_stream()
output_stream.start_stream()

# Run the event loop
try:
    asyncio.run(process_audio())
except KeyboardInterrupt:
    pass
finally:
    # Stop and close streams
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()

    # Terminate PyAudio
    p.terminate()
