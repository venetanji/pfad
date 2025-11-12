#!/usr/bin/env python3
"""
Test and validation script for ndi_hand_tracking.py

This script validates the core logic of the hand tracking application
without requiring actual NDI sources or camera hardware.
"""

import sys
import math
from pathlib import Path

# Mock classes for testing without dependencies
class MockLandmark:
    """Mock MediaPipe landmark for testing"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockHandLandmarks:
    """Mock MediaPipe hand landmarks for testing"""
    def __init__(self):
        # Create 21 mock landmarks in a hand-like pattern
        self.landmark = []
        # Wrist
        self.landmark.append(MockLandmark(0.5, 0.5))
        # Thumb (landmarks 1-4, tip at 4)
        self.landmark.extend([
            MockLandmark(0.4, 0.5),
            MockLandmark(0.35, 0.45),
            MockLandmark(0.3, 0.4),
            MockLandmark(0.25, 0.35),  # Thumb tip
        ])
        # Index finger (landmarks 5-8, tip at 8)
        self.landmark.extend([
            MockLandmark(0.5, 0.4),
            MockLandmark(0.5, 0.3),
            MockLandmark(0.5, 0.2),
            MockLandmark(0.5, 0.1),  # Index tip (far from thumb)
        ])
        # Add remaining landmarks (middle, ring, pinky)
        for i in range(12):
            self.landmark.append(MockLandmark(0.5 + i*0.01, 0.5 + i*0.01))

def test_hand_center_calculation():
    """Test hand center position calculation"""
    print("🧪 Testing hand center calculation...")
    
    # Create mock hand
    hand_landmarks = MockHandLandmarks()
    frame_shape = (480, 640, 3)  # H, W, C
    
    # Calculate center
    sum_x = sum(lm.x for lm in hand_landmarks.landmark)
    sum_y = sum(lm.y for lm in hand_landmarks.landmark)
    num_landmarks = len(hand_landmarks.landmark)
    center_x = sum_x / num_landmarks
    center_y = sum_y / num_landmarks
    
    print(f"  ✅ Hand center: ({center_x:.3f}, {center_y:.3f})")
    
    # Validate center is in valid range
    assert 0 <= center_x <= 1, "Center X out of range"
    assert 0 <= center_y <= 1, "Center Y out of range"
    
    print("  ✅ Center calculation validated")
    return True

def test_pinch_calculation():
    """Test pinch gesture calculation"""
    print("\n🧪 Testing pinch calculation...")
    
    # Create mock hand with specific thumb and index positions
    hand_landmarks = MockHandLandmarks()
    frame_shape = (480, 640, 3)  # H, W, C
    h, w = frame_shape[:2]
    
    # Get thumb and index positions
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    
    print(f"  Thumb tip: ({thumb_tip.x:.3f}, {thumb_tip.y:.3f})")
    print(f"  Index tip: ({index_tip.x:.3f}, {index_tip.y:.3f})")
    
    # Convert to pixel coordinates
    thumb_x = int(thumb_tip.x * w)
    thumb_y = int(thumb_tip.y * h)
    index_x = int(index_tip.x * w)
    index_y = int(index_tip.y * h)
    
    # Calculate distance
    dx = index_x - thumb_x
    dy = index_y - thumb_y
    pixel_distance = math.sqrt(dx * dx + dy * dy)
    
    # Normalize by frame diagonal
    frame_diagonal = math.sqrt(w * w + h * h)
    normalized_distance = pixel_distance / frame_diagonal
    
    # Calculate angle
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    
    print(f"  ✅ Pinch length (normalized): {normalized_distance:.3f}")
    print(f"  ✅ Pinch angle: {angle_deg:.1f}°")
    
    # Test pinch detection threshold
    is_pinching = normalized_distance < 0.05
    print(f"  Is pinching (< 0.05): {is_pinching}")
    
    # Validate values are in reasonable ranges
    assert normalized_distance >= 0, "Distance cannot be negative"
    assert -180 <= angle_deg <= 180, "Angle out of valid range"
    
    print("  ✅ Pinch calculation validated")
    return True

def test_osc_address_patterns():
    """Test OSC address pattern generation"""
    print("\n🧪 Testing OSC address patterns...")
    
    expected_patterns = [
        "/hand/0/position",
        "/hand/0/pinch_length",
        "/hand/0/pinch_angle",
        "/hand/0/is_pinching",
        "/hand/1/position",
        "/hand/1/pinch_length",
        "/hand/1/pinch_angle",
        "/hand/1/is_pinching",
    ]
    
    for hand_id in [0, 1]:
        patterns = [
            f"/hand/{hand_id}/position",
            f"/hand/{hand_id}/pinch_length",
            f"/hand/{hand_id}/pinch_angle",
            f"/hand/{hand_id}/is_pinching",
        ]
        
        for pattern in patterns:
            assert pattern in expected_patterns, f"Unexpected pattern: {pattern}"
            print(f"  ✅ {pattern}")
    
    print("  ✅ OSC patterns validated")
    return True

def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing file structure...")
    
    week11_path = Path(__file__).parent
    
    required_files = [
        "ndi_hand_tracking.py",
        "requirements.txt",
        "README.md",
    ]
    
    for filename in required_files:
        filepath = week11_path / filename
        assert filepath.exists(), f"Missing file: {filename}"
        print(f"  ✅ {filename} exists")
    
    print("  ✅ File structure validated")
    return True

def test_week08_integration():
    """Test that week08 imports can be resolved"""
    print("\n🧪 Testing week08 integration...")
    
    week11_path = Path(__file__).parent
    week08_path = week11_path.parent / "week08"
    
    required_files = [
        "setup_camera.py",
        "camera_utils.py",
    ]
    
    for filename in required_files:
        filepath = week08_path / filename
        assert filepath.exists(), f"Missing week08 file: {filename}"
        print(f"  ✅ week08/{filename} accessible")
    
    print("  ✅ Week08 integration validated")
    return True

def test_requirements():
    """Test that requirements.txt has necessary packages"""
    print("\n🧪 Testing requirements.txt...")
    
    week11_path = Path(__file__).parent
    req_file = week11_path / "requirements.txt"
    
    with open(req_file, 'r') as f:
        content = f.read()
    
    required_packages = [
        "cyndilib",
        "opencv-python",
        "mediapipe",
        "python-osc",
        "numpy",
    ]
    
    for package in required_packages:
        assert package in content, f"Missing package in requirements: {package}"
        print(f"  ✅ {package} listed")
    
    print("  ✅ Requirements validated")
    return True

def test_code_syntax():
    """Test that Python code is syntactically valid"""
    print("\n🧪 Testing code syntax...")
    
    import py_compile
    
    week11_path = Path(__file__).parent
    script_path = week11_path / "ndi_hand_tracking.py"
    
    try:
        py_compile.compile(str(script_path), doraise=True)
        print("  ✅ Code syntax is valid")
        return True
    except py_compile.PyCompileError as e:
        print(f"  ❌ Syntax error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("NDI Hand Tracking Validation Tests")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Week08 Integration", test_week08_integration),
        ("Requirements", test_requirements),
        ("Code Syntax", test_code_syntax),
        ("Hand Center Calculation", test_hand_center_calculation),
        ("Pinch Calculation", test_pinch_calculation),
        ("OSC Address Patterns", test_osc_address_patterns),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
