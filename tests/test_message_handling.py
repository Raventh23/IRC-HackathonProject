#!/usr/bin/env python3
"""
Enhanced test for Stage 2.2 - Basic Message Handling
Tests raw IRC commands and server response handling.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.irc_client import IRCClient
import time
import random


def test_message_handling():
    """Test advanced message handling capabilities."""
    print("Testing Stage 2.2: Basic Message Handling")
    print("==========================================")
    
    # Create client with unique nickname
    test_nick = f"TestBot{random.randint(1000, 9999)}"
    client = IRCClient(nickname=test_nick)
    
    # Connect and register
    if not client.connect():
        print("Connection failed!")
        return False
    
    if not client.register():
        print("Registration failed!")
        client.disconnect()
        return False
    
    # Test sending various IRC commands
    print("\nTesting raw IRC commands...")
    
    # Test LUSERS command (get user statistics)
    print("Sending LUSERS command...")
    client.send_raw("LUSERS")
    
    # Test MOTD command (message of the day)
    print("Sending MOTD command...")
    client.send_raw("MOTD")
    
    # Test TIME command (server time)
    print("Sending TIME command...")
    client.send_raw("TIME")
    
    # Listen for responses for 15 seconds
    print("Listening for server responses for 15 seconds...")
    start_time = time.time()
    ping_count = 0
    message_count = 0
    
    while time.time() - start_time < 15:
        messages = client.receive_raw()
        for raw_msg in messages:
            message_count += 1
            print(f"<<< {raw_msg}")
            msg = client.parse_message(raw_msg)
            
            # Handle PING
            if msg['command'] == 'PING':
                ping_count += 1
                pong_response = f"PONG :{msg['trailing']}"
                client.send_raw(pong_response)
                print(f"Responded to PING #{ping_count}")
            
            # Show parsed message details for interesting commands
            elif msg['command'] in ['251', '252', '253', '254', '255', '372', '375', '376', '391']:
                print(f"    Parsed: Command={msg['command']}, Params={msg['params']}, Trailing='{msg['trailing']}'")
        
        time.sleep(0.1)
    
    print(f"\nReceived {message_count} messages total")
    print(f"Handled {ping_count} PING requests")
    
    # Disconnect
    client.disconnect()
    
    if message_count > 0:
        print("✅ Stage 2.2 Complete: Basic Message Handling working")
        return True
    else:
        print("❌ Stage 2.2 Failed: No messages received")
        return False


if __name__ == "__main__":
    success = test_message_handling()
    sys.exit(0 if success else 1)
