#!/usr/bin/env python3
"""
Hand Position Smoothing Demo
===========================

This script demonstrates the difference between raw hand tracking positions
and smoothed positions using rolling average and exponential smoothing.

Usage:
- Run with different smoothing parameters to see the effect
- Shows both raw and smoothed positions overlaid
"""

import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque

class PositionSmoother:
    def __init__(self, window_size=5, smoothing_factor=0.7):
        self.window_size = window_size
        self.smoothing_factor = smoothing_factor
        self.position_history = deque(maxlen=window_size)
        self.last_smoothed = None
    
    def smooth(self, position):
        """Apply smoothing to position"""
        self.position_history.append(position)
        
        # Rolling average
        if len(self.position_history) > 1:
            avg_x = sum(pos[0] for pos in self.position_history) / len(self.position_history)
            avg_y = sum(pos[1] for pos in self.position_history) / len(self.position_history)
            
            # Exponential smoothing
            if self.last_smoothed is not None:
                smoothed_x = self.smoothing_factor * avg_x + (1 - self.smoothing_factor) * self.last_smoothed[0]
                smoothed_y = self.smoothing_factor * avg_y + (1 - self.smoothing_factor) * self.last_smoothed[1]
            else:
                smoothed_x, smoothed_y = avg_x, avg_y
            
            self.last_smoothed = (smoothed_x, smoothed_y)
            return (smoothed_x, smoothed_y)
        else:
            self.last_smoothed = position
            return position

def demo_smoothing():
    """Demonstrate position smoothing"""
    
    print("🎯 Hand Position Smoothing Demo")
    print("===============================")
    print("📹 This demo shows raw vs smoothed hand positions")
    print("🔴 Red dot: Raw position (jittery)")
    print("🟢 Green dot: Smoothed position (stable)")
    print("Press 'q' to quit\n")
    
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
        max_num_hands=1
    )
    
    # Initialize position smoother
    smoother = PositionSmoother(window_size=5, smoothing_factor=0.7)
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ No camera available")
        return
    
    print("🚀 Demo started! Move your hand to see smoothing effect")
    
    # Store position trails for visualization
    raw_trail = deque(maxlen=20)
    smooth_trail = deque(maxlen=20)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        # Process detected hands
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Calculate hand center (raw position)
                landmarks = hand_landmarks.landmark
                center_x = sum(lm.x for lm in landmarks) / len(landmarks)
                center_y = sum(lm.y for lm in landmarks) / len(landmarks)
                
                # Convert to pixel coordinates
                raw_pos = (int(center_x * width), int(center_y * height))
                
                # Apply smoothing
                smooth_pos = smoother.smooth((center_x, center_y))
                smooth_pixel = (int(smooth_pos[0] * width), int(smooth_pos[1] * height))
                
                # Add to trails
                raw_trail.append(raw_pos)
                smooth_trail.append(smooth_pixel)
                
                # Draw trails
                for i, pos in enumerate(raw_trail):
                    alpha = i / len(raw_trail)
                    cv2.circle(frame, pos, 2, (0, 0, int(255 * alpha)), -1)
                
                for i, pos in enumerate(smooth_trail):
                    alpha = i / len(smooth_trail)
                    cv2.circle(frame, pos, 2, (0, int(255 * alpha), 0), -1)
                
                # Draw current positions
                cv2.circle(frame, raw_pos, 8, (0, 0, 255), -1)  # Red for raw
                cv2.circle(frame, smooth_pixel, 8, (0, 255, 0), -1)  # Green for smoothed
                
                # Draw connection line
                cv2.line(frame, raw_pos, smooth_pixel, (255, 255, 255), 1)
                
                # Show position values
                cv2.putText(frame, f"Raw: ({center_x:.3f}, {center_y:.3f})", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.putText(frame, f"Smooth: ({smooth_pos[0]:.3f}, {smooth_pos[1]:.3f})", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Show legend
        cv2.putText(frame, "Red: Raw | Green: Smoothed", 
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Position Smoothing Demo', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print("👋 Demo finished!")

if __name__ == "__main__":
    demo_smoothing()