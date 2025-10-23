#!/usr/bin/env python3
"""
Emotion recognition using MediaPipe face detection and EmotiEffLib
Combines face detection with real-time emotion analysis
"""

import cv2
import mediapipe as mp
import numpy as np
from camera_utils import setup_camera
import time

# EmotiEffLib imports
try:
    from emotiefflib.facial_analysis import EmotiEffLibRecognizer, get_model_list
    EMOTION_LIB_AVAILABLE = True
except ImportError:
    EMOTION_LIB_AVAILABLE = False
    print("⚠️  EmotiEffLib not installed. Install with: pip install emotiefflib")

def create_emotion_colors():
    """Create color mapping for different emotions"""
    return {
        'happy': (0, 255, 0),       # Green
        'sad': (255, 0, 0),         # Blue
        'angry': (0, 0, 255),       # Red
        'surprised': (0, 255, 255), # Yellow
        'fearful': (128, 0, 128),   # Purple
        'fear': (128, 0, 128),      # Purple (alternative name)
        'disgusted': (0, 128, 128), # Teal
        'disgust': (0, 128, 128),   # Teal (alternative name)
        'neutral': (128, 128, 128), # Gray (changed from white for visibility)
        'contempt': (255, 128, 0),  # Orange
        'joy': (0, 255, 0),         # Green (alternative for happy)
        'sadness': (255, 0, 0),     # Blue (alternative for sad)
        'anger': (0, 0, 255),       # Red (alternative for angry)
        'surprise': (0, 255, 255),  # Yellow (alternative for surprised)
    }

def main():
    print("😊 MediaPipe + EmotiEffLib Emotion Detection")
    print("=" * 50)
    
    if not EMOTION_LIB_AVAILABLE:
        print("❌ EmotiEffLib is required for this example.")
        print("📦 Install it with: pip install emotiefflib")
        print("📚 More info: https://github.com/sb-ai-lab/EmotiEffLib")
        return
    
    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    
    # Initialize EmotiEffLib
    try:
        print("🔄 Loading EmotiEffLib model (this may take a moment)...")
        device = "cpu"  # Use CPU for compatibility
        model_name = get_model_list()[0]  # Get first available model
        emotion_detector = EmotiEffLibRecognizer(engine="onnx", model_name=model_name, device=device)
        print(f"✅ EmotiEffLib model loaded successfully: {model_name}")
    except Exception as e:
        print(f"❌ Failed to load EmotiEffLib model: {e}")
        print("💡 Make sure you have internet connection for the first run")
        return
    
    try:
        # Setup camera using configuration
        cap, camera_id = setup_camera()
        print("✅ Camera initialized successfully")
        
    except RuntimeError as e:
        print(f"❌ Camera Error: {e}")
        print("💡 Run 'python setup_camera.py' to configure your camera")
        return
    
    print("🚀 Emotion Detection started. Press 'q' to quit.")
    
    # Emotion colors and statistics
    emotion_colors = create_emotion_colors()
    emotion_history = []
    max_history = 10  # Keep last 10 emotion detections
    
    # FPS calculation
    prev_time = time.time()
    frame_count = 0
    
    with mp_face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.5
    ) as face_detection:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read frame")
                break
            
            # Flip frame horizontally for selfie view
            frame = cv2.flip(frame, 1)
            frame_count += 1
            
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces with MediaPipe
            results = face_detection.process(rgb_frame)
            
            detected_emotions = []
            
            if results.detections:
                for detection in results.detections:
                    # Get bounding box
                    bbox = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    
                    # Convert relative coordinates to absolute
                    x = int(bbox.xmin * w)
                    y = int(bbox.ymin * h)
                    width = int(bbox.width * w)
                    height = int(bbox.height * h)
                    
                    # Ensure bounding box is within frame
                    x = max(0, x)
                    y = max(0, y)
                    width = min(width, w - x)
                    height = min(height, h - y)
                    
                    # Extract face region
                    face_roi = frame[y:y+height, x:x+width]
                    
                    if face_roi.size > 0:
                        try:
                            # Convert BGR to RGB for EmotiEffLib (it expects RGB)
                            face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
                            
                            # Analyze emotion using EmotiEffLib
                            emotion_result = emotion_detector.predict_emotions(face_rgb)
                            
                            # Handle EmotiEffLib result format
                            # emotion_result is a tuple: (emotions_list, logits_array)
                            if emotion_result is not None:
                                if isinstance(emotion_result, tuple) and len(emotion_result) >= 1:
                                    emotions_list = emotion_result[0]  # First element is the emotions
                                    if emotions_list and len(emotions_list) > 0:
                                        # Get the first detected emotion
                                        emotion_name = str(emotions_list[0])
                                        confidence = 0.85  # Default confidence
                                    else:
                                        emotion_name = "Unknown"
                                        confidence = 0.5
                                else:
                                    emotion_name = "Unknown" 
                                    confidence = 0.5
                                
                                detected_emotions.append({
                                    'emotion': emotion_name,
                                    'confidence': confidence,
                                    'bbox': (x, y, width, height)
                                })
                                
                                # Add to history
                                emotion_history.append(emotion_name)
                                if len(emotion_history) > max_history:
                                    emotion_history.pop(0)
                                
                                # Get color for emotion (try exact match first, then lowercase)
                                emotion_key = emotion_name.lower().strip()
                                color = emotion_colors.get(emotion_key, emotion_colors.get(emotion_name, (255, 255, 255)))
                                
                                # Debug: Print emotion name and color (remove this after testing)
                                print(f"🎨 Emotion: '{emotion_name}' -> Color: {color}")
                                
                                # Draw bounding box
                                cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
                                
                                # Draw emotion label
                                label = f"{emotion_name}: {confidence:.2f}"
                                cv2.putText(frame, label, 
                                           (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                        
                        except Exception as e:
                            print(f"⚠️  Emotion recognition error: {e}")
                            # Fall back to drawing basic face detection
                            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                            cv2.putText(frame, "Face (No Emotion)", 
                                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Calculate FPS
            curr_time = time.time()
            if frame_count % 30 == 0:  # Update FPS every 30 frames
                fps = 30 / (curr_time - prev_time) if frame_count > 30 else 0
                prev_time = curr_time
            else:
                fps = 0
            
            # Display status and statistics
            face_count = len(results.detections) if results.detections else 0
            emotion_count = len(detected_emotions)
            
            cv2.putText(frame, f"Camera {camera_id} | Faces: {face_count} | Emotions: {emotion_count}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            if fps > 0:
                cv2.putText(frame, f"FPS: {fps:.1f}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            # Display emotion history
            if emotion_history:
                most_common = max(set(emotion_history), key=emotion_history.count)
                cv2.putText(frame, f"Dominant: {most_common}", 
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            # Display legend
            legend_y_start = frame.shape[0] - 200
            cv2.putText(frame, "Emotion Colors:", 
                       (10, legend_y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            legend_emotions = ['happy', 'sad', 'angry', 'surprised', 'neutral']
            for i, emotion in enumerate(legend_emotions):
                color = emotion_colors[emotion]
                y_pos = legend_y_start + 20 + i * 20
                cv2.putText(frame, emotion.title(), 
                           (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            
            # Instructions
            cv2.putText(frame, "Press 'q' to quit", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow('MediaPipe + EmotiEff Emotion Detection', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Display final statistics
    if emotion_history:
        print("\n📊 Emotion Detection Summary:")
        unique_emotions = set(emotion_history)
        for emotion in unique_emotions:
            count = emotion_history.count(emotion)
            percentage = (count / len(emotion_history)) * 100
            print(f"  {emotion.title()}: {count} times ({percentage:.1f}%)")
    
    print("👋 Emotion detection stopped")

if __name__ == "__main__":
    main()