#!/usr/bin/env python3
"""
NDI Utilities Module
===================

This module provides common NDI (Network Device Interface) functionality
using cyndilib, following the official documentation patterns.

It can be used by both the test NDI receiver and the hand tracking application
to ensure consistent NDI handling.
"""

import cv2
import numpy as np
import time
import sys

try:
    import cyndilib as ndi
    from cyndilib.wrapper.ndi_recv import RecvColorFormat, RecvBandwidth
    from cyndilib.wrapper.ndi_structs import FourCC
except ImportError:
    print("❌ Error: cyndilib not installed")
    print("Install with: pip install cyndilib")
    sys.exit(1)


class NDISource:
    """Helper class to hold NDI source information"""
    
    def __init__(self, source):
        self.source = source
        self.name = source.name
        self.stream_name = source.stream_name
        
        # Handle ip_address safely (not available in all versions)
        try:
            self.ip_address = source.ip_address
        except AttributeError:
            self.ip_address = "Not available"


class NDIReceiver:
    """
    NDI Receiver class using proper cyndilib patterns
    
    This class handles NDI source discovery, connection, and frame reception
    using the with statement pattern recommended in the cyndilib documentation.
    """
    
    def __init__(self, source_name=None, color_format=RecvColorFormat.BGRX_BGRA, bandwidth=RecvBandwidth.highest):
        """
        Initialize NDI receiver
        
        Args:
            source_name: Name of NDI source to connect to (None = auto-detect)
            color_format: NDI color format (default: BGRX_BGRA for OpenCV compatibility)
            bandwidth: NDI bandwidth setting (default: highest)
        """
        self.source_name = source_name
        self.color_format = color_format
        self.bandwidth = bandwidth
        self.finder = None
        self.receiver = None
        self.video_frame = None
        self.current_source = None
        self.is_initialized = False
        
    def find_sources(self):
        """
        Find available NDI sources using with statement
        
        Returns:
            list: List of NDISource objects, or None if no sources found
        """
        print("🔍 Searching for NDI sources...")
        
        # Use with statement as shown in cyndilib documentation
        with ndi.Finder() as finder:
            print("⏳ Waiting for NDI sources...")
            finder.wait_for_sources(timeout=10)
            
            # Get available sources
            sources = list(finder)
            
            if not sources:
                print("⚠️  No NDI sources found on network")
                return None
            
            print(f"📺 Found {len(sources)} NDI source(s):")
            ndi_sources = []
            for i, source in enumerate(sources):
                ndi_source = NDISource(source)
                ndi_sources.append(ndi_source)
                print(f"  {i + 1}. {ndi_source.name}")
                print(f"      Stream: {ndi_source.stream_name}")
                print(f"      IP: {ndi_source.ip_address}")
            
            return ndi_sources
    
    def select_source(self, sources):
        """
        Select an NDI source based on the configured source name
        
        Args:
            sources: List of NDISource objects
            
        Returns:
            NDISource: Selected source, or None if not found
        """
        if not sources:
            return None
            
        selected_source = None
        if self.source_name:
            # Try to find the specified source by name or stream_name
            for source in sources:
                if (source.name == self.source_name or 
                    source.stream_name == self.source_name or
                    self.source_name in source.name):
                    selected_source = source
                    break
            
            if not selected_source:
                print(f"⚠️  Source '{self.source_name}' not found, using first source")
                selected_source = sources[0]
        else:
            # Use first available source
            selected_source = sources[0]
        
        return selected_source
    
    def connect(self):
        """
        Connect to NDI source using with statement pattern
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Find and select source first
            sources = self.find_sources()
            if not sources:
                return False
            
            # Select source
            selected_source = self.select_source(sources)
            if not selected_source:
                return False
            
            print(f"✅ Connecting to NDI source: {selected_source.name}")
            
            # Create a new finder for connection (the old one is closed after find_sources)
            self.finder = ndi.Finder()
            self.finder.wait_for_sources(timeout=5)
            finder_sources = list(self.finder)
            
            # Find the actual source object in the new finder
            current_source = None
            for source in finder_sources:
                if source.name == selected_source.name:
                    current_source = source
                    break
            
            if not current_source:
                # Try one more time with a longer wait
                print("⏳ Source not immediately available, waiting longer...")
                self.finder.wait_for_sources(timeout=10)
                finder_sources = list(self.finder)
                
                for source in finder_sources:
                    if source.name == selected_source.name:
                        current_source = source
                        break
                
                if not current_source:
                    print("❌ Source no longer available")
                    return False
            
            # Store the current source
            self.current_source = selected_source
            
            # Create receiver with proper configuration
            self.receiver = ndi.Receiver(
                color_format=self.color_format,
                bandwidth=self.bandwidth
            )
            
            # Create video frame sync object
            self.video_frame = ndi.VideoFrameSync()
            self.receiver.frame_sync.set_video_frame(self.video_frame)
            
            # Set the source and wait for connection
            self.receiver.set_source(current_source)
            
            # Wait for connection
            connection_attempts = 0
            while not self.receiver.is_connected():
                if connection_attempts > 30:
                    print("❌ Timeout waiting for NDI connection")
                    return False
                if connection_attempts % 10 == 0:
                    print(f"⏳ Waiting for connection... ({connection_attempts}/30)")
                time.sleep(0.5)
                connection_attempts += 1
            
            print("✅ NDI receiver connected successfully")
            
            # Wait for first frame to ensure everything is working
            if not self._wait_for_first_frame():
                print("❌ Failed to receive first frame")
                return False
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"❌ NDI connection failed: {e}")
            import traceback
            traceback.print_exc()
            self.cleanup()
            return False
    
    def _wait_for_first_frame(self):
        """
        Wait for the first frame with actual data
        
        Returns:
            bool: True if first frame received, False if timeout
        """
        print("⏳ Waiting for first frame...")
        
        attempts = 0
        max_attempts = 100
        
        while self.receiver.is_connected() and attempts < max_attempts:
            self.receiver.frame_sync.capture_video()
            
            if self.video_frame is not None:
                resolution = self.video_frame.get_resolution()
                if min(resolution) > 0 and self.video_frame.get_data_size() > 0:
                    frame_rate = self.video_frame.get_frame_rate()
                    print(f"✅ First frame received: {resolution[0]}x{resolution[1]} @ {float(frame_rate):.2f}fps")
                    return True
            
            attempts += 1
            time.sleep(0.1)
        
        print("❌ Timeout waiting for first frame")
        return False
    
    def is_connected(self):
        """
        Check if the receiver is connected
        
        Returns:
            bool: True if connected, False otherwise
        """
        return (self.is_initialized and 
                self.receiver is not None and 
                self.receiver.is_connected())
    
    def get_frame(self):
        """
        Get a video frame as OpenCV BGR format
        
        Returns:
            numpy.ndarray: BGR image frame, or None if no frame available
        """
        if not self.is_connected():
            return None
            
        try:
            # Capture video frame
            self.receiver.frame_sync.capture_video()
            
            if self.video_frame is not None:
                resolution = self.video_frame.get_resolution()
                if min(resolution) > 0 and self.video_frame.get_data_size() > 0:
                    # Convert frame data to numpy array
                    frame_data = np.frombuffer(self.video_frame, dtype=np.uint8)
                    
                    # Get frame properties
                    width, height = resolution
                    fourcc = self.video_frame.get_fourcc()
                    
                    # Handle different pixel formats
                    if fourcc.name in ['BGRX', 'BGRA']:
                        # BGRX/BGRA format - reshape and convert to BGR
                        channels = 4
                        frame = frame_data.reshape((height, width, channels))
                        # Convert to BGR (remove alpha if present)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR) if fourcc.name == 'BGRA' else frame[:,:,:3]
                    elif fourcc.name in ['RGBX', 'RGBA']:
                        # RGBX/RGBA format - reshape and convert to BGR
                        channels = 4
                        frame = frame_data.reshape((height, width, channels))
                        # Convert to BGR
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR) if fourcc.name == 'RGBA' else cv2.cvtColor(frame[:,:,:3], cv2.COLOR_RGB2BGR)
                    elif fourcc.name == 'UYVY':
                        # UYVY format - need special handling
                        frame = frame_data.reshape((height, width * 2))
                        frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_UYVY)
                    else:
                        # Try to handle as BGR directly
                        try:
                            frame = frame_data.reshape((height, width, 3))
                        except ValueError:
                            # If reshape fails, try with 4 channels and drop alpha
                            frame = frame_data.reshape((height, width, 4))
                            frame = frame[:,:,:3]
                    
                    return frame
                    
        except Exception as e:
            # Handle specific NDI disconnection errors gracefully
            error_msg = str(e).lower()
            if 'connection' in error_msg or 'disconnect' in error_msg or 'timeout' in error_msg:
                print(f"📡 NDI connection issue: {e}")
            else:
                print(f"❌ Error getting frame: {e}")
            return None
        
        return None
    
    def get_source_info(self):
        """
        Get information about the current NDI source
        
        Returns:
            dict: Source information, or None if not connected
        """
        if not self.current_source:
            return None
        
        return {
            'name': self.current_source.name,
            'stream_name': self.current_source.stream_name,
            'ip_address': self.current_source.ip_address
        }
    
    def cleanup(self):
        """Clean up NDI resources"""
        if self.receiver:
            self.receiver = None
        
        if self.video_frame:
            self.video_frame = None
        
        if self.finder:
            self.finder = None
        
        self.current_source = None
        self.is_initialized = False
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()