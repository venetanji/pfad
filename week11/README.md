# Week 11: NDI Hand Tracking with OSC

This directory contains examples for integrating third-party creative tools with Python, including NDI video streaming, hand tracking, and OSC communication.

## NDI Hand Tracking Application

### Overview

`ndi_hand_tracking.py` is a comprehensive example that demonstrates:

- **NDI Video Reception**: Receives video frames from an NDI source over the network using `cyndilib`
- **Hand Tracking**: Uses MediaPipe to detect and track hands in real-time
- **Gesture Analysis**: Calculates pinch gestures between thumb and index finger
- **OSC Communication**: Broadcasts hand tracking data via OSC for use in other applications
- **Visual Feedback**: Displays annotated video with hand overlays

### Features

#### Hand Tracking Metrics

For each detected hand (up to 2 hands), the application calculates:

- **Position**: X/Y center position (normalized 0-1)
- **Pinch Length**: Distance between thumb tip and index finger tip (normalized)
- **Pinch Angle**: Rotation angle of the pinch segment (in degrees)
- **Pinch State**: Boolean flag indicating if hand is actively pinching

#### OSC Messages

Hand data is broadcast via OSC with the following address patterns:

```
/hand/[hand_id]/position [x, y]        # Hand center position (0-1)
/hand/[hand_id]/pinch_length [length]  # Normalized distance (0-1)
/hand/[hand_id]/pinch_angle [angle]    # Rotation angle (-180 to 180)
/hand/[hand_id]/is_pinching [state]    # 1.0 or 0.0
```

Where `[hand_id]` is 0 for the first hand and 1 for the second hand.

#### Visual Overlay

The OpenCV display window shows:

- Complete hand skeleton (MediaPipe landmarks)
- Pinch segment between thumb and index finger
  - **Blue line**: Normal state
  - **Green line**: Pinching detected
- Yellow circles at thumb and index tips
- Cyan dot at hand center
- Real-time hand metrics (position, pinch data)
- Status information (source, hand count, frame number)

### Installation

1. Install dependencies:

```bash
cd week11
pip install -r requirements.txt
```

#### Dependencies

- `cyndilib` - NDI video streaming
- `opencv-python` - Computer vision and display
- `mediapipe` - Hand tracking AI model
- `python-osc` - OSC communication protocol
- `numpy` - Numerical operations
- `python-dotenv` - Environment configuration

### Testing and Validation

Before running the full application, you can validate the setup:

#### Run Validation Tests

```bash
python test_validation.py
```

This tests:
- File structure
- Week08 integration
- Requirements completeness
- Code syntax
- Hand calculation logic
- OSC message patterns

#### Test OSC Messages

To test your OSC receiver without NDI/camera setup:

```bash
python osc_demo.py
```

This sends animated example OSC messages showing what the real application sends.

Options:
- `--osc-ip` : IP address to send to (default: 127.0.0.1)
- `--osc-port` : Port number (default: 8000)
- `--duration` : How long to run in seconds (default: 10)

### Usage

#### Basic Usage (Auto-detect NDI source)

```bash
python ndi_hand_tracking.py
```

#### Specify NDI Source

```bash
python ndi_hand_tracking.py --ndi-source "OBS (Output)"
```

#### Custom OSC Configuration

```bash
python ndi_hand_tracking.py --osc-ip 192.168.1.100 --osc-port 9000
```

#### All Options

```bash
python ndi_hand_tracking.py \
  --ndi-source "Source Name" \
  --osc-ip 127.0.0.1 \
  --osc-port 8000
```

### Command Line Arguments

- `--ndi-source` : Name of NDI source to connect to (default: auto-detect first available)
- `--osc-ip` : IP address to send OSC messages (default: 127.0.0.1)
- `--osc-port` : Port number for OSC messages (default: 8000)

### Camera Fallback

If no NDI source is available, the application will automatically fall back to using a regular camera. It uses the camera configuration from `week08/setup_camera.py`.

To configure your camera:

```bash
cd ../week08
python setup_camera.py
```

### Integration with Other Applications

#### TouchDesigner

1. In TouchDesigner, add an "OSC In DAT"
2. Set the network port to match your OSC port (default: 8000)
3. Use the incoming OSC messages in your network:
   - `/hand/0/position` for first hand position
   - `/hand/0/pinch_length` for pinch distance
   - etc.

#### Max/MSP

1. Add `udpreceive` object with your OSC port
2. Add `route /hand/0 /hand/1` to separate hand data
3. Further route messages by parameter (position, pinch_length, etc.)

#### Processing

Use the oscP5 library to receive OSC messages:

```java
import oscP5.*;

OscP5 oscP5;

void setup() {
  oscP5 = new OscP5(this, 8000);
}

void oscEvent(OscMessage msg) {
  if (msg.checkAddrPattern("/hand/0/position")) {
    float x = msg.get(0).floatValue();
    float y = msg.get(1).floatValue();
    // Use x, y values
  }
}
```

### How It Works

#### 1. Video Source

The application first attempts to connect to an NDI source on the network. NDI (Network Device Interface) is a protocol that allows video to be transmitted over standard networks with very low latency. Common NDI sources include:

- OBS Studio (with NDI plugin)
- vMix
- Wirecast
- NDI Scan Converter
- TouchDesigner

If no NDI source is found, it falls back to a regular USB/built-in camera.

#### 2. Hand Detection

MediaPipe Hands is a machine learning solution that detects 21 3D hand landmarks in real-time. The landmarks include:

- Wrist (0)
- Thumb: 1-4 (tip at 4)
- Index finger: 5-8 (tip at 8)
- Middle finger: 9-12 (tip at 12)
- Ring finger: 13-16 (tip at 16)
- Pinky: 17-20 (tip at 20)

#### 3. Pinch Gesture

The pinch gesture is detected by analyzing the distance between:
- Landmark 4 (thumb tip)
- Landmark 8 (index finger tip)

When this distance is less than 5% of the frame diagonal, it's considered a "pinch".

#### 4. Data Calculation

For each hand:

- **Center Position**: Average of all 21 landmark positions
- **Pinch Length**: Euclidean distance between thumb and index tips, normalized by frame diagonal
- **Pinch Angle**: Arc tangent of the vector from thumb to index (atan2)

#### 5. OSC Broadcasting

The calculated data is sent via UDP to the specified IP and port using the OSC protocol. OSC is widely supported in creative coding environments and allows for easy integration with audio/visual software.

### Troubleshooting

#### No NDI sources found

- Ensure NDI source is running and on the same network
- Check firewall settings (NDI uses UDP ports 5960-5970)
- Wait a few seconds after starting NDI source for discovery

#### Camera not working

- Run camera setup: `cd ../week08 && python setup_camera.py`
- Ensure camera is not in use by another application
- Try unplugging and reconnecting the camera

#### OSC messages not received

- Check that receiving application is listening on correct port
- Verify IP address (use 127.0.0.1 for local, or actual IP for network)
- Use an OSC monitor tool to verify messages are being sent

#### Performance issues

- Reduce video resolution in NDI source
- Lower MediaPipe model complexity (edit `model_complexity` in code)
- Close other applications using CPU/GPU

### Educational Notes

This example demonstrates several important concepts for interactive art:

1. **Network Video**: NDI allows video to flow between applications over standard networks
2. **Computer Vision**: MediaPipe provides ready-to-use AI models for detecting humans
3. **Gesture Recognition**: Simple distance/angle calculations create meaningful interactions
4. **OSC Protocol**: Standard way to send control data between creative applications
5. **Real-time Processing**: Balancing accuracy with frame rate for interactive work

### Example Projects

This application can be used as a foundation for:

- **Interactive Installations**: Control visuals/sound with hand gestures
- **VJ Tools**: Hand-controlled video effects in TouchDesigner
- **Music Controllers**: Map pinch gestures to synthesizer parameters
- **Game Controls**: Alternative input method using hand tracking
- **Accessibility Tools**: Hands-free control interfaces

### Credits

- **MediaPipe**: Google's open-source ML framework
- **cyndilib**: Python wrapper for NDI SDK
- **python-osc**: OSC implementation for Python
- **OpenCV**: Computer vision library

### Helper Scripts

#### test_validation.py

Validates the implementation without requiring dependencies:
- Tests file structure and integration
- Validates calculation logic
- Checks OSC message patterns
- Verifies code syntax

Run with: `python test_validation.py`

#### osc_demo.py

Sends example OSC messages for testing receivers:
- Simulates animated hand movements
- No camera or NDI required
- Useful for testing TouchDesigner/Max patches

Run with: `python osc_demo.py [--osc-ip IP] [--osc-port PORT] [--duration SECONDS]`

### License

Educational example for PFAD (Programming for Art and Design) course.

---

## Other Week 11 Examples

- `blender/` - Blender integration examples
- `orange/` - Orange Data Mining workflows  
- `touchdesigner/` - TouchDesigner Python integration including NDI examples
