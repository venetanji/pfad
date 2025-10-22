#!/usr/bin/env python3
"""
Selfie segmentation using MediaPipe
Segments person from background for virtual background effects
"""

import cv2
import mediapipe as mp
import numpy as np
from camera_utils import setup_camera

def create_background_effects():
    """Create different background effects"""
    backgrounds = {}
    
    # Solid color backgrounds
    backgrounds['blue'] = np.full((480, 640, 3), (255, 0, 0), dtype=np.uint8)
    backgrounds['green'] = np.full((480, 640, 3), (0, 255, 0), dtype=np.uint8)
    backgrounds['red'] = np.full((480, 640, 3), (0, 0, 255), dtype=np.uint8)
    
    # Gradient background
    gradient = np.zeros((480, 640, 3), dtype=np.uint8)
    for i in range(480):
        gradient[i, :] = [int(255 * i / 480), int(128 * (1 - i / 480)), 255 - int(255 * i / 480)]
    backgrounds['gradient'] = gradient
    
    # Pattern background
    pattern = np.zeros((480, 640, 3), dtype=np.uint8)
    for i in range(0, 480, 40):
        for j in range(0, 640, 40):
            color = (255, 255, 255) if (i // 40 + j // 40) % 2 == 0 else (0, 0, 0)
            pattern[i:i+40, j:j+40] = color
    backgrounds['checkerboard'] = pattern
    
    return backgrounds

def main():
    print("🤳 MediaPipe Selfie Segmentation")
    print("=" * 40)
    
    # Initialize MediaPipe Selfie Segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    
    try:
        # Setup camera using configuration
        cap, camera_id = setup_camera()
        print("✅ Camera initialized successfully")
        
    except RuntimeError as e:
        print(f"❌ Camera Error: {e}")
        print("💡 Run 'python setup_camera.py' to configure your camera")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("🚀 Selfie Segmentation started.")
    print("Press 'b' to cycle backgrounds, 'o' for original, 'q' to quit.")
    
    # Create background effects
    backgrounds = create_background_effects()
    background_names = list(backgrounds.keys())
    current_bg_idx = 0
    show_original = False
    
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Flip frame horizontally for selfie view
            frame = cv2.flip(frame, 1)
            
            # Resize frame to match background size
            frame = cv2.resize(frame, (640, 480))
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = selfie_segmentation.process(rgb_frame)
            
            if show_original:
                # Show original frame
                output_frame = frame.copy()
                cv2.putText(output_frame, f"Camera {camera_id} | Original", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            else:
                # Create segmentation mask
                condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
                
                # Get current background
                current_bg = backgrounds[background_names[current_bg_idx]]
                
                # Apply background replacement
                output_frame = np.where(condition, frame, current_bg)
                
                # Add text overlay
                bg_name = background_names[current_bg_idx].title()
                cv2.putText(output_frame, f"Camera {camera_id} | Background: {bg_name}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Show segmentation confidence
                avg_confidence = np.mean(results.segmentation_mask)
                cv2.putText(output_frame, f"Segmentation: {avg_confidence:.2f}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add instructions
            instructions = [
                "Controls:",
                "'b' - Change background",
                "'o' - Toggle original",
                "'q' - Quit"
            ]
            
            for i, instruction in enumerate(instructions):
                cv2.putText(output_frame, instruction, 
                           (10, 100 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display frame
            cv2.imshow('MediaPipe Selfie Segmentation', output_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('b') and not show_original:
                # Cycle through backgrounds
                current_bg_idx = (current_bg_idx + 1) % len(background_names)
                print(f"Switched to {background_names[current_bg_idx]} background")
            elif key == ord('o'):
                # Toggle original view
                show_original = not show_original
                print("Original view" if show_original else "Segmentation view")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Selfie segmentation stopped")

if __name__ == "__main__":
    main()