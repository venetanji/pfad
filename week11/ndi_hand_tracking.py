#!/usr/bin/env python3
"""
NDI Hand Tracking with OSC Server
==================================

This application receives video frames from an NDI source, performs hand tracking
using MediaPipe, and broadcasts hand data via OSC (Open Sound Control).

Features:
- Receives NDI video stream using cyndilib
- Tracks hands using MediaPipe
- Calculates hand position (x/y center)
- Detects pinch gesture between thumb tip and index finger tip
- Calculates pinch length (normalized) and rotation angle
- Sends data via OSC for use in other applications (TouchDesigner, Max/MSP, etc.)
- Displays annotated video with hand tracking overlay

Educational Purpose:
This script demonstrates integration of multiple technologies commonly used
in interactive art and design projects.
"""

import cv2
import numpy as np
import mediapipe as mp
import math
import sys
from pathlib import Path

# Import shared NDI utilities
try:
    from ndi_utils import NDIReceiver
except ImportError:
    print("❌ Error: cyndilib or ndi_utils not available")
    print("Install cyndilib with: pip install cyndilib")
    sys.exit(1)

# Import python-osc for OSC server
try:
    from pythonosc import udp_client
    from pythonosc.osc_server import AsyncIOOSCUDPServer
    from pythonosc.dispatcher import Dispatcher
except ImportError:
    print("❌ Error: python-osc not installed")
    print("Install with: pip install python-osc")
    sys.exit(1)

# Import camera setup utilities from week08
# This allows fallback to regular camera if NDI is not available
week08_path = Path(__file__).parent.parent / "week08"
sys.path.insert(0, str(week08_path))

try:
    from camera_utils import setup_camera
    CAMERA_UTILS_AVAILABLE = True
except ImportError:
    CAMERA_UTILS_AVAILABLE = False
    print("⚠️  Warning: Could not import camera_utils from week08")


class HandData:
    """
    Data structure to hold hand tracking information
    
    This class stores all the calculated data for a single hand,
    making it easy to organize and transmit via OSC.
    """
    def __init__(self):
        self.hand_id = 0           # Hand identifier (0 for first hand, 1 for second)
        self.center_x = 0.0        # X position of hand center (normalized 0-1)
        self.center_y = 0.0        # Y position of hand center (normalized 0-1)
        self.pinch_length = 0.0    # Distance between thumb and index (normalized)
        self.pinch_angle = 0.0     # Rotation angle of pinch segment (degrees)
        self.is_pinching = False   # Boolean flag for pinch gesture
        self.thumb_tip = (0, 0)    # Thumb tip position in pixels
        self.index_tip = (0, 0)    # Index finger tip position in pixels


class NDIHandTracker:
    """
    Main application class that handles NDI reception, hand tracking, and OSC
    
    This class encapsulates all the functionality needed for:
    - NDI video reception
    - MediaPipe hand tracking
    - Hand gesture calculations
    - OSC communication
    - Video display with overlays
    """
    
    def __init__(self, ndi_source_name=None, osc_ip="127.0.0.1", osc_port=8000):
        """
        Initialize the NDI hand tracker
        
        Args:
            ndi_source_name: Name of NDI source to connect to (None = auto-detect)
            osc_ip: IP address for OSC client (default: localhost)
            osc_port: Port number for OSC messages (default: 8000)
        """
        print("🎬 NDI Hand Tracking with OSC")
        print("=" * 50)
        
        # Initialize MediaPipe Hands
        # MediaPipe is a machine learning framework for detecting hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Create hands detector with optimized settings
        # - model_complexity=1: Balance between speed and accuracy
        # - min_detection_confidence: Higher confidence to reduce false detections
        # - min_tracking_confidence: Higher confidence for stable tracking
        self.hands = self.mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.75,  # Higher confidence to reduce false positives
            min_tracking_confidence=0.75,   # Higher tracking confidence
            max_num_hands=2  # Track up to 2 hands
        )
        
        # Initialize OSC client for sending data
        # OSC is a protocol for networking sound synthesizers, computers, and multimedia devices
        self.osc_client = udp_client.SimpleUDPClient(osc_ip, osc_port)
        print(f"📡 OSC client initialized: {osc_ip}:{osc_port}")
        
        # NDI receiver setup
        self.ndi_source_name = ndi_source_name
        self.ndi_receiver = None
        self.use_ndi = True
        
        # Fallback camera setup
        self.camera_cap = None
        self.camera_id = None
        
        # Frame counter for display
        self.frame_count = 0
        
        # Simplified hand tracking - single hand is always ID 0
        
    def setup_ndi_receiver(self):
        """
        Initialize NDI receiver to capture video from NDI source
        
        NDI (Network Device Interface) allows video to be sent over a network.
        This is commonly used in professional video production and live streaming.
        
        This implementation uses the shared NDI utilities module.
        """
        try:
            # Create NDI receiver using the shared utilities
            self.ndi_receiver = NDIReceiver(source_name=self.ndi_source_name)
            
            # Connect to NDI source
            if not self.ndi_receiver.connect():
                print("❌ Failed to connect to NDI source")
                return False
            
            # Get source info for display
            source_info = self.ndi_receiver.get_source_info()
            print(f"✅ Connected to NDI source: {source_info['name']}")
            
            return True
            
        except Exception as e:
            print(f"❌ NDI setup failed: {e}")
            return False
    
    def setup_camera_fallback(self):
        """
        Setup regular camera as fallback if NDI is not available
        
        This uses the camera utilities from week08 to initialize a USB/built-in camera
        """
        if not CAMERA_UTILS_AVAILABLE:
            print("❌ Camera utilities not available")
            return False
        
        try:
            print("📷 Setting up camera fallback...")
            self.camera_cap, self.camera_id = setup_camera()
            print("✅ Camera initialized successfully")
            return True
        except RuntimeError as e:
            print(f"❌ Camera setup failed: {e}")
            return False
    
    def get_frame(self):
        """
        Get next video frame from NDI or camera
        
        Returns:
            numpy.ndarray: BGR image frame, or None if no frame available
        """
        if self.use_ndi and self.ndi_receiver:
            # Get frame from NDI using the shared utilities
            try:
                # Check if still connected
                if not self.ndi_receiver.is_connected():
                    print("⚠️  NDI source disconnected")
                    return None
                
                # Get frame using the shared NDI utilities
                frame = self.ndi_receiver.get_frame()
                return frame
                    
            except Exception as e:
                print(f"⚠️  NDI frame capture error: {e}")
                return None
        
        elif self.camera_cap:
            # Get frame from regular camera
            ret, frame = self.camera_cap.read()
            if ret:
                # Flip for selfie view (mirrors the image)
                frame = cv2.flip(frame, 1)
                return frame
        
        return None
    
    def calculate_hand_center(self, hand_landmarks, frame_shape):
        """
        Calculate the center position of the hand
        
        The center is computed as the average of all landmark positions.
        This gives us a single point representing the hand's location.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks object
            frame_shape: Shape of the video frame (height, width, channels)
            
        Returns:
            tuple: (center_x, center_y) normalized to 0-1 range
        """
        h, w = frame_shape[:2]
        
        # Sum all landmark positions
        sum_x = 0.0
        sum_y = 0.0
        
        for landmark in hand_landmarks.landmark:
            sum_x += landmark.x
            sum_y += landmark.y
        
        # Calculate average (center point)
        num_landmarks = len(hand_landmarks.landmark)
        center_x = sum_x / num_landmarks
        center_y = sum_y / num_landmarks
        
        return (center_x, center_y)
    

    
    def calculate_pinch_data(self, hand_landmarks, frame_shape):
        """
        Calculate pinch gesture data from thumb and index finger
        
        The pinch gesture is detected by analyzing the distance and angle
        between the thumb tip (landmark 4) and index finger tip (landmark 8).
        
        Args:
            hand_landmarks: MediaPipe hand landmarks object
            frame_shape: Shape of the video frame (height, width, channels)
            
        Returns:
            dict: Contains pinch_length, pinch_angle, thumb_tip, index_tip
        """
        h, w = frame_shape[:2]
        
        # MediaPipe hand landmark indices:
        # 4 = thumb tip
        # 8 = index finger tip
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        
        # Convert normalized coordinates to pixel coordinates
        thumb_x = int(thumb_tip.x * w)
        thumb_y = int(thumb_tip.y * h)
        index_x = int(index_tip.x * w)
        index_y = int(index_tip.y * h)
        
        # Calculate distance between thumb and index (in pixels)
        dx = index_x - thumb_x
        dy = index_y - thumb_y
        pixel_distance = math.sqrt(dx * dx + dy * dy)
        
        # Normalize distance relative to frame diagonal
        # This makes the measurement scale-invariant
        frame_diagonal = math.sqrt(w * w + h * h)
        normalized_distance = pixel_distance / frame_diagonal
        
        # Calculate angle of the segment (in degrees)
        # atan2 gives angle in radians, convert to degrees
        # 0° points right, 90° points down (image coordinates)
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        return {
            'pinch_length': normalized_distance,
            'pinch_angle': angle_deg,
            'thumb_tip': (thumb_x, thumb_y),
            'index_tip': (index_x, index_y)
        }
    
    def process_hands(self, frame):
        """
        Process frame to detect and track hands
        
        This is the main processing function that:
        1. Converts frame to RGB for MediaPipe
        2. Detects hands
        3. Calculates hand data
        4. Returns list of HandData objects
        
        Args:
            frame: BGR image from camera/NDI
            
        Returns:
            list: List of HandData objects for detected hands
        """
        # Convert BGR (OpenCV format) to RGB (MediaPipe format)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = self.hands.process(rgb_frame)
        
        hands_data = []
        
        # Check if hands were detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Create HandData object for this hand
                hand_data = HandData()
                
                # Calculate hand center position
                hand_data.center_x, hand_data.center_y = \
                    self.calculate_hand_center(hand_landmarks, frame.shape)
                
                # Calculate pinch gesture data
                pinch_data = self.calculate_pinch_data(hand_landmarks, frame.shape)
                hand_data.pinch_length = pinch_data['pinch_length']
                hand_data.pinch_angle = pinch_data['pinch_angle']
                hand_data.thumb_tip = pinch_data['thumb_tip']
                hand_data.index_tip = pinch_data['index_tip']
                
                # Detect if hand is pinching
                # Threshold: if distance is less than 5% of frame diagonal, consider it a pinch
                hand_data.is_pinching = hand_data.pinch_length < 0.05
                
                hands_data.append(hand_data)
        
        # Simple hand ID assignment: first hand is always 0, second is 1
        for i, hand_data in enumerate(hands_data):
            hand_data.hand_id = i
        
        return hands_data, results
    
    def send_osc_data(self, hands_data):
        """
        Send hand tracking data via OSC
        
        OSC (Open Sound Control) is a protocol for sending data over networks.
        It's commonly used in interactive installations, VJing, and music software.
        
        We send separate messages for each hand with the address pattern:
        /hand/[hand_id]/[parameter]
        
        Args:
            hands_data: List of HandData objects
        """
        for hand_data in hands_data:
            hand_id = hand_data.hand_id
            
            # Send position data
            # Address: /hand/0/position or /hand/1/position
            # Arguments: [x, y]
            self.osc_client.send_message(
                f"/hand/{hand_id}/position",
                [hand_data.center_x, hand_data.center_y]
            )
            
            # Send pinch length
            # This value represents how close thumb and index are
            self.osc_client.send_message(
                f"/hand/{hand_id}/pinch_length",
                hand_data.pinch_length
            )
            
            # Send pinch angle
            # This is the rotation angle of the pinch gesture
            self.osc_client.send_message(
                f"/hand/{hand_id}/pinch_angle",
                hand_data.pinch_angle
            )
            
            # Send pinch state (boolean)
            # 1.0 = pinching, 0.0 = not pinching
            self.osc_client.send_message(
                f"/hand/{hand_id}/is_pinching",
                1.0 if hand_data.is_pinching else 0.0
            )
    
    def draw_overlays(self, frame, hands_data, mp_results):
        """
        Draw hand tracking overlays on the frame
        
        This adds visual feedback showing:
        - MediaPipe hand skeleton
        - Pinch segment between thumb and index
        - Hand position indicator
        - Status information
        
        Args:
            frame: BGR image to draw on
            hands_data: List of HandData objects
            mp_results: MediaPipe detection results
        """
        # Draw MediaPipe hand landmarks and connections
        if mp_results.multi_hand_landmarks:
            for hand_landmarks in mp_results.multi_hand_landmarks:
                # Draw the full hand skeleton
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        # Draw custom overlays for each hand
        for hand_data in hands_data:
            # Draw pinch segment (line between thumb and index)
            # Color: Green if pinching, Blue if not
            pinch_color = (0, 255, 0) if hand_data.is_pinching else (255, 0, 0)
            thickness = 3 if hand_data.is_pinching else 2
            
            cv2.line(
                frame,
                hand_data.thumb_tip,
                hand_data.index_tip,
                pinch_color,
                thickness
            )
            
            # Draw circles at thumb and index tips
            cv2.circle(frame, hand_data.thumb_tip, 8, (0, 255, 255), -1)
            cv2.circle(frame, hand_data.index_tip, 8, (0, 255, 255), -1)
            
            # Draw hand center position
            h, w = frame.shape[:2]
            center_px = (int(hand_data.center_x * w), int(hand_data.center_y * h))
            cv2.circle(frame, center_px, 5, (255, 255, 0), -1)
            
            # Draw hand info text
            info_y = 120 + (hand_data.hand_id * 80)
            cv2.putText(
                frame,
                f"Hand {hand_data.hand_id}: ({hand_data.center_x:.2f}, {hand_data.center_y:.2f})",
                (10, info_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
            cv2.putText(
                frame,
                f"  Pinch: {hand_data.pinch_length:.3f} @ {hand_data.pinch_angle:.1f}°",
                (10, info_y + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
            if hand_data.is_pinching:
                cv2.putText(
                    frame,
                    "  PINCHING!",
                    (10, info_y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )
        
        # Draw status bar at top
        source_name = "NDI" if self.use_ndi else f"Camera {self.camera_id}"
        hand_count = len(hands_data)
        
        cv2.putText(
            frame,
            f"{source_name} | Hands: {hand_count} | Frame: {self.frame_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        cv2.putText(
            frame,
            "Press 'q' to quit",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )
        
        # Draw OSC indicator
        cv2.putText(
            frame,
            "📡 OSC Broadcasting",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1
        )
    
    def run(self):
        """
        Main application loop
        
        This runs continuously:
        1. Captures video frames
        2. Processes hands
        3. Sends OSC data
        4. Displays annotated video
        5. Handles user input
        """
        # Try to setup NDI first
        if not self.setup_ndi_receiver():
            print("⚠️  NDI not available, trying camera fallback...")
            self.use_ndi = False
            
            if not self.setup_camera_fallback():
                print("❌ No video source available!")
                print("Please ensure:")
                print("  - NDI source is running on network, OR")
                print("  - Camera is connected and configured")
                return
        
        print("\n🚀 Hand tracking started!")
        print("📡 OSC messages being sent to configured address")
        print("👁️  OpenCV window shows video with overlays")
        print("Press 'q' to quit\n")
        
        try:
            no_frame_count = 0
            max_no_frame_count = 100  # Allow more consecutive empty frames for hand tracking
            
            while True:
                # Get next frame
                frame = self.get_frame()
                
                if frame is None:
                    no_frame_count += 1
                    if no_frame_count >= max_no_frame_count:
                        print("⚠️  Too many consecutive empty frames, source may be unavailable")
                        break
                    elif no_frame_count % 20 == 0:
                        print(f"⚠️  No frame received ({no_frame_count}/{max_no_frame_count})")
                    
                    # Still check for 'q' key press even when no frame
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    continue
                
                # Reset no frame counter when we get a frame
                no_frame_count = 0
                self.frame_count += 1
                
                # Process hands in the frame
                hands_data, mp_results = self.process_hands(frame)
                
                # Send hand data via OSC
                if hands_data:
                    self.send_osc_data(hands_data)
                
                # Draw overlays on frame
                self.draw_overlays(frame, hands_data, mp_results)
                
                # Display the frame
                cv2.imshow('NDI Hand Tracking with OSC', frame)
                
                # Check for quit key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        finally:
            # Cleanup resources
            self.cleanup()
    
    def cleanup(self):
        """
        Clean up resources before exiting
        
        Properly releases video sources and closes windows
        """
        print("\n🧹 Cleaning up...")
        
        if self.ndi_receiver:
            # Clean up NDI receiver resources using the shared utilities
            self.ndi_receiver.cleanup()
            self.ndi_receiver = None
        
        if self.camera_cap:
            self.camera_cap.release()
        
        cv2.destroyAllWindows()
        
        print("👋 Hand tracking stopped")


def main():
    """
    Entry point for the application
    
    This function handles command-line arguments and starts the tracker
    """
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="NDI Hand Tracking with OSC - Track hands from NDI video and broadcast via OSC"
    )
    parser.add_argument(
        '--ndi-source',
        type=str,
        default=None,
        help='Name of NDI source to connect to (default: auto-detect first source)'
    )
    parser.add_argument(
        '--osc-ip',
        type=str,
        default='127.0.0.1',
        help='IP address for OSC messages (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--osc-port',
        type=int,
        default=8000,
        help='Port number for OSC messages (default: 8000)'
    )
    
    args = parser.parse_args()
    
    # Create and run the tracker
    tracker = NDIHandTracker(
        ndi_source_name=args.ndi_source,
        osc_ip=args.osc_ip,
        osc_port=args.osc_port
    )
    
    tracker.run()


if __name__ == "__main__":
    main()
