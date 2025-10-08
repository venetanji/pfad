import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import warnings

# Suppress matplotlib warnings
warnings.filterwarnings('ignore')

# Parameters
INPUTFORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
ROLLING_WINDOW = 2 * RATE  # 2 seconds

def find_input_device():
    """Find a working input device"""
    p = pyaudio.PyAudio()
    
    print("Available audio devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            print(f"  {i}: {device_info['name']}")
    
    try:
        default_input = p.get_default_input_device_info()
        device_index = default_input['index']
        print(f"\nUsing: {default_input['name']}")
        return p, device_index
    except:
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                print(f"\nUsing fallback: {device_info['name']}")
                return p, i
        print("No input devices found!")
        p.terminate()
        sys.exit(1)

# Initialize
p, input_device_index = find_input_device()
buffer = np.zeros(ROLLING_WINDOW, dtype=np.float32)

# Open stream
try:
    stream = p.open(format=INPUTFORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=input_device_index)
    print("Audio stream opened successfully")
except Exception as e:
    print(f"Error: {e}")
    p.terminate()
    sys.exit(1)

# Create figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Waveform plot
line, = ax1.plot(np.arange(ROLLING_WINDOW), buffer, 'b-', linewidth=0.5)
ax1.set_ylabel('Amplitude')
ax1.set_title('Audio Waveform')
ax1.grid(True, alpha=0.3)

# Spectrogram setup
ax2.set_ylabel('Frequency (Hz)')
ax2.set_xlabel('Time (s)')
ax2.set_title('Spectrogram - ALWAYS VISIBLE')

def update_plot(frame):
    global buffer
    
    try:
        # Read audio
        chunk = stream.read(CHUNK, exception_on_overflow=False)
        new_data = np.frombuffer(chunk, dtype=np.float32)
        
        if len(new_data) == 0:
            return line,
        
        # Update buffer
        buffer = np.roll(buffer, -len(new_data))
        buffer[-len(new_data):] = new_data
        
        # Update waveform
        line.set_ydata(buffer)
        
        # Calculate signal stats
        rms = np.sqrt(np.mean(buffer**2))
        max_amp = np.max(np.abs(buffer))
        
        # Dynamic y-axis for waveform
        if max_amp > 1e-6:
            ax1.set_ylim(-max_amp*1.2, max_amp*1.2)
        else:
            ax1.set_ylim(-0.001, 0.001)  # Very small range for quiet signals
        
        ax1.set_title(f'Audio Waveform (RMS: {rms:.2e}, Max: {max_amp:.2e})')
        
        # FORCE SPECTROGRAM DISPLAY
        ax2.clear()
        ax2.set_ylabel('Frequency (Hz)')
        ax2.set_xlabel('Time (s)')
        
        # Prepare signal for spectrogram
        display_signal = buffer.copy()
        
        # If signal is too quiet, amplify it dramatically
        if rms < 1e-4:
            display_signal = display_signal * 10000  # Multiply by 10,000
            amplification_text = " (Amplified x10,000)"
        elif rms < 1e-3:
            display_signal = display_signal * 1000   # Multiply by 1,000
            amplification_text = " (Amplified x1,000)"
        else:
            amplification_text = ""
        
        # Add small noise to prevent log(0) errors
        display_signal = display_signal + np.random.normal(0, 1e-10, len(display_signal))
        
        try:
            # ALWAYS compute spectrogram
            Pxx, freqs, bins, im = ax2.specgram(
                display_signal,
                NFFT=512,
                Fs=RATE,
                noverlap=256,
                cmap='hot',
                vmin=-140,  # Very low minimum to show everything
                vmax=-40
            )
            
            ax2.set_ylim(0, 4000)  # Show up to 4kHz
            ax2.set_title(f'Spectrogram{amplification_text} (RMS: {rms:.2e})')
            
            # Add colorbar once
            if not hasattr(update_plot, 'colorbar_added'):
                try:
                    plt.colorbar(im, ax=ax2, label='Power (dB)')
                    update_plot.colorbar_added = True
                except:
                    pass
                    
        except Exception as e:
            ax2.text(0.5, 0.5, f'Spectrogram Error: {str(e)[:50]}', 
                   transform=ax2.transAxes, ha='center', va='center',
                   fontsize=10, color='red')
        
        return line,
    
    except Exception as e:
        print(f"Update error: {e}")
        return line,

print("Starting FORCED spectrogram display...")
print("This version will show spectrogram even for very quiet signals!")
print("Make some noise to see better results!")

plt.tight_layout()

try:
    ani = animation.FuncAnimation(fig, update_plot, interval=100, blit=False, cache_frame_data=False)
    plt.show()
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    print("Cleaning up...")
    try:
        stream.stop_stream()
        stream.close()
        p.terminate()
    except:
        pass
    print("Done!")