#!/usr/bin/env python3
"""
Test script to verify error handling works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.irc_client import IRCClient

def test_error_handling():
    """Test various error conditions."""
    print("Testing error handling...")
    
    # Test invalid server
    print("\n1. Testing invalid server:")
    client = IRCClient("invalid.server.test", 6667)
    client.connect()
    
    # Test invalid port
    print("\n2. Testing invalid port:")
    client2 = IRCClient("irc.libera.chat", 99999)
    client2.connect()
    
    print("\nError handling tests complete!")

if __name__ == "__main__":
    test_error_handling()
