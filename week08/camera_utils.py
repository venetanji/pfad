#!/usr/bin/env python3
"""
Camera configuration utilities
Handles loading camera device from .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import cv2

def load_camera_config():
    """Load camera device ID from .env file"""
    # Load .env file from the same directory as this script
    env_file = Path(__file__).parent / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
        
        camera_device = os.getenv('CAMERA_DEVICE')
        if camera_device is not None:
            try:
                return int(camera_device)
            except ValueError:
                print(f"⚠️  Invalid CAMERA_DEVICE value in .env: {camera_device}")
                return None
    
    return None

def get_camera_device():
    """Get camera device ID with fallback logic"""
    # Try to load from .env file
    camera_id = load_camera_config()
    
    if camera_id is not None:
        # Test if the configured camera still works
        if test_camera_quick(camera_id):
            return camera_id
        else:
            print(f"⚠️  Configured camera {camera_id} is not available")
    
    # Fallback: auto-detect first available camera
    print("🔍 Auto-detecting available camera...")
    for i in range(10):
        if test_camera_quick(i):
            print(f"📷 Using camera device {i}")
            return i
    
    print("❌ No working camera found!")
    return None

def test_camera_quick(device_id):
    """Quick test if camera device works"""
    try:
        cap = cv2.VideoCapture(device_id)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret and frame is not None
        return False
    except:
        return False

def init_camera(camera_id=None):
    """Initialize camera with proper error handling"""
    if camera_id is None:
        camera_id = get_camera_device()
    
    if camera_id is None:
        raise RuntimeError("No working camera found. Run 'python setup_camera.py' to configure camera.")
    
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open camera {camera_id}. Run 'python setup_camera.py' to reconfigure.")
    
    print(f"📷 Using camera device {camera_id}")
    return cap, camera_id

# Convenience function for scripts
def setup_camera():
    """Setup camera and return capture object and device ID"""
    return init_camera()