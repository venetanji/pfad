#!/usr/bin/env python3
"""
Multi-detection application combining multiple MediaPipe models
Demonstrates face mesh, hands, pose, and segmentation simultaneously
"""

import cv2
import mediapipe as mp
import numpy as np
from camera_utils import setup_camera

class MultiDetector:
    def __init__(self):
        # Initialize MediaPipe solutions
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize models
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(
            model_selection=0
        )
        
        # Detection flags
        self.show_face = True
        self.show_hands = True
        self.show_pose = True
        self.show_segmentation = False
        
    def process_frame(self, frame):
        """Process frame with all detectors"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = {}
        
        # Face mesh detection
        if self.show_face:
            results['face'] = self.face_mesh.process(rgb_frame)
        
        # Hand detection
        if self.show_hands:
            results['hands'] = self.hands.process(rgb_frame)
        
        # Pose detection
        if self.show_pose:
            results['pose'] = self.pose.process(rgb_frame)
        
        # Segmentation
        if self.show_segmentation:
            results['segmentation'] = self.selfie_segmentation.process(rgb_frame)
        
        return results
    
    def draw_detections(self, frame, results):
        """Draw all detection results on frame"""
        output_frame = frame.copy()
        
        # Apply segmentation background if enabled
        if self.show_segmentation and 'segmentation' in results:
            # Create a colored background
            bg_color = (50, 50, 150)  # Dark red background
            background = np.full_like(frame, bg_color, dtype=np.uint8)
            
            # Create mask
            condition = np.stack((results['segmentation'].segmentation_mask,) * 3, axis=-1) > 0.1
            output_frame = np.where(condition, frame, background)
        
        # Draw face mesh
        if self.show_face and 'face' in results and results['face'].multi_face_landmarks:
            for face_landmarks in results['face'].multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    output_frame,
                    face_landmarks,
                    self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style()
                )
        
        # Draw pose
        if self.show_pose and 'pose' in results and results['pose'].pose_landmarks:
            self.mp_drawing.draw_landmarks(
                output_frame,
                results['pose'].pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        # Draw hands
        if self.show_hands and 'hands' in results and results['hands'].multi_hand_landmarks:
            for hand_landmarks in results['hands'].multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    output_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        return output_frame
    
    def get_detection_stats(self, results):
        """Get statistics about current detections"""
        stats = {
            'faces': 0,
            'hands': 0,
            'pose': 0,
            'segmentation': 0
        }
        
        if 'face' in results and results['face'].multi_face_landmarks:
            stats['faces'] = len(results['face'].multi_face_landmarks)
        
        if 'hands' in results and results['hands'].multi_hand_landmarks:
            stats['hands'] = len(results['hands'].multi_hand_landmarks)
        
        if 'pose' in results and results['pose'].pose_landmarks:
            stats['pose'] = 1
        
        if 'segmentation' in results:
            stats['segmentation'] = np.mean(results['segmentation'].segmentation_mask)
        
        return stats

def main():
    print("🎯 MediaPipe Multi-Detection System")
    print("=" * 40)
    
    detector = MultiDetector()
    
    try:
        # Setup camera using configuration
        cap, camera_id = setup_camera()
        print("✅ Camera initialized successfully")
        
    except RuntimeError as e:
        print(f"❌ Camera Error: {e}")
        print("💡 Run 'python setup_camera.py' to configure your camera")
        return
    
    print("🚀 Multi-Detection started.")
    print("Controls: 'f'-face, 'h'-hands, 'p'-pose, 's'-segmentation, 'q'-quit")
    
    # FPS calculation
    import time
    prev_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Flip frame horizontally for selfie view
        frame = cv2.flip(frame, 1)
        
        # Process frame
        results = detector.process_frame(frame)
        
        # Draw detections
        output_frame = detector.draw_detections(frame, results)
        
        # Get detection statistics
        stats = detector.get_detection_stats(results)
        
        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        
        # Draw UI
        y_offset = 30
        
        # Title
        cv2.putText(output_frame, f"Camera {camera_id} | Multi-Detection System", 
                   (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_offset += 35
        
        # Active detections
        active_detections = []
        if detector.show_face:
            active_detections.append(f"Face({stats['faces']})")
        if detector.show_hands:
            active_detections.append(f"Hands({stats['hands']})")
        if detector.show_pose:
            active_detections.append(f"Pose({stats['pose']})")
        if detector.show_segmentation:
            active_detections.append(f"Seg({stats['segmentation']:.2f})")
        
        cv2.putText(output_frame, f"Active: {', '.join(active_detections)}", 
                   (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        y_offset += 30
        
        # FPS
        cv2.putText(output_frame, f"FPS: {fps:.1f}", 
                   (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        y_offset += 40
        
        # Controls
        controls = [
            "Controls:",
            "'f' - Toggle Face Mesh",
            "'h' - Toggle Hand Tracking",
            "'p' - Toggle Pose Detection",
            "'s' - Toggle Segmentation",
            "'q' - Quit"
        ]
        
        for i, control in enumerate(controls):
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            font_size = 0.6 if i == 0 else 0.5
            cv2.putText(output_frame, control, 
                       (10, y_offset + i * 25), cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 1)
        
        # Display frame
        cv2.imshow('MediaPipe Multi-Detection System', output_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('f'):
            detector.show_face = not detector.show_face
            print(f"Face mesh: {'ON' if detector.show_face else 'OFF'}")
        elif key == ord('h'):
            detector.show_hands = not detector.show_hands
            print(f"Hand tracking: {'ON' if detector.show_hands else 'OFF'}")
        elif key == ord('p'):
            detector.show_pose = not detector.show_pose
            print(f"Pose detection: {'ON' if detector.show_pose else 'OFF'}")
        elif key == ord('s'):
            detector.show_segmentation = not detector.show_segmentation
            print(f"Segmentation: {'ON' if detector.show_segmentation else 'OFF'}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Multi-detection stopped")

if __name__ == "__main__":
    main()