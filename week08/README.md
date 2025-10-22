# MediaPipe Examples - Week 08

This folder contains comprehensive examples of using Google's MediaPipe framework for computer vision and machine learning tasks.

## Overview

MediaPipe is a powerful framework for building multimodal applied ML pipelines. These examples demonstrate various computer vision capabilities including face detection, hand tracking, pose estimation, and more.

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

## Examples

### 1. Face Detection (`1_face_detection.py`)
- Basic face detection using MediaPipe
- Draws bounding boxes around detected faces
- Shows confidence scores
- Good starting point for understanding MediaPipe basics

**Key Features:**
- Real-time face detection
- Confidence scoring
- Bounding box visualization

### 2. Hand Tracking (`2_hand_tracking.py`)
- Detects and tracks hand landmarks
- Identifies fingertips with blue dots
- Works with both hands simultaneously
- 21 landmarks per hand

**Key Features:**
- 21-point hand landmark detection
- Fingertip identification
- Multi-hand support
- Real-time tracking

### 3. Pose Estimation (`3_pose_estimation.py`)
- Full body pose detection with 33 landmarks
- Calculates joint angles (demonstrated with left arm)
- Detects specific poses (hands up detection)
- Body keypoint connections

**Key Features:**
- 33-point pose landmarks
- Joint angle calculation
- Pose recognition
- Real-time body tracking

### 4. Face Mesh (`4_face_mesh.py`)
- Detailed face landmark detection with 468 points
- Multiple visualization modes: contours, full mesh, irises
- High-precision facial feature mapping
- Interactive mode switching

**Key Features:**
- 468 facial landmarks
- Face contours visualization
- Full face mesh tessellation
- Iris tracking (when enabled)
- Interactive controls to switch between modes

**Controls:**
- `c` - Contours only mode
- `f` - Full mesh mode  
- `i` - Irises + contours mode

### 5. Gesture Recognition (`5_gesture_recognition.py`)
- Recognizes common hand gestures
- Supports thumbs up/down, peace sign, rock on, numbers
- Real-time gesture classification
- Works with both hands

**Supported Gestures:**
- 👍 Thumbs Up
- 👎 Thumbs Down
- ✌️ Peace Sign
- 🤟 Rock On
- ✊ Fist
- 🖐️ Open Hand
- 👉 Pointing
- 👌 OK Sign
- Numbers 1-5

### 6. Holistic Detection (`6_holistic_detection.py`)
- Combines face mesh, pose, and hand detection
- Unified model for comprehensive body analysis
- Shows detection status for each component
- Counts total landmarks detected

**Key Features:**
- Face mesh (468 landmarks)
- Pose detection (33 landmarks)
- Hand detection (21 landmarks each)
- Integrated processing

### 7. Selfie Segmentation (`7_selfie_segmentation.py`)
- Person segmentation for virtual backgrounds
- Multiple background effects (solid colors, gradient, patterns)
- Real-time background replacement
- Adjustable segmentation threshold

**Background Effects:**
- Solid colors (blue, green, red)
- Gradient backgrounds
- Checkerboard pattern
- Original view toggle

### 8. Multi-Detection System (`8_multi_detection.py`)
- Combines multiple MediaPipe models
- Toggle individual detection modules
- Performance monitoring with FPS counter
- Comprehensive body analysis system

**Features:**
- Face mesh detection
- Hand tracking
- Pose estimation
- Background segmentation
- Real-time performance metrics
- Modular activation/deactivation

## 📷 Camera Setup

### First Time Setup
Before running any MediaPipe examples, configure your camera:

```bash
python setup_camera.py
```

This will:
1. 🔍 Detect all available cameras (tests devices 0-10)
2. 📋 Show you working cameras with their resolutions and FPS
3. 🎥 Let you test the selected camera with live preview
4. 💾 Save the working camera ID to `.env` file
5. ✅ All other scripts will automatically use the configured camera

### Camera Configuration Details

The setup script creates a `.env` file with your camera device ID:
```
CAMERA_DEVICE=4
```

All MediaPipe scripts automatically load this configuration using `camera_utils.py`.

### Manual Camera Override

If you need to use a different camera temporarily, you can:
1. Edit the `.env` file directly
2. Run `setup_camera.py` again to reconfigure
3. Delete `.env` file to force auto-detection

## Usage Tips

### Camera Best Practices
- 🚫 Close other camera applications (Zoom, Skype, etc.)
- 💡 Ensure good lighting for better detection accuracy
- 📏 Position yourself 1-2 meters from the camera for optimal results
- 🔄 If camera stops working, run `setup_camera.py` to reconfigure

### Performance Optimization
- Close other camera applications
- Reduce video resolution if experiencing lag
- Toggle off unused detection modules in multi-detection example


### Camera Issues
```python
# Check available cameras
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} is available")
        cap.release()
```

## Controls

### Common Controls (Most Examples)
- `q` - Quit application
- `ESC` - Alternative quit key

### Specific Controls
- **Face Mesh**: `c` - Contours, `f` - Full mesh, `i` - Irises
- **Selfie Segmentation**: `b` - Change background, `o` - Original view
- **Multi-Detection**: `f` - Face, `h` - Hands, `p` - Pose, `s` - Segmentation

## Applications

These examples can be used as building blocks for:

- **Fitness Applications**: Pose estimation for exercise tracking
- **Sign Language Recognition**: Hand gesture classification
- **Video Conferencing**: Background replacement and effects
- **Augmented Reality**: Face mesh and hand tracking for AR filters
- **Security Systems**: Face detection and recognition
- **Accessibility Tools**: Gesture-based control interfaces
- **Gaming**: Motion-based game controls
- **Medical Applications**: Posture analysis and rehabilitation
- **Beauty Applications**: Face mesh for makeup filters and facial analysis

## Performance Notes

- **Face Detection**: ~30-60 FPS on most modern computers
- **Hand Tracking**: ~20-40 FPS depending on number of hands
- **Pose Estimation**: ~15-30 FPS for full body tracking
- **Face Mesh**: ~20-40 FPS depending on visualization mode
- **Gesture Recognition**: ~25-40 FPS with hand tracking overhead
- **Holistic Model**: ~10-25 FPS (combines all features)
- **Selfie Segmentation**: ~20-35 FPS depending on background complexity
- **Multi-Detection**: Varies based on active modules

## Further Reading

- [MediaPipe Documentation](https://mediapipe.dev/)

## Advanced Usage

For production applications, consider:
- Model optimization for specific use cases
- Custom training for specialized gestures
- Integration with other ML frameworks
- Mobile deployment using MediaPipe mobile solutions
