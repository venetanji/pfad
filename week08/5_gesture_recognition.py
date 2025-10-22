#!/usr/bin/env python3
"""
Gesture recognition using MediaPipe hand tracking
Recognizes basic hand gestures like thumbs up, peace sign, etc.
"""

import cv2
import mediapipe as mp
import numpy as np
from camera_utils import setup_camera

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
    
    def get_finger_states(self, landmarks):
        """Determine if fingers are up or down"""
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [3, 6, 10, 14, 18]  # PIP joints
        
        fingers_up = []
        
        # Thumb (special case - check x coordinate)
        if landmarks[finger_tips[0]].x > landmarks[finger_pips[0]].x:
            fingers_up.append(1)
        else:
            fingers_up.append(0)
        
        # Other fingers (check y coordinate)
        for i in range(1, 5):
            if landmarks[finger_tips[i]].y < landmarks[finger_pips[i]].y:
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        return fingers_up
    
    def recognize_gesture(self, landmarks):
        """Recognize gestures based on finger states"""
        fingers_up = self.get_finger_states(landmarks)
        total_fingers = sum(fingers_up)
        
        # Thumbs up
        if fingers_up == [1, 0, 0, 0, 0]:
            return "👍 Thumbs Up"
        
        # Thumbs down
        elif fingers_up == [0, 0, 0, 0, 0] and landmarks[4].y > landmarks[3].y:
            return "👎 Thumbs Down"
        
        # Peace sign
        elif fingers_up == [0, 1, 1, 0, 0]:
            return "✌️ Peace"
        
        # Rock and roll
        elif fingers_up == [0, 1, 0, 0, 1]:
            return "🤟 Rock On"
        
        # Open hand
        elif total_fingers == 5:
            return "🖐️ Open Hand"
        
        # Fist
        elif total_fingers == 0:
            return "✊ Fist"
        
        # Pointing
        elif fingers_up == [0, 1, 0, 0, 0]:
            return "👉 Pointing"
        
        # OK sign (approximate)
        elif fingers_up == [1, 0, 1, 1, 1]:
            return "👌 OK"
        
        # Number counting
        elif total_fingers == 1:
            return "1️⃣ One"
        elif total_fingers == 2:
            return "2️⃣ Two"
        elif total_fingers == 3:
            return "3️⃣ Three"
        elif total_fingers == 4:
            return "4️⃣ Four"
        
        return f"🤔 Unknown ({total_fingers} fingers)"

def main():
    print("👋 MediaPipe Gesture Recognition")
    print("=" * 40)
    
    recognizer = GestureRecognizer()
    
    try:
        # Setup camera using configuration
        cap, camera_id = setup_camera()
        print("✅ Camera initialized successfully")
        
    except RuntimeError as e:
        print(f"❌ Camera Error: {e}")
        print("💡 Run 'python setup_camera.py' to configure your camera")
        return
    
    print("🚀 Gesture Recognition started. Press 'q' to quit.")
    
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
        results = recognizer.hands.process(rgb_frame)
        
        gestures = []
        
        # Process each detected hand
        if results.multi_hand_landmarks:
            for i, (hand_landmarks, handedness) in enumerate(
                zip(results.multi_hand_landmarks, results.multi_handedness)
            ):
                # Draw landmarks
                recognizer.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, recognizer.mp_hands.HAND_CONNECTIONS
                )
                
                # Recognize gesture
                gesture = recognizer.recognize_gesture(hand_landmarks.landmark)
                hand_type = handedness.classification[0].label
                
                gestures.append(f"{hand_type}: {gesture}")
                
                # Draw gesture text near hand
                h, w, _ = frame.shape
                x = int(hand_landmarks.landmark[0].x * w)
                y = int(hand_landmarks.landmark[0].y * h)
                
                cv2.putText(frame, f"{hand_type}: {gesture}", 
                           (x - 100, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                           (255, 255, 0), 2)
        
        # Display status overlay
        cv2.putText(frame, f"Camera {camera_id} | Gesture Recognition", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display recognized gestures
        y_offset = 60
        for gesture in gestures:
            cv2.putText(frame, gesture, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            y_offset += 30
        
        # Display supported gestures
        supported_gestures = [
            "Supported: Thumbs up/down, Peace, Rock on,",
            "Open hand, Fist, Pointing, OK, Numbers 1-5"
        ]
        
        for i, text in enumerate(supported_gestures):
            cv2.putText(frame, text, (10, frame.shape[0] - 50 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Add quit instruction
        cv2.putText(frame, "Press 'q' to quit", 
                   (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display frame
        cv2.imshow('MediaPipe Gesture Recognition', frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Gesture recognition stopped")

if __name__ == "__main__":
    main()