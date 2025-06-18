#!/usr/bin/env python3
"""
IRC Chat Demo - Stage 3 Complete
Interactive IRC client ready for real use!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_interactive import InteractiveIRCClient
import random


def main():
    """Demo the complete Stage 3 IRC client."""
    print("IRC Chat Client - Interactive Demo")
    print("==================================")
    print("This is a working IRC client!")
    print()
    
    # Get user preferences
    nickname = input("Enter your nickname (or press Enter for random): ").strip()
    if not nickname:
        nickname = f"IRCUser{random.randint(100, 999)}"
    
    channel = input("Enter channel to join (default: #bottest): ").strip()
    if not channel:
        channel = "#bottest"
    elif not channel.startswith('#'):
        channel = '#' + channel
    
    server = input("Enter IRC server (default: irc.libera.chat): ").strip()
    if not server:
        server = "irc.libera.chat"
    
    print(f"\nConnecting to {server} as {nickname}...")
    print(f"Will auto-join {channel}")
    print()
    
    # Create and start client
    client = InteractiveIRCClient(
        server=server,
        nickname=nickname,
        username=nickname.lower(),
        realname=f"{nickname} IRC Client"
    )
    
    try:
        # Connect and register
        if not client.connect():
            print("❌ Connection failed!")
            return
        
        if not client.register():
            print("❌ Registration failed!")
            client.disconnect()
            return
        
        # Start interactive session
        client.interactive_session(channel)
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
