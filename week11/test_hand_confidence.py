#!/usr/bin/env python3
"""
Test Hand Tracking Confidence
============================

Simple test to validate hand tracking confidence settings work properly.
This script shows:
- Detection confidence threshold
- How many hands are detected
- Hand ID assignment logic
"""

import cv2
import mediapipe as mp
import time

def test_hand_confidence():
    """Test different confidence levels"""
    
    # Test different confidence levels
    confidence_levels = [0.5, 0.7, 0.9]
    
    for confidence in confidence_levels:
        print(f"\n🧪 Testing with confidence: {confidence}")
        
        # Initialize MediaPipe hands with current confidence
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=confidence,
            min_tracking_confidence=confidence,
            max_num_hands=2
        )
        
        # Try to use camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ No camera available")
            continue
            
        print("📹 Testing for 5 seconds... wave your hand(s)")
        
        start_time = time.time()
        hand_counts = []
        
        while time.time() - start_time < 5:
            ret, frame = cap.read()
            if not ret:
                continue
                
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            
            # Count detected hands
            num_hands = len(results.multi_hand_landmarks) if results.multi_hand_landmarks else 0
            hand_counts.append(num_hands)
            
            # Show frame with detection count
            cv2.putText(frame, f"Confidence: {confidence}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Hands: {num_hands}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow('Hand Confidence Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        hands.close()
        
        # Analyze results
        if hand_counts:
            avg_hands = sum(hand_counts) / len(hand_counts)
            max_hands = max(hand_counts)
            false_detections = sum(1 for count in hand_counts if count > 1)  # Assuming single hand test
            
            print(f"📊 Results for confidence {confidence}:")
            print(f"   Average hands detected: {avg_hands:.2f}")
            print(f"   Maximum hands detected: {max_hands}")
            print(f"   Frames with >1 hand: {false_detections}/{len(hand_counts)} ({false_detections/len(hand_counts)*100:.1f}%)")
    
    cv2.destroyAllWindows()
    print("\n✅ Confidence test complete!")
    print("💡 Higher confidence = fewer false detections but may miss real hands")

if __name__ == "__main__":
    test_hand_confidence()