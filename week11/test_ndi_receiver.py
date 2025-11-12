#!/usr/bin/env python3
"""
Test NDI Receiver using cyndilib
================================

This script demonstrates the proper way to receive NDI video using cyndilib,
following the official documentation pattern from:
https://cyndilib.readthedocs.io/en/latest/examples.html#receiver

This uses the shared NDI utilities module for consistent NDI handling.
"""

import cv2
import numpy as np
import time
import sys

# Import the shared NDI utilities
from ndi_utils import NDIReceiver


class NDIReceiverTest:
    """Simple NDI receiver test using the shared NDI utilities"""
    
    def __init__(self, source_name=None):
        self.source_name = source_name
    
    def run_test(self):
        """Run the NDI receiver test using the shared NDI utilities"""
        try:
            # Create NDI receiver with the shared utilities
            with NDIReceiver(source_name=self.source_name) as ndi_receiver:
                # Connect to NDI source
                if not ndi_receiver.connect():
                    return False
                
                # Get source info
                source_info = ndi_receiver.get_source_info()
                print(f"✅ Connected to: {source_info['name']}")
                
                print("\n🎬 Starting video display...")
                print("Press 'q' to quit, 's' to save a frame")
                
                frame_count = 0
                no_frame_count = 0
                max_no_frame_count = 50  # Allow 50 consecutive empty frames before considering disconnection
                
                while True:
                    # Check if receiver is still connected
                    if not ndi_receiver.is_connected():
                        print("📡 NDI source disconnected")
                        break
                    
                    frame = ndi_receiver.get_frame()
                    
                    if frame is not None:
                        frame_count += 1
                        no_frame_count = 0  # Reset no frame counter
                        
                        # Add info overlay
                        cv2.putText(
                            frame,
                            f"NDI Source: {source_info['name']}",
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 255),
                            2
                        )
                        
                        cv2.putText(
                            frame,
                            f"Frame: {frame_count}",
                            (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (255, 255, 255),
                            1
                        )
                        
                        cv2.putText(
                            frame,
                            "Press 'q' to quit, 's' to save frame",
                            (10, frame.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 255),
                            1
                        )
                        
                        # Display frame
                        cv2.imshow('NDI Receiver Test', frame)
                        
                        # Handle keyboard input
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q'):
                            break
                        elif key == ord('s'):
                            filename = f"ndi_frame_{frame_count:04d}.png"
                            cv2.imwrite(filename, frame)
                            print(f"📸 Saved frame to {filename}")
                    else:
                        no_frame_count += 1
                        if no_frame_count >= max_no_frame_count:
                            print("⚠️  Too many consecutive empty frames, source may be unavailable")
                            break
                        elif no_frame_count % 10 == 0:
                            print(f"⚠️  No frame received ({no_frame_count}/{max_no_frame_count})")
                        
                        # Still check for 'q' key press even when no frame
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q'):
                            break
                        
                        time.sleep(0.1)
                
                print("\n📺 Video stream ended")
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
            return True
        except Exception as e:
            print(f"❌ Error during test: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            cv2.destroyAllWindows()
            print("👋 NDI receiver test stopped")
    



def main():
    """Entry point for the NDI receiver test"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test NDI receiver using cyndilib"
    )
    parser.add_argument(
        '--source',
        type=str,
        default=None,
        help='Name of NDI source to connect to (default: use first available)'
    )
    
    args = parser.parse_args()
    
    print("🎬 NDI Receiver Test")
    print("=" * 50)
    print("This test will:")
    print("1. Search for NDI sources on the network")
    print("2. Connect to the specified (or first available) source")
    print("3. Display the video stream in an OpenCV window")
    print("4. Allow you to save frames by pressing 's'")
    print("5. Exit when you press 'q'")
    print()
    
    receiver = NDIReceiverTest(source_name=args.source)
    success = receiver.run_test()
    
    if success:
        print("✅ NDI receiver test completed successfully")
    else:
        print("❌ NDI receiver test failed")
        sys.exit(1)


if __name__ == "__main__":
    main()