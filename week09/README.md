# Week 09 - WebSockets and Speech-to-Text

This week builds upon the previous week's agent bot work and introduces real-time speech-to-text capabilities using WebSockets and WebRTC.

## Files Overview

### Core WebSocket Examples
- `websocket_server_echo.py` - Basic WebSocket echo server
- `websocket_server_echo_ping.py` - Echo server with periodic ping messages
- `websocket_client_example.py` - Simple WebSocket client
- `pygame_websocket.py` - WebSocket integration with pygame and asyncio

### Speech-to-Text Examples
- `speech_to_text_webrtc.py` - **NEW**: Streamlit WebRTC speech-to-text demo (WebSocket-based)
- `simple_audio_transcription.py` - **NEW**: Continuous audio transcription using OpenAI-compatible API
- `simple_transcription_test.py` - **NEW**: Basic single-recording transcription test

### Other Files
- `fastapi_example.py` - FastAPI server example
- `compose.yml` - Docker Compose configuration with Faster Whisper service
- `requirements.txt` - Python dependencies

## New Speech-to-Text Features

### 1. Streamlit WebRTC Speech-to-Text (`speech_to_text_webrtc.py`)

A real-time web-based speech recognition interface that:
- Uses WebRTC for browser-based audio capture
- Streams audio via WebSockets to Faster Whisper service
- Displays transcriptions in real-time
- Maintains transcription history
- Built with Streamlit for easy web interface

#### Features:
- Real-time audio streaming from browser microphone
- WebSocket connection to Faster Whisper service
- Live transcription display
- Transcription history with timestamps
- Audio format conversion (resampling to 16kHz mono)
- Connection status indicators

### 2. Simple Audio Transcription (`simple_audio_transcription.py`)

A command-line tool for real-time audio transcription that:
- Uses the OpenAI Realtime API WebSocket interface (`/v1/realtime?intent=transcription`)
- Implements pyaudio asyncio patterns from week06 examples
- Streams audio in real-time to OpenAI-compatible transcription service
- Shows live transcriptions with server-side Voice Activity Detection (VAD)
- Displays transcriptions in terminal

#### Features:
- OpenAI Realtime API WebSocket connection
- Real-time audio streaming with pyaudio callbacks
- Server-side Voice Activity Detection (VAD)
- Audio device selection
- Configurable recording duration
- Real-time transcription display
- Graceful shutdown with Ctrl+C
- Base64 audio encoding for WebSocket transmission

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Transcription Service

#### Option A: Faster Whisper Service (for WebRTC demo)

```bash
docker-compose up faster-whisper
```

This starts the Faster Whisper service on port 10300 with:
- Model: `small-int8` (balance of speed and accuracy)
- Language: English
- GPU acceleration (if available)

#### Option B: OpenAI Realtime API (for simple_audio_transcription.py)

For the WebSocket realtime transcription, you have two options:

**Using OpenAI API:**
1. Get an OpenAI API key
2. Update `API_KEY` in `simple_audio_transcription.py`
3. Change `WEBSOCKET_URL` to `"wss://api.openai.com/v1/realtime?intent=transcription"`

**Using Local OpenAI-compatible Server:**
1. Setup a server that supports OpenAI Realtime API on `localhost:8000`
2. Make sure it supports the `/v1/realtime?intent=transcription` WebSocket endpoint
3. Update `API_KEY` if your server requires authentication

### 3. Run the Examples

#### Streamlit WebRTC Demo:
```bash
streamlit run speech_to_text_webrtc.py
```

Then open your browser to the provided URL (usually http://localhost:8501).

#### Command-line Audio Transcription:
```bash
python simple_audio_transcription.py
```

Follow the prompts to select audio device and recording duration.

## Usage Tips

### For WebRTC Demo:
1. Allow microphone access when prompted by browser
2. Click "START" to begin recording
3. Speak clearly into your microphone
4. Watch transcriptions appear in real-time
5. Click "STOP" to end the session

### For Command-line Demo:
1. Choose your microphone from the device list
2. Set recording duration (default 30 seconds)
3. Speak during the recording period
4. Press Ctrl+C to stop early if needed

## Technical Architecture

### WebRTC Demo Pipeline (speech_to_text_webrtc.py):
1. **Audio Capture**: WebRTC (browser-based)
2. **Format Conversion**: Resample to 16kHz mono S16LE
3. **WebSocket Streaming**: Send audio chunks to Faster Whisper
4. **Speech Recognition**: Faster Whisper processes audio
5. **Result Display**: Real-time transcription updates

### Realtime API Pipeline (simple_audio_transcription.py):
1. **Audio Capture**: PyAudio with callback streaming
2. **Format Encoding**: PCM16 audio encoded as base64
3. **WebSocket Realtime API**: OpenAI `/v1/realtime?intent=transcription` endpoint
4. **Server-side VAD**: Voice Activity Detection handles speech segmentation
5. **Real-time Transcription**: Immediate transcription results via WebSocket events

### Key Technologies:
- **WebRTC**: Browser-based audio/video capture
- **WebSockets**: Real-time bidirectional communication
- **Faster Whisper**: Optimized speech recognition service
- **Streamlit**: Web app framework
- **PyAudio**: System audio interface
- **asyncio**: Asynchronous programming

## Connection to Previous Weeks

### Week 06 - Audio Processing:
- Builds on `4a_asyncio_loopback.py` audio handling patterns
- Uses similar pyaudio callback and queue mechanisms
- Applies asyncio patterns for concurrent audio processing

### Week 08 - Computer Vision:
- Similar real-time processing concepts
- WebSocket streaming patterns
- Docker service integration

### Docker Bot (Extra):
- Extends Streamlit interface patterns
- WebSocket communication
- Service containerization concepts

## Troubleshooting

### Common Issues:

1. **"Connection Refused" Error**:
   - Make sure Faster Whisper service is running: `docker-compose up faster-whisper`
   - Check if port 10300 is available

2. **No Audio Input**:
   - Check microphone permissions in browser (WebRTC)
   - Verify audio device selection (command-line)
   - Test with `python list_cameras.py` equivalent for audio

3. **WebRTC Not Starting**:
   - Use HTTPS or localhost (required for WebRTC)
   - Allow microphone access in browser
   - Check browser console for errors

4. **Missing Dependencies**:
   - Install with: `pip install -r requirements.txt`
   - Some systems may need additional audio libraries

## Extension Ideas

1. **Multi-language Support**: Change WebSocket endpoint language parameter
2. **Real-time Translation**: Add translation service after transcription
3. **Voice Commands**: Parse transcriptions for specific commands
4. **Audio Recording**: Save audio files along with transcriptions
5. **WebSocket Broadcasting**: Share transcriptions with multiple clients
6. **Integration with LLM**: Use transcriptions as input to chatbot (like docker-bot)

## Docker Services

The `compose.yml` includes:
- **faster-whisper**: GPU-accelerated speech recognition service
- Configurable model size and language
- Persistent configuration storage
- Automatic restart policy

## Related Files

- See `extra/docker-bot/` for the base Streamlit chatbot implementation
- See `week06/4a_asyncio_loopback.py` for audio processing patterns
- See other week09 WebSocket examples for communication patterns