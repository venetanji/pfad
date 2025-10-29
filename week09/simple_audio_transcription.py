import asyncio
import pyaudio
import time
import base64
import json
import websockets

# Audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000  # 16kHz for OpenAI Realtime API

# OpenAI Realtime API WebSocket endpoint
WEBSOCKET_URL = "ws://localhost:8000/v1/realtime?intent=transcription&model=whisper-1"
API_KEY = ""  # Leave empty for local servers that don't require authentication

class RealtimeAudioTranscriber:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.recording = False
        self.transcriptions = []
        self.audio_queue = asyncio.Queue()
        
    def list_audio_devices(self):
        """List available audio input devices"""
        print("Available audio input devices:")
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  {i}: {info['name']} (channels: {info['maxInputChannels']})")
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio input stream"""
        if self.recording:
            # Put audio data into queue for async processing
            try:
                self.audio_queue.put_nowait(in_data)
            except asyncio.QueueFull:
                # Skip frame if queue is full
                pass
        return (None, pyaudio.paContinue)
    
    async def stream_audio_to_websocket(self, websocket, device_index=None):
        """Stream audio data to WebSocket"""
        # Open audio stream
        stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=CHUNK,
            stream_callback=self.audio_callback
        )
        
        self.recording = True
        stream.start_stream()
        
        try:
            while self.recording:
                # Get audio data from queue
                try:
                    audio_data = await asyncio.wait_for(self.audio_queue.get(), timeout=0.1)
                    
                    # Convert to base64 and send via WebSocket
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    
                    message = {
                        "type": "input_audio_buffer.append",
                        "audio": audio_base64
                    }
                    
                    await websocket.send(json.dumps(message))
                    
                except asyncio.TimeoutError:
                    # No audio data available, continue
                    continue
                    
        finally:
            stream.stop_stream()
            stream.close()
    
    async def receive_transcriptions(self, websocket):
        """Receive transcription results from WebSocket"""
        try:
            async for message in websocket:
                try:
                    event = json.loads(message)
                    
                    # Handle different event types
                    if event.get('type') == 'input_audio_buffer.committed':
                        print("Audio buffer committed")
                    
                    elif event.get('type') == 'conversation.item.input_audio_transcription.completed':
                        transcript = event.get('transcript', '')
                        if transcript.strip():
                            timestamp = time.strftime("%H:%M:%S")
                            print(f"\n[{timestamp}] Transcription: {transcript}")
                            self.transcriptions.append((timestamp, transcript))
                    
                    elif event.get('type') == 'conversation.item.input_audio_transcription.failed':
                        error = event.get('error', {})
                        print(f"Transcription failed: {error}")
                    
                    elif event.get('type') == 'error':
                        error = event.get('error', {})
                        print(f"WebSocket error: {error}")
                        
                except json.JSONDecodeError:
                    print(f"Failed to decode message: {message}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
    
    async def setup_transcription_session(self, websocket):
        """Setup the transcription session configuration"""
        session_config = {
            "type": "transcription.update",
            "id": "session_abc123",
            "audio": {
                "input": {
                    "format": {
                        "type": "audio/pcm",
                        "rate": 24000
                    },
                    "noise_reduction": {
                        "type": "near_field"
                    },
                    "transcription": {
                        "model": "whisper-1",
                        "prompt": "",
                        "language": "en"
                    },
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5,
                        "prefix_padding_ms": 300,
                        "silence_duration_ms": 500
                    }
                }
            }
        }
        
        
        await websocket.send(json.dumps(session_config))
        print("Transcription session configured")
    
    async def transcribe_realtime(self, device_index=None):
        """Main transcription function using WebSocket realtime API"""
        print("Starting realtime transcription...")
        print("Press Ctrl+C to stop\n")
        
        # Configure audio input device
        if device_index is not None:
            try:
                device_info = self.p.get_device_info_by_index(device_index)
                print(f"Using device: {device_info['name']}")
            except Exception as e:
                print(f"Warning: Could not get device info: {e}")
        
        try:
            # Setup WebSocket headers
            headers = {}
            if API_KEY and API_KEY.startswith("sk-"):
                headers["Authorization"] = f"Bearer {API_KEY}"
            
            # Connect to WebSocket
            async with websockets.connect(WEBSOCKET_URL, additional_headers=headers if headers else None) as websocket:
                print("Connected to Realtime API")
                
                # Setup transcription session
                await self.setup_transcription_session(websocket)
                
                # Create tasks for streaming audio and receiving transcriptions
                audio_task = asyncio.create_task(
                    self.stream_audio_to_websocket(websocket, device_index)
                )
                transcription_task = asyncio.create_task(
                    self.receive_transcriptions(websocket)
                )
                
                # Run until interrupted
                try:
                    await asyncio.gather(audio_task, transcription_task)
                except KeyboardInterrupt:
                    print("\nRecording interrupted by user")
                finally:
                    self.recording = False
                    audio_task.cancel()
                    transcription_task.cancel()
                    
        except websockets.exceptions.InvalidStatusCode as e:
            print(f"Connection failed with status code: {e.status_code}")
        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running on localhost:8000.")
        except Exception as e:
            print(f"Error: {e}")
    
    def cleanup(self):
        """Clean up PyAudio resources"""
        self.p.terminate()
    
    def get_transcriptions(self):
        """Get all transcriptions"""
        return self.transcriptions
    




async def main():
    """Main function"""
    transcriber = RealtimeAudioTranscriber()
    
    print("=== Realtime Audio Transcription ===")
    print("Press Ctrl+C to stop\n")
    
    # List available audio devices
    transcriber.list_audio_devices()
    
    # Get user input for device selection
    device_input = input("\nEnter device index (or press Enter for default): ").strip()
    device_index = None
    if device_input:
        try:
            device_index = int(device_input)
        except ValueError:
            print("Invalid device index, using default")
            device_index = None
    
    try:
        # Start realtime transcription
        await transcriber.transcribe_realtime(device_index=device_index)
        
        # Display final transcriptions
        transcriptions = transcriber.get_transcriptions()
        if transcriptions:
            print("\n=== Final Transcriptions ===")
            for timestamp, text in transcriptions:
                print(f"[{timestamp}] {text}")
        else:
            print("\nNo transcriptions received")
            
    finally:
        transcriber.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Error: {e}")