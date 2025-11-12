# Week 11: NDI Hand Tracking with OSC

A comprehensive hand tracking application that receives video from NDI sources, tracks hands using MediaPipe, and broadcasts hand data via OSC to other creative applications.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd week11
pip install -r requirements.txt
```

### 2. Test Your Setup
```bash
# Validate everything is working
python test_validation.py

# Test OSC messages (without camera)
python osc_demo.py
```

### 3. Run the Application

**With NDI source:**
```bash
python ndi_hand_tracking.py
```

**With regular camera:**
```bash
# First configure camera (one-time setup)
cd ../week08
python setup_camera.py
cd ../week11

# Then run
python ndi_hand_tracking.py
```

## 📡 What You Get

### OSC Messages
Each hand sends these messages with **consistent hand IDs**:

```
/hand/0/position [x, y]           # Where the hand is (0-1)
/hand/0/pinch_length [distance]   # How close thumb and index are
/hand/0/pinch_angle [angle]       # Rotation angle of the pinch
/hand/0/is_pinching [true/false]  # Is the hand pinching?
```

Second hand uses `/hand/1/...`

### Hand ID Consistency
✅ **New Feature**: Hands maintain consistent IDs even when temporarily lost or when hands cross over each other. The system tracks hand positions between frames to assign stable IDs.

### Visual Feedback
- Complete hand skeleton overlay
- Pinch detection (blue = normal, green = pinching)
- Hand center indicators
- Real-time metrics display

## 🎯 Integration Examples

### TouchDesigner
1. Add "OSC In DAT" set to port 8000
2. Watch OSC messages flow in
3. Map `/hand/0/position` to visual parameters
4. Use `/hand/0/is_pinching` to trigger effects

### Max/MSP
1. Use `udpreceive 8000`
2. Route with `route /hand/0 /hand/1`
3. Map pinch gestures to synthesis parameters

### Processing
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
    // Control graphics with hand position
  }
}
```

## ⚙️ Command Line Options

```bash
python ndi_hand_tracking.py \
  --ndi-source "OBS (Output)" \    # NDI source name
  --osc-ip 192.168.1.100 \         # IP for OSC messages
  --osc-port 9000                  # OSC port
```

## 🔧 Technical Details

### Hand Tracking
- **MediaPipe Hands**: Detects 21 landmarks per hand
- **Consistent IDs**: Tracks hand positions between frames
- **Max Distance**: 0.3 normalized units for hand matching
- **Pinch Detection**: Thumb-index distance < 5% of frame diagonal

### NDI Video
- **Protocol**: Network Device Interface for low-latency video
- **Sources**: OBS, vMix, TouchDesigner, NDI Scan Converter
- **Fallback**: Automatic camera fallback if no NDI found
- **Format**: BGRX/BGRA with highest bandwidth

### OSC Communication
- **Protocol**: Open Sound Control over UDP
- **Default**: 127.0.0.1:8000 (localhost)
- **Network**: Can broadcast to any IP/port
- **Compatible**: TouchDesigner, Max/MSP, Processing, PureData

## 🛠️ Implementation Details

### Files Structure
- `ndi_hand_tracking.py` - Main application with consistent hand tracking
- `ndi_utils.py` - Shared NDI receiver utilities following cyndilib best practices
- `test_ndi_receiver.py` - Simple NDI connectivity test
- `test_validation.py` - Validates setup without dependencies
- `osc_demo.py` - Sends test OSC messages for receiver testing

### Key Improvements Made

#### 1. Consistent Hand IDs
**Problem**: MediaPipe can assign inconsistent hand IDs when hands disappear/reappear or cross over.

**Solution**: Track hand positions between frames and assign stable IDs based on spatial proximity.

```python
def assign_consistent_hand_ids(self, current_hands):
    # Match current hands to previous hands by position
    # Assign stable IDs based on closest matching positions
    # Handle new hands and disappeared hands gracefully
```

#### 2. Proper cyndilib Implementation
**Original Issues Fixed**:
- Incorrect Finder usage
- Missing receiver configuration
- Wrong frame capture method
- No connection handling

**Fixed Implementation**:
```python
# Proper cyndilib pattern
with ndi.Finder() as finder:
    finder.wait_for_sources(timeout=10)
    sources = list(finder)

# Proper receiver setup
receiver = ndi.Receiver(
    color_format=RecvColorFormat.BGRX_BGRA,
    bandwidth=RecvBandwidth.highest
)
```

#### 3. Robust Error Handling
- NDI connection timeout handling
- Camera fallback system
- Graceful degradation
- Resource cleanup

## 🎨 Creative Applications

### Interactive Installations
- Map hand position to particle systems
- Control lighting with pinch gestures
- Create responsive environments

### VJ Performance
- Hand-controlled video effects
- Real-time visual manipulation
- Gesture-based scene switching

### Music Control
- Map pinch to filter cutoff
- Use hand position for spatial audio
- Gesture-triggered samples

### Game Controls
- Alternative input method
- Accessibility-friendly interface
- Natural gesture recognition

## 🐛 Troubleshooting

### Common Issues

**"No NDI sources found"**
- Ensure NDI source is running (OBS with NDI plugin, etc.)
- Check network connectivity (same subnet)
- Wait 5-10 seconds after starting NDI source

**"Hand IDs jumping around"**
- ✅ Fixed with consistent hand tracking
- Hands now maintain stable IDs even when temporarily lost

**"No working camera found"**
- Run `cd ../week08 && python setup_camera.py`
- Close other apps using the camera
- Try different USB ports

**"OSC not working"**
- Verify receiving app is listening on correct port
- Test with `python osc_demo.py` first
- Check firewall settings

### Performance Tips
- Reduce NDI source resolution
- Lower MediaPipe model complexity
- Close resource-heavy applications

## 📚 Educational Value

This project demonstrates:

1. **Network Protocols**: NDI for video, OSC for control data
2. **Computer Vision**: Real-time hand detection and tracking
3. **Gesture Recognition**: Converting motion to meaningful data
4. **Creative Coding**: Integration with artistic tools
5. **Real-time Systems**: Balancing accuracy with performance

## 🏗️ Architecture

```
NDI Source → NDI Receiver → MediaPipe → Hand Tracking → OSC Broadcast
    ↓              ↓           ↓            ↓             ↓
  OBS/vMix    cyndilib    AI Model    Gesture Calc   TouchDesigner
```

## 📄 Dependencies

- `cyndilib` - NDI video streaming
- `opencv-python` - Computer vision and display  
- `mediapipe` - Hand tracking AI model
- `python-osc` - OSC communication protocol
- `numpy` - Numerical operations

## 🎓 Credits

- **MediaPipe**: Google's ML framework for hand detection
- **cyndilib**: Python NDI SDK wrapper
- **NDI**: NewTek's Network Device Interface
- **OSC**: Open Sound Control protocol

## 📜 License

Educational example for PFAD (Programming for Art and Design) course.

---

## 🔗 Related Examples

- `blender/` - Blender integration scripts
- `orange/` - Orange Data Mining workflows  
- `touchdesigner/` - TouchDesigner Python examples
