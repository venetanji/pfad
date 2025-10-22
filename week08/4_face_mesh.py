#!/usr/bin/env python3
"""
Face mesh detection using MediaPipe
Detects and draws detailed face landmarks and mesh
"""

import cv2
import mediapipe as mp
import numpy as np
from camera_utils import setup_camera

def main():
    print("🎭 MediaPipe Face Mesh Detection")
    print("=" * 40)
    
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
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
    
    print("🚀 Face Mesh Detection started.")
    print("Press 'c' to toggle contours only, 'f' for full mesh, 'i' for irises, 'q' to quit.")
    
    # Drawing modes
    drawing_mode = 'contours'  # 'contours', 'full', 'irises'
    
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,  # Enables iris landmarks
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read frame")
                break
            
            # Flip frame horizontally for selfie view
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = face_mesh.process(rgb_frame)
            
            # Draw face mesh
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    if drawing_mode == 'contours':
                        # Draw face contours only
                        mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                        )
                    elif drawing_mode == 'full':
                        # Draw full face mesh
                        mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                        )
                        # Also draw contours on top
                        mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                        )
                    elif drawing_mode == 'irises':
                        # Draw irises
                        mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            mp_face_mesh.FACEMESH_IRISES,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style()
                        )
                        # Also draw contours
                        mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                        )
                
                # Count landmarks
                landmark_count = len(results.multi_face_landmarks[0].landmark)
                cv2.putText(frame, f"Landmarks: {landmark_count}", 
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Display status and controls
            face_count = len(results.multi_face_landmarks) if results.multi_face_landmarks else 0
            cv2.putText(frame, f"Camera {camera_id} | Face Mesh ({drawing_mode.title()})", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Faces: {face_count}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Controls
            controls = [
                "Controls:",
                "'c' - Contours only",
                "'f' - Full mesh",
                "'i' - Irises + contours",
                "'q' - Quit"
            ]
            
            for i, control in enumerate(controls):
                y_pos = frame.shape[0] - 120 + i * 20
                color = (255, 255, 255) if i == 0 else (200, 200, 200)
                font_size = 0.6 if i == 0 else 0.5
                cv2.putText(frame, control, 
                           (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, font_size, color, 1)
            
            # Display frame
            cv2.imshow('MediaPipe Face Mesh Detection', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                drawing_mode = 'contours'
                print("Switched to contours mode")
            elif key == ord('f'):
                drawing_mode = 'full'
                print("Switched to full mesh mode")
            elif key == ord('i'):
                drawing_mode = 'irises'
                print("Switched to irises mode")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Face mesh detection stopped")

if __name__ == "__main__":
    main()