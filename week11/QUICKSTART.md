# NDI Hand Tracking - Quick Start Guide

## What This Does
Tracks your hands from an NDI video source and sends the data over OSC to other applications like TouchDesigner, Max/MSP, or Processing.

## Quick Start

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

## OSC Messages You'll Receive

Each hand sends these messages:

```
/hand/0/position [x, y]           # Where the hand is (0-1)
/hand/0/pinch_length [distance]   # How close thumb and index are
/hand/0/pinch_angle [angle]       # Rotation angle of the pinch
/hand/0/is_pinching [true/false]  # Is the hand pinching?
```

Second hand uses `/hand/1/...`

## Common Issues

**"No NDI sources found"**
- Make sure your NDI source (like OBS) is running
- Check you're on the same network
- Wait a few seconds after starting NDI source

**"No working camera found"**
- Run `cd ../week08 && python setup_camera.py`
- Make sure no other app is using your camera
- Try unplugging and reconnecting

**"Module not found"**
- Run `pip install -r requirements.txt`
- Make sure you're in the week11 directory

## What to Build With This

- **VJ Tool**: Control TouchDesigner visuals with hand gestures
- **Music Controller**: Map pinch to synthesizer parameters in Max
- **Interactive Art**: Create installations that respond to hand movements
- **Game Controller**: Alternative input for games
- **Accessibility Tool**: Hands-free interface control

## Next Steps

1. Open TouchDesigner and add an "OSC In DAT" set to port 8000
2. Watch the OSC messages come in
3. Map hand position to visual parameters
4. Map pinch gesture to effects or controls
5. Experiment and create!

## More Info

See README.md for detailed documentation, integration examples, and troubleshooting.
