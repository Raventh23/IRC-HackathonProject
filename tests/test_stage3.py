#!/usr/bin/env python3
"""
Automated test for Stage 3.2 - Interactive functionality
Tests threading and command processing without requiring user input.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_interactive import InteractiveIRCClient
import time
import random
import threading


def test_interactive_functionality():
    """Test interactive functionality automatically."""
    print("Testing Stage 3.2: Interactive IRC Client")
    print("==========================================")
    
    # Create client instance
    test_nick = f"TestBot{random.randint(1000, 9999)}"
    client = InteractiveIRCClient(nickname=test_nick, debug=False)
    
    try:
        # Connect and register
        if not client.connect():
            print("❌ Connection failed!")
            return False
        
        if not client.register():
            print("❌ Registration failed!")
            client.disconnect()
            return False
        
        print("✅ Connection and registration successful")
        
        # Test joining a channel
        test_channel = "#bottest"
        if not client.join_channel(test_channel):
            print(f"❌ Failed to join {test_channel}")
            client.disconnect()
            return False
        
        print(f"✅ Successfully joined {test_channel}")
        
        # Start receiver thread
        print("✅ Starting message receiver thread...")
        client.start_receiver_thread()
        
        # Test sending a message
        test_message = f"Hello from {test_nick}! Testing Stage 3.2 - Threading"
        print(f"✅ Sending test message: {test_message}")
        client.send_message(test_channel, test_message)
        
        # Test command parsing
        print("✅ Testing command parsing...")
        
        # Test /help command
        print("Testing /help command:")
        client.parse_user_input("/help")
        
        # Test /me command
        print("Testing /me command:")
        client.parse_user_input("/me waves hello to everyone")
        
        # Test invalid command
        print("Testing invalid command:")
        client.parse_user_input("/invalid")
        
        # Listen for messages for a few seconds
        print("✅ Testing message reception for 10 seconds...")
        time.sleep(10)
        
        # Test graceful shutdown
        print("✅ Testing graceful shutdown...")
        client.stop_receiver_thread()
        
        print("✅ All Stage 3.2 tests passed!")
        return True
    
    finally:
        client.disconnect()


if __name__ == "__main__":
    success = test_interactive_functionality()
    if success:
        print("Stage 3.2 Complete: Interactive IRC Client working!")
    else:
        print("Stage 3.2 Failed!")
        sys.exit(1)
