#!/usr/bin/env python3
"""
Basic face detection using MediaPipe
Detects faces in webcam feed and draws bounding boxes
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import sys
from camera_utils import setup_camera

def main():
    # Set environment variable to help with Windows MediaPipe issues
    os.environ['MEDIAPIPE_DISABLE_GPU'] = '1'
    
    print("🎥 MediaPipe Face Detection")
    print("=" * 40)
    
    try:
        # Initialize MediaPipe Face Detection
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        
        print("✅ MediaPipe modules loaded successfully")
        
    except Exception as e:
        print(f"❌ Error loading MediaPipe: {e}")
        print("💡 Try running: python setup_camera.py")
        print("💡 Or reinstall with: pip install -r requirements.txt")
        return
    
    try:
        # Setup camera using configuration
        cap, camera_id = setup_camera()
        print("✅ Camera initialized successfully")
        
    except RuntimeError as e:
        print(f"❌ Camera Error: {e}")
        print("💡 Run 'python setup_camera.py' to configure your camera")
        return
    
    print("🚀 Face Detection started. Press 'q' to quit.")
    
    try:
        with mp_face_detection.FaceDetection(
            model_selection=0,  # 0 for short-range (2 meters), 1 for full-range (5 meters)
            min_detection_confidence=0.5
        ) as face_detection:
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Error: Could not read frame")
                    break
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process the frame
                results = face_detection.process(rgb_frame)
                
                # Draw face detections
                face_count = 0
                if results.detections:
                    for detection in results.detections:
                        face_count += 1
                        # Get bounding box
                        bbox = detection.location_data.relative_bounding_box
                        h, w, _ = frame.shape
                        
                        # Convert relative coordinates to absolute
                        x = int(bbox.xmin * w)
                        y = int(bbox.ymin * h)
                        width = int(bbox.width * w)
                        height = int(bbox.height * h)
                        
                        # Draw bounding box
                        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                        
                        # Draw confidence score
                        confidence = detection.score[0]
                        cv2.putText(frame, f'Face: {confidence:.2f}', 
                                   (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Add status overlay
                cv2.putText(frame, f'Camera {camera_id} | Faces: {face_count}', 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, "Press 'q' to quit", 
                           (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Display frame
                cv2.imshow('MediaPipe Face Detection', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
    except Exception as e:
        print(f"❌ Error during face detection: {e}")
        print("💡 Troubleshooting tips:")
        print("1. Run 'python setup_camera.py' to reconfigure camera")
        print("2. Check if camera is being used by another application")
        print("3. Try: pip install -r requirements.txt")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("👋 Face detection stopped")

if __name__ == "__main__":
    main()