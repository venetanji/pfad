#!/usr/bin/env python3
"""
Pose estimation using MediaPipe
Detects and tracks human pose landmarks in real-time
"""

import cv2
import mediapipe as mp
import numpy as np
from camera_utils import setup_camera

def calculate_angle(a, b, c):
    """Calculate angle between three points"""
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

def main():
    print("🧍 MediaPipe Pose Estimation")
    print("=" * 40)
    
    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
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
    
    print("🚀 Pose Estimation started. Press 'q' to quit.")
    
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        
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
            results = pose.process(rgb_frame)
            
            # Draw pose landmarks
            if results.pose_landmarks:
                # Draw landmarks and connections
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                )
                
                # Extract landmarks
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates for angle calculation
                try:
                    # Left arm angle (shoulder-elbow-wrist)
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    
                    # Calculate angle
                    angle = calculate_angle(shoulder, elbow, wrist)
                    
                    # Convert to pixel coordinates for display
                    h, w, _ = frame.shape
                    elbow_pixel = (int(elbow[0] * w), int(elbow[1] * h))
                    
                    # Display angle
                    cv2.putText(frame, f'Left Arm: {int(angle)}°', 
                               (elbow_pixel[0] - 50, elbow_pixel[1] - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                    
                except:
                    pass
                
                # Detect if person is raising both hands
                try:
                    left_wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
                    right_wrist_y = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
                    nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y
                    
                    if left_wrist_y < nose_y and right_wrist_y < nose_y:
                        cv2.putText(frame, "HANDS UP!", (50, 100), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                except:
                    pass
            
            # Add status overlay
            cv2.putText(frame, f'Camera {camera_id} | Pose Detection', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Stand in front of camera for pose detection", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow('MediaPipe Pose Estimation', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Pose estimation stopped")

if __name__ == "__main__":
    main()