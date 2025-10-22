#!/usr/bin/env python3
"""
Holistic model using MediaPipe
Combines face, hand, and pose detection in a single model
"""

import cv2
import mediapipe as mp
import numpy as np
from camera_utils import setup_camera

def main():
    print("🎭 MediaPipe Holistic Detection")
    print("=" * 40)
    
    # Initialize MediaPipe Holistic
    mp_holistic = mp.solutions.holistic
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
    
    print("🚀 Holistic Detection started. Press 'q' to quit.")
    
    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:
        
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
            results = holistic.process(rgb_frame)
            
            # Draw face landmarks
            if results.face_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.face_landmarks,
                    mp_holistic.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                )
                
                # Add face detection indicator
                cv2.putText(frame, "Face Detected", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw pose landmarks
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                )
                
                # Add pose detection indicator
                cv2.putText(frame, "Pose Detected", (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw left hand landmarks
            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.left_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Add left hand detection indicator
                cv2.putText(frame, "Left Hand Detected", (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Draw right hand landmarks
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.right_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Add right hand detection indicator
                cv2.putText(frame, "Right Hand Detected", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Count total landmarks detected
            total_landmarks = 0
            if results.face_landmarks:
                total_landmarks += len(results.face_landmarks.landmark)
            if results.pose_landmarks:
                total_landmarks += len(results.pose_landmarks.landmark)
            if results.left_hand_landmarks:
                total_landmarks += len(results.left_hand_landmarks.landmark)
            if results.right_hand_landmarks:
                total_landmarks += len(results.right_hand_landmarks.landmark)
            
            # Display landmark count
            cv2.putText(frame, f"Total Landmarks: {total_landmarks}", (10, 180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Add status overlay
            cv2.putText(frame, f"Camera {camera_id} | Holistic Detection", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow('MediaPipe Holistic Detection', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Holistic detection stopped")

if __name__ == "__main__":
    main()