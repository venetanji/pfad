import pygame
import pyaudio
import numpy as np
import colorsys
from scipy import signal
import threading
import queue
import time

class PygameSpectrogram:
    def __init__(self, width=1200, height=800):
        # Display settings
        self.width = width
        self.height = height
        self.spec_height = height // 2
        self.wave_height = height // 4
        
        # Audio settings
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.ROLLING_WINDOW = 4 * self.RATE  # 4 seconds
        
        # Spectrogram settings
        self.NFFT = 1024
        self.noverlap = 512
        self.freq_bins = self.NFFT // 2 + 1
        self.max_freq_display = 8000  # Show up to 8kHz
        self.freq_bin_display = int((self.max_freq_display / (self.RATE / 2)) * self.freq_bins)
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Real-time Spectrogram & Waveform - Press ESC to quit")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 100, 255)
        self.RED = (255, 100, 100)
        
        # Data buffers
        self.audio_buffer = np.zeros(self.ROLLING_WINDOW, dtype=np.float32)
        self.spectrogram_history = np.zeros((self.freq_bin_display, self.width))
        self.spectrogram_smoothed = np.zeros((self.freq_bin_display, self.width))
        self.audio_queue = queue.Queue()
        
        # Smoothing parameters
        self.temporal_smoothing = 0.7  # How much to blend with previous frame (0-1)
        self.update_counter = 0
        
        # Initialize audio
        self.setup_audio()
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
    def setup_audio(self):
        """Initialize PyAudio stream"""
        self.p = pyaudio.PyAudio()
        
        # Try to find a working input device
        input_device = None
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_device = i
                print(f"Using audio device: {device_info['name']}")
                break
        
        if input_device is None:
            print("No input device found!")
            return
            
        try:
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                input_device_index=input_device,
                stream_callback=self.audio_callback
            )
            self.stream.start_stream()
            print("Audio stream started successfully")
        except Exception as e:
            print(f"Could not open audio stream: {e}")
            self.stream = None
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback function - runs in separate thread"""
        if status:
            print(f"Audio status: {status}")
        
        # Convert audio data to numpy array
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        
        # Add to queue for main thread processing
        try:
            self.audio_queue.put(audio_data, block=False)
        except queue.Full:
            pass  # Drop data if queue is full
        
        return (None, pyaudio.paContinue)
    
    def update_audio_data(self):
        """Process audio data from queue"""
        # Process all available audio data
        while not self.audio_queue.empty():
            try:
                new_data = self.audio_queue.get_nowait()
                # Roll buffer and add new data
                self.audio_buffer = np.roll(self.audio_buffer, -len(new_data))
                self.audio_buffer[-len(new_data):] = new_data
            except queue.Empty:
                break
    
    def compute_spectrogram(self):
        """Compute spectrogram from current audio buffer"""
        if len(self.audio_buffer) < self.NFFT:
            return
        
        # Compute spectrogram using scipy
        try:
            # Use only the most recent portion of the buffer for better real-time response
            recent_buffer = self.audio_buffer[-self.RATE:]  # Last 1 second
            
            if len(recent_buffer) < self.NFFT:
                recent_buffer = self.audio_buffer
            
            frequencies, times, Sxx = signal.spectrogram(
                recent_buffer,
                fs=self.RATE,
                nperseg=self.NFFT,
                noverlap=self.noverlap,
                window='hann'
            )
            
            # Debug: Check if we're getting data
            max_power = np.max(Sxx)
            if hasattr(self, 'debug_counter'):
                self.debug_counter += 1
            else:
                self.debug_counter = 0
            
            if self.debug_counter % 30 == 0:  # Print every second at 30fps
                print(f"Spectrogram max power: {max_power:.2e}, Shape: {Sxx.shape}")
            
            # Convert to dB scale with better handling
            Sxx_db = 10 * np.log10(Sxx + 1e-12)  # Smaller epsilon for better sensitivity
            
            # Adaptive normalization based on current data
            current_min = np.percentile(Sxx_db, 10)  # 10th percentile
            current_max = np.percentile(Sxx_db, 95)  # 95th percentile
            
            # Use adaptive range with fallback
            min_db = max(current_min, -80)  # Don't go below -80dB
            max_db = min(current_max, 20)   # Don't go above 20dB
            
            # Ensure we have a reasonable range
            if max_db - min_db < 20:
                max_db = min_db + 40
            
            # Normalize to 0-1 range
            Sxx_normalized = np.clip((Sxx_db - min_db) / (max_db - min_db), 0, 1)
            
            # Apply gamma correction to make low values more visible
            gamma = 0.5
            Sxx_normalized = np.power(Sxx_normalized, gamma)
            
            # Update spectrogram history (scroll left, add new column)
            if times.shape[0] > 0:
                # Take the latest time slice, or average if multiple
                if Sxx_normalized.shape[1] > 1:
                    latest_spectrum = np.mean(Sxx_normalized[:self.freq_bin_display, -3:], axis=1)
                else:
                    latest_spectrum = Sxx_normalized[:self.freq_bin_display, -1]
                
                # Scroll history left and add new column
                self.spectrogram_history = np.roll(self.spectrogram_history, -1, axis=1)
                self.spectrogram_history[:, -1] = latest_spectrum
                
                # Apply temporal smoothing to reduce flickering
                self.spectrogram_smoothed = (
                    self.temporal_smoothing * self.spectrogram_smoothed + 
                    (1 - self.temporal_smoothing) * self.spectrogram_history
                )
                
        except Exception as e:
            print(f"Error computing spectrogram: {e}")
            import traceback
            traceback.print_exc()
    
    def value_to_color(self, value):
        """Convert normalized value (0-1) to color with smooth transitions"""
        # Apply slight compression to reduce extreme values
        value = np.power(value, 0.8)  # Compress dynamic range slightly
        
        if value < 0.02:  # Very low threshold
            return (5, 5, 15)  # Very dark blue instead of black
        
        # Smooth color transitions using interpolation
        # Blue -> Cyan -> Green -> Yellow -> Red
        if value < 0.25:
            # Dark blue to bright blue
            t = value / 0.25
            r = int(t * 30)
            g = int(t * 30) 
            b = int(80 + t * 175)
        elif value < 0.45:
            # Blue to cyan
            t = (value - 0.25) / 0.2
            r = int(30 + t * 70)
            g = int(30 + t * 225)
            b = 255
        elif value < 0.65:
            # Cyan to green
            t = (value - 0.45) / 0.2
            r = int(100 * (1 - t))
            g = 255
            b = int(255 * (1 - t))
        elif value < 0.85:
            # Green to yellow
            t = (value - 0.65) / 0.2
            r = int(t * 255)
            g = 255
            b = 0
        else:
            # Yellow to red
            t = (value - 0.85) / 0.15
            r = 255
            g = int(255 * (1 - t))
            b = 0
        
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    def draw_spectrogram(self):
        """Draw the spectrogram"""
        spec_rect = pygame.Rect(0, 0, self.width, self.spec_height)
        
        # Clear spectrogram area with dark background
        pygame.draw.rect(self.screen, (20, 20, 20), spec_rect)
        
        # Check if we have any data
        max_value = np.max(self.spectrogram_smoothed)
        if max_value < 1e-6:
            # Draw "no signal" message
            no_signal_text = self.font.render("No audio signal detected - make some noise!", True, (100, 100, 100))
            text_rect = no_signal_text.get_rect(center=(self.width//2, self.spec_height//2))
            self.screen.blit(no_signal_text, text_rect)
            return
        
        # Draw spectrogram pixels with improved scaling
        pixel_size = max(1, min(2, self.width // 600))  # Smaller pixels for smoother look
        
        for x in range(0, self.width, pixel_size):
            for y in range(0, min(self.freq_bin_display, self.spec_height), pixel_size):
                if x < self.spectrogram_smoothed.shape[1] and y < self.spectrogram_smoothed.shape[0]:
                    value = self.spectrogram_smoothed[y, x]
                    
                    # Skip very low values for performance
                    if value > 0.1:
                        color = self.value_to_color(value)
                        
                        # Calculate position (flip Y axis)
                        draw_y = self.spec_height - (y * self.spec_height // self.freq_bin_display) - pixel_size
                        draw_y = max(0, min(self.spec_height - pixel_size, draw_y))
                        
                        # Draw pixel
                        pixel_rect = pygame.Rect(x, draw_y, pixel_size, pixel_size)
                        pygame.draw.rect(self.screen, color, pixel_rect)
        
        # Draw frequency labels
        label_y_positions = [0.1, 0.3, 0.5, 0.7, 0.9]
        for pos in label_y_positions:
            freq = pos * self.max_freq_display
            y_pos = self.spec_height - int(pos * self.spec_height)
            
            label = self.small_font.render(f"{freq/1000:.1f}kHz", True, self.WHITE)
            self.screen.blit(label, (5, y_pos))
        
        # Title
        title = self.font.render("Spectrogram (Frequency vs Time)", True, self.WHITE)
        self.screen.blit(title, (10, 10))
    
    def draw_waveform(self):
        """Draw the audio waveform"""
        wave_y_start = self.spec_height + 20
        wave_rect = pygame.Rect(0, wave_y_start, self.width, self.wave_height)
        
        # Clear waveform area
        pygame.draw.rect(self.screen, self.BLACK, wave_rect)
        
        # Draw waveform
        if len(self.audio_buffer) > 1:
            # Downsample for display
            samples_per_pixel = len(self.audio_buffer) // self.width
            if samples_per_pixel > 0:
                points = []
                for x in range(self.width):
                    start_idx = x * samples_per_pixel
                    end_idx = min(start_idx + samples_per_pixel, len(self.audio_buffer))
                    
                    if end_idx > start_idx:
                        # Use RMS for each pixel to show energy
                        segment = self.audio_buffer[start_idx:end_idx]
                        rms = np.sqrt(np.mean(segment**2))
                        
                        # Scale to waveform area
                        y = wave_y_start + self.wave_height // 2 - int(rms * self.wave_height * 10)
                        y = max(wave_y_start, min(wave_y_start + self.wave_height, y))
                        points.append((x, y))
                
                # Draw waveform line
                if len(points) > 1:
                    pygame.draw.lines(self.screen, self.GREEN, False, points, 1)
        
        # Draw center line
        center_y = wave_y_start + self.wave_height // 2
        pygame.draw.line(self.screen, (50, 50, 50), (0, center_y), (self.width, center_y), 1)
        
        # Title
        title = self.font.render("Waveform (Amplitude vs Time)", True, self.WHITE)
        self.screen.blit(title, (10, wave_y_start - 15))
    
    def draw_info(self):
        """Draw information panel"""
        info_y_start = self.spec_height + self.wave_height + 40
        
        # Audio info
        if self.stream and self.stream.is_active():
            status_color = self.GREEN
            status_text = "ACTIVE"
        else:
            status_color = self.RED
            status_text = "INACTIVE"
        
        # Calculate audio level
        audio_level = np.sqrt(np.mean(self.audio_buffer[-1000:]**2))  # RMS of recent samples
        spec_max = np.max(self.spectrogram_smoothed)
        
        info_lines = [
            f"Audio Status: {status_text}",
            f"Sample Rate: {self.RATE} Hz",
            f"Audio Level: {audio_level:.4f}",
            f"Spec Max: {spec_max:.4f}",
            f"Smoothing: {self.temporal_smoothing:.2f}",
            f"Frequency Range: 0 - {self.max_freq_display/1000:.1f} kHz",
            "Controls: ↑/↓ adjust smoothing, R reset, ESC quit"
        ]
        
        for i, line in enumerate(info_lines):
            color = status_color if i == 0 else self.WHITE
            text = self.small_font.render(line, True, color)
            self.screen.blit(text, (10, info_y_start + i * 20))
    
    def run(self):
        """Main application loop"""
        print("Starting spectrogram display...")
        print("Make some noise to see the visualization!")
        
        running = True
        frame_count = 0
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        # Increase smoothing (less flickering, more lag)
                        self.temporal_smoothing = min(0.95, self.temporal_smoothing + 0.05)
                        print(f"Smoothing: {self.temporal_smoothing:.2f}")
                    elif event.key == pygame.K_DOWN:
                        # Decrease smoothing (more responsive, more flickering)
                        self.temporal_smoothing = max(0.1, self.temporal_smoothing - 0.05)
                        print(f"Smoothing: {self.temporal_smoothing:.2f}")
                    elif event.key == pygame.K_r:
                        # Reset smoothing to default
                        self.temporal_smoothing = 0.7
                        print(f"Smoothing reset to: {self.temporal_smoothing:.2f}")
            
            # Update audio data
            self.update_audio_data()
            
            # Compute spectrogram at a controlled rate to reduce flickering
            self.update_counter += 1
            if self.update_counter % 2 == 0:  # Every 2nd frame (15 FPS updates)
                self.compute_spectrogram()
            
            # Clear screen
            self.screen.fill(self.BLACK)
            
            # Draw components
            self.draw_spectrogram()
            self.draw_waveform()
            self.draw_info()
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(30)  # 30 FPS
            frame_count += 1
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        if hasattr(self, 'stream') and self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'p'):
            self.p.terminate()
        pygame.quit()

if __name__ == "__main__":
    try:
        app = PygameSpectrogram()
        app.run()
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()