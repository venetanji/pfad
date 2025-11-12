#!/usr/bin/env python3
"""
OSC Message Format Example

This script demonstrates the OSC message format used by ndi_hand_tracking.py
It shows what messages look like and can be used to test OSC receivers.

Run this to send sample OSC messages without needing NDI or camera setup.
"""

import time
import math

try:
    from pythonosc import udp_client
except ImportError:
    print("❌ python-osc not installed")
    print("Install with: pip install python-osc")
    exit(1)

def main():
    """Send example OSC messages"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Send example OSC messages from hand tracking"
    )
    parser.add_argument(
        '--osc-ip',
        type=str,
        default='127.0.0.1',
        help='OSC IP address (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--osc-port',
        type=int,
        default=8000,
        help='OSC port (default: 8000)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=10,
        help='Duration in seconds (default: 10)'
    )
    
    args = parser.parse_args()
    
    print("📡 OSC Message Format Example")
    print("=" * 50)
    print(f"Sending to: {args.osc_ip}:{args.osc_port}")
    print(f"Duration: {args.duration} seconds")
    print("\nMessage Format:")
    print("  /hand/0/position [x, y]")
    print("  /hand/0/pinch_length [length]")
    print("  /hand/0/pinch_angle [angle]")
    print("  /hand/0/is_pinching [state]")
    print("\nPress Ctrl+C to stop\n")
    
    # Create OSC client
    client = udp_client.SimpleUDPClient(args.osc_ip, args.osc_port)
    
    start_time = time.time()
    frame = 0
    
    try:
        while time.time() - start_time < args.duration:
            # Generate animated hand data
            t = time.time() - start_time
            
            # Simulate hand 0 moving in a circle
            x0 = 0.5 + 0.3 * math.cos(t)
            y0 = 0.5 + 0.3 * math.sin(t)
            
            # Simulate pinch gesture with oscillating length
            pinch_length = 0.1 + 0.05 * math.sin(t * 2)
            pinch_angle = (t * 45) % 360 - 180  # Rotate over time
            is_pinching = pinch_length < 0.05
            
            # Send hand 0 messages
            client.send_message("/hand/0/position", [x0, y0])
            client.send_message("/hand/0/pinch_length", pinch_length)
            client.send_message("/hand/0/pinch_angle", pinch_angle)
            client.send_message("/hand/0/is_pinching", 1.0 if is_pinching else 0.0)
            
            # Optionally send hand 1 (second hand)
            if frame % 60 < 30:  # Hand 1 appears for half the time
                x1 = 0.5 - 0.2 * math.cos(t * 0.5)
                y1 = 0.5 + 0.2 * math.sin(t * 0.5)
                
                client.send_message("/hand/1/position", [x1, y1])
                client.send_message("/hand/1/pinch_length", 0.15)
                client.send_message("/hand/1/pinch_angle", 45.0)
                client.send_message("/hand/1/is_pinching", 0.0)
            
            frame += 1
            
            # Print status every second
            if frame % 30 == 0:
                elapsed = time.time() - start_time
                print(f"[{elapsed:.1f}s] Frame {frame} | Hand 0: ({x0:.2f}, {y0:.2f}) | Pinch: {pinch_length:.3f}")
            
            # Send at ~30 fps
            time.sleep(1/30)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    
    elapsed = time.time() - start_time
    print(f"\n✅ Sent {frame} frames over {elapsed:.1f} seconds")
    print(f"📊 Average rate: {frame/elapsed:.1f} fps")

if __name__ == "__main__":
    main()
