#!/usr/bin/env python3
"""
Simple NDI test to verify the shared utilities work
"""

from ndi_utils import NDIReceiver
import time

def test_ndi_basic():
    print("🧪 Testing NDI utilities...")
    
    # Test source discovery
    receiver = NDIReceiver()
    sources = receiver.find_sources()
    
    if sources:
        print(f"✅ Found {len(sources)} sources:")
        for source in sources:
            print(f"  - {source.name} ({source.stream_name})")
        
        # Test connection
        print("\n🔗 Testing connection...")
        if receiver.connect():
            print("✅ Connection successful!")
            
            # Test frame capture
            print("📹 Testing frame capture...")
            for i in range(5):
                frame = receiver.get_frame()
                if frame is not None:
                    print(f"✅ Frame {i+1}: {frame.shape}")
                else:
                    print(f"⚠️  Frame {i+1}: None")
                time.sleep(0.1)
        else:
            print("❌ Connection failed")
    else:
        print("❌ No sources found")
    
    # Cleanup
    receiver.cleanup()
    print("👋 Test complete")

if __name__ == "__main__":
    test_ndi_basic()