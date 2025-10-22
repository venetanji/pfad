#!/usr/bin/env python3
"""
Hand tracking using MediaPipe
Detects and tracks hand landmarks in real-time
"""

import cv2
import mediapipe as mp
import numpy as np
from camera_utils import setup_camera

def main():
    print("🖐️ MediaPipe Hand Tracking")
    print("=" * 40)
    
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    try:
        # Setup camera using configuration
        cap, camera_id = setup_camera()
        print("✅ Camera initialized successfully")
        
    except RuntimeError as e:
        print(f"❌ Camera Error: {e}")
        print("💡 Run 'python setup_camera.py' to configure your camera")
        return
    
    print("🚀 Hand Tracking started. Press 'q' to quit.")
    
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Flip frame horizontally for selfie view
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = hands.process(rgb_frame)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks and connections
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    # Get landmark positions
                    landmarks = []
                    for landmark in hand_landmarks.landmark:
                        h, w, _ = frame.shape
                        x, y = int(landmark.x * w), int(landmark.y * h)
                        landmarks.append([x, y])
                    
                    # Draw fingertips
                    fingertip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
                    for tip_id in fingertip_ids:
                        if tip_id < len(landmarks):
                            cv2.circle(frame, tuple(landmarks[tip_id]), 10, (255, 0, 0), -1)
            
            # Add status overlay
            hand_count = len(results.multi_hand_landmarks) if results.multi_hand_landmarks else 0
            cv2.putText(frame, f'Camera {camera_id} | Hands: {hand_count}', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Show your hands to the camera", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, "Blue dots mark fingertips", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow('MediaPipe Hand Tracking', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Hand tracking stopped")

if __name__ == "__main__":
    main()