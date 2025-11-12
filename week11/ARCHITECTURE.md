# NDI Hand Tracking - System Architecture

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        VIDEO SOURCE                              │
├─────────────────────────────────────────────────────────────────┤
│  NDI Source (OBS, vMix)   OR    USB/Built-in Camera            │
│         (cyndilib)                 (week08/camera_utils)         │
└───────────────────┬─────────────────────────────────────────────┘
                    │
                    │ Video Frames (BGR format)
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MEDIAPIPE HAND TRACKING                        │
├─────────────────────────────────────────────────────────────────┤
│  • Detects up to 2 hands                                        │
│  • Provides 21 landmarks per hand                               │
│  • Landmarks 4 (thumb) and 8 (index) used for pinch            │
└───────────────────┬─────────────────────────────────────────────┘
                    │
                    │ Hand Landmarks (x, y, z coordinates)
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GESTURE CALCULATION                           │
├─────────────────────────────────────────────────────────────────┤
│  For each hand:                                                 │
│  1. Calculate center position (average of all 21 landmarks)     │
│  2. Get thumb tip (landmark 4) and index tip (landmark 8)       │
│  3. Calculate distance → pinch_length (normalized 0-1)          │
│  4. Calculate angle → pinch_angle (-180° to 180°)               │
│  5. Detect pinch state (distance < 5% threshold)                │
└───────────────┬───────────────────────┬─────────────────────────┘
                │                       │
                │ Hand Data             │ Hand Data
                ▼                       ▼
┌───────────────────────────┐   ┌─────────────────────────────────┐
│     OSC BROADCASTING      │   │    OPENCV VISUALIZATION         │
├───────────────────────────┤   ├─────────────────────────────────┤
│ Send to other apps:       │   │ Display overlays:               │
│ /hand/[id]/position       │   │ • Hand skeleton (MediaPipe)     │
│ /hand/[id]/pinch_length   │   │ • Pinch segment line            │
│ /hand/[id]/pinch_angle    │   │ • Thumb/index circles           │
│ /hand/[id]/is_pinching    │   │ • Hand center dot               │
└───────────┬───────────────┘   │ • Metrics overlay               │
            │                   └─────────────────────────────────┘
            │ UDP Messages
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RECEIVING APPLICATIONS                          │
├─────────────────────────────────────────────────────────────────┤
│  TouchDesigner  •  Max/MSP  •  Processing  •  Custom Apps       │
└─────────────────────────────────────────────────────────────────┘
```

## Class Structure

```
HandData
├── hand_id (0 or 1)
├── center_x (0-1)
├── center_y (0-1)
├── pinch_length (0-1)
├── pinch_angle (-180 to 180)
├── is_pinching (boolean)
├── thumb_tip (x, y pixels)
└── index_tip (x, y pixels)

NDIHandTracker
├── __init__(ndi_source_name, osc_ip, osc_port)
├── setup_ndi_receiver() → connects to NDI source
├── setup_camera_fallback() → initializes USB camera
├── get_frame() → returns video frame
├── calculate_hand_center(landmarks) → (x, y)
├── calculate_pinch_data(landmarks) → {length, angle, positions}
├── process_hands(frame) → [HandData, ...]
├── send_osc_data(hands_data) → broadcasts via UDP
├── draw_overlays(frame, hands_data) → annotates video
├── run() → main loop
└── cleanup() → releases resources
```

## MediaPipe Hand Landmarks

```
Hand with 21 landmarks:

     8   12  16  20        (Finger tips)
     |   |   |   |
     7   11  15  19
     |   |   |   |
     6   10  14  18
     |   |   |   |
     5   9   13  17
      \  |   |   /
       \ |   |  /
        \|   | /
         2   3
          \ /
           1
           |
           0 (Wrist)

Thumb chain:  0 → 1 → 2 → 3 → 4 (tip)
Index chain:  0 → 5 → 6 → 7 → 8 (tip)
Middle chain: 0 → 9 → 10 → 11 → 12 (tip)
Ring chain:   0 → 13 → 14 → 15 → 16 (tip)
Pinky chain:  0 → 17 → 18 → 19 → 20 (tip)
```

## Pinch Calculation

```python
# 1. Get landmark positions
thumb_tip = landmarks[4]    # (x, y, z) normalized
index_tip = landmarks[8]    # (x, y, z) normalized

# 2. Convert to pixel coordinates
thumb_x = thumb_tip.x * frame_width
thumb_y = thumb_tip.y * frame_height
index_x = index_tip.x * frame_width
index_y = index_tip.y * frame_height

# 3. Calculate distance
dx = index_x - thumb_x
dy = index_y - thumb_y
pixel_distance = sqrt(dx² + dy²)

# 4. Normalize by frame diagonal (scale-invariant)
frame_diagonal = sqrt(width² + height²)
pinch_length = pixel_distance / frame_diagonal

# 5. Calculate angle
pinch_angle = atan2(dy, dx) * 180 / π

# 6. Detect pinch (threshold: 5% of diagonal)
is_pinching = (pinch_length < 0.05)
```

## OSC Message Format

```
Message Structure:
┌──────────────────────┬──────────────────┬─────────────┐
│   Address Pattern    │   Arguments      │    Range    │
├──────────────────────┼──────────────────┼─────────────┤
│ /hand/0/position     │ [float, float]   │ 0.0 to 1.0  │
│ /hand/0/pinch_length │ float            │ 0.0 to 1.0  │
│ /hand/0/pinch_angle  │ float            │ -180 to 180 │
│ /hand/0/is_pinching  │ float            │ 0.0 or 1.0  │
│ /hand/1/position     │ [float, float]   │ 0.0 to 1.0  │
│ /hand/1/pinch_length │ float            │ 0.0 to 1.0  │
│ /hand/1/pinch_angle  │ float            │ -180 to 180 │
│ /hand/1/is_pinching  │ float            │ 0.0 or 1.0  │
└──────────────────────┴──────────────────┴─────────────┘

Messages sent at video frame rate (~30 Hz)
Protocol: UDP (connectionless, low latency)
Default port: 8000
```

## Integration Patterns

### TouchDesigner
```
OSC In DAT (port 8000)
    ↓
Select DAT (filter /hand/0/position)
    ↓
Split DAT (separate x and y)
    ↓
CHOP Execute (trigger on change)
    ↓
Your creative network!
```

### Max/MSP
```
[udpreceive 8000]
    ↓
[route /hand/0 /hand/1]
    ↓
[route position pinch_length pinch_angle is_pinching]
    ↓
[unpack f f] for position
    ↓
Your patch!
```

### Processing
```java
import oscP5.*;

OscP5 oscP5;
float handX, handY;

void setup() {
  oscP5 = new OscP5(this, 8000);
}

void oscEvent(OscMessage msg) {
  if (msg.checkAddrPattern("/hand/0/position")) {
    handX = msg.get(0).floatValue();
    handY = msg.get(1).floatValue();
  }
}
```

## Performance Considerations

- **Frame Rate**: Typically 30 fps for camera, varies for NDI
- **Latency**: 
  - NDI: ~1 frame (33ms at 30fps)
  - MediaPipe: ~30-50ms processing
  - OSC: <1ms on local network
  - Total: ~65-85ms end-to-end
- **CPU Usage**: Moderate (MediaPipe is optimized)
- **Network**: NDI requires good bandwidth (100+ Mbps for HD)
- **GPU**: MediaPipe can use GPU if available

## Troubleshooting Flow

```
Start ndi_hand_tracking.py
    ↓
NDI sources found? ──No──→ Try camera fallback
    │                          ↓
   Yes                     Camera works? ──No──→ Run setup_camera.py
    │                          │
    │                         Yes
    ↓                          │
Hands detected? ←──────────────┘
    │
   Yes
    ↓
OSC messages sent? ──No──→ Check firewall
    │                      Check port not in use
   Yes
    ↓
Receiver getting data? ──No──→ Check IP address
    │                          Check port number
   Yes                         Use osc_demo.py to test
    ↓
Success! 🎉
```
