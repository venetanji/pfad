#!/usr/bin/env python3
"""
Camera Device Detection and Configuration
Tests available cameras and saves the working one to .env file
"""

import cv2
import os
from pathlib import Path

def test_camera_device(device_id, test_duration=2):
    """Test a specific camera device"""
    try:
        cap = cv2.VideoCapture(device_id)
        
        if not cap.isOpened():
            return False, "Failed to open camera"
        
        # Try to read a frame
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return False, "Failed to read frame"
        
        # Check frame properties
        height, width = frame.shape[:2]
        if height == 0 or width == 0:
            cap.release()
            return False, "Invalid frame dimensions"
        
        # Get camera properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        
        # Test multiple frames
        for _ in range(5):
            ret, frame = cap.read()
            if ret:
                frame_count += 1
        
        cap.release()
        
        success_rate = frame_count / 5
        info = {
            'width': width,
            'height': height,
            'fps': fps,
            'success_rate': success_rate
        }
        
        return success_rate > 0.5, info
        
    except Exception as e:
        return False, f"Exception: {str(e)}"

def detect_cameras():
    """Detect all available camera devices"""
    print("🎥 Detecting camera devices...")
    print("=" * 50)
    
    working_cameras = []
    
    # Test camera indices 0-10
    for device_id in range(11):
        print(f"Testing camera device {device_id}...", end=" ")
        
        is_working, info = test_camera_device(device_id)
        
        if is_working:
            print("✅ WORKING")
            working_cameras.append({
                'id': device_id,
                'info': info
            })
            print(f"   Resolution: {info['width']}x{info['height']}")
            print(f"   FPS: {info['fps']:.1f}")
            print(f"   Success Rate: {info['success_rate']:.1f}")
            print()
        else:
            print(f"❌ Failed - {info}")
    
    return working_cameras

def save_camera_config(camera_id):
    """Save camera configuration to .env file"""
    env_file = Path(__file__).parent / '.env'
    
    # Read existing .env file if it exists
    env_content = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.readlines()
    
    # Remove existing CAMERA_DEVICE lines
    env_content = [line for line in env_content if not line.startswith('CAMERA_DEVICE')]
    
    # Add new camera device
    env_content.append(f'CAMERA_DEVICE={camera_id}\n')
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.writelines(env_content)
    
    print(f"✅ Camera device {camera_id} saved to .env file")

def interactive_camera_selection(working_cameras):
    """Let user select camera if multiple are available"""
    if not working_cameras:
        print("❌ No working cameras found!")
        return None
    
    if len(working_cameras) == 1:
        camera_id = working_cameras[0]['id']
        print(f"🎯 Found 1 working camera: Device {camera_id}")
        return camera_id
    
    print(f"🎯 Found {len(working_cameras)} working cameras:")
    print()
    
    for i, camera in enumerate(working_cameras):
        info = camera['info']
        print(f"  {i + 1}. Camera {camera['id']}: {info['width']}x{info['height']}, FPS: {info['fps']:.1f}")
    
    while True:
        try:
            choice = input(f"\nSelect camera (1-{len(working_cameras)}) or press Enter for default: ").strip()
            
            if not choice:
                # Default to first camera
                return working_cameras[0]['id']
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(working_cameras):
                return working_cameras[choice_idx]['id']
            else:
                print(f"Please enter a number between 1 and {len(working_cameras)}")
        
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nCancelled")
            return None

def test_selected_camera(camera_id):
    """Test the selected camera with live preview"""
    print(f"\n🧪 Testing camera {camera_id} with live preview...")
    print("Press 'q' to confirm and save, or 'ESC' to cancel")
    
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"❌ Failed to open camera {camera_id}")
        return False
    
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame")
                break
            
            frame_count += 1
            
            # Add overlay text
            cv2.putText(frame, f"Camera Device: {camera_id}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Frame: {frame_count}", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to confirm, 'ESC' to cancel", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            cv2.imshow(f'Camera {camera_id} Test', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return True
            elif key == 27:  # ESC key
                cap.release()
                cv2.destroyAllWindows()
                return False
    
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    return False

def main():
    print("🎥 MediaPipe Camera Setup Utility")
    print("=" * 50)
    
    # Check if .env file exists and has camera config
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'CAMERA_DEVICE=' in content:
                print("📁 Existing .env file found with camera configuration")
                print("This will detect cameras and update the configuration.\n")
    
    # Detect available cameras
    working_cameras = detect_cameras()
    
    if not working_cameras:
        print("\n❌ No working cameras detected!")
        print("Please check:")
        print("- Camera is connected and not used by other applications")
        print("- Camera drivers are installed")
        print("- Try different USB ports")
        return
    
    # Let user select camera
    selected_camera = interactive_camera_selection(working_cameras)
    
    if selected_camera is None:
        print("No camera selected. Exiting...")
        return
    
    # Test selected camera with preview
    if test_selected_camera(selected_camera):
        # Save configuration
        save_camera_config(selected_camera)
        
        print("\n🎉 Camera setup completed!")
        print(f"📝 Camera device {selected_camera} saved to .env file")
        print("\nYou can now run any MediaPipe script and it will use the configured camera.")
        print("\nTo reconfigure, run this script again.")
    else:
        print("\n❌ Camera test cancelled or failed")
        print("Run this script again to try a different camera.")

if __name__ == "__main__":
    main()