#!/usr/bin/env python3
"""
Interactive IRC Chat Client - Stage 3.2
Implements threading for simultaneous send/receive and user input handling.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.irc_client import IRCClient
import threading
import time
import random


class InteractiveIRCClient(IRCClient):
    """Interactive IRC client with threading support."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = False
        self.receiver_thread = None
        self.input_prompt = "> "
    
    def start_receiver_thread(self):
        """Start the background thread for receiving messages."""
        self.running = True
        self.receiver_thread = threading.Thread(target=self._message_receiver, daemon=True)
        self.receiver_thread.start()
        self.log_debug("Message receiver thread started")
    
    def stop_receiver_thread(self):
        """Stop the background message receiver thread."""
        self.running = False
        if self.receiver_thread and self.receiver_thread.is_alive():
            self.receiver_thread.join(timeout=2)
        self.log_debug("Message receiver thread stopped")
    
    def _message_receiver(self):
        """Background thread function to continuously receive messages."""
        while self.running and self.connected:
            try:
                messages = self.receive_raw()
                for raw_msg in messages:
                    if not self.running:
                        break
                    
                    self.log_debug(f"Received: {raw_msg}")
                    msg = self.parse_message(raw_msg)
                    
                    # Handle PING/PONG automatically
                    if msg['command'] == 'PING':
                        pong_response = f"PONG :{msg['trailing']}"
                        self.send_raw(pong_response)
                        self.log_debug("Auto-responded to PING")
                        continue
                    
                    # Format and display channel messages
                    elif msg['command'] in ['PRIVMSG', 'JOIN', 'PART', 'QUIT']:
                        formatted = self.format_channel_message(msg)
                        if formatted:
                            # Clear current input line, show message, restore prompt
                            print(f"\r{' ' * 50}\r{formatted}")
                            print(self.input_prompt, end='', flush=True)
                    
                    # Handle server messages
                    elif msg['command'].isdigit():
                        # Only show important server messages
                        if msg['command'] in ['332', '353', '366']:  # Topic, names, end of names
                            if msg['command'] == '332':  # Topic
                                topic_channel = msg['params'][1] if len(msg['params']) > 1 else ""
                                topic = msg['trailing']
                                print(f"\r{' ' * 50}\r[{self.format_timestamp()}] Topic for {topic_channel}: {topic}")
                                print(self.input_prompt, end='', flush=True)
                            elif msg['command'] == '353':  # Names list
                                names_channel = msg['params'][2] if len(msg['params']) > 2 else ""
                                names = msg['trailing'].split()
                                print(f"\r{' ' * 50}\r[{self.format_timestamp()}] Users in {names_channel}: {', '.join(names)}")
                                print(self.input_prompt, end='', flush=True)
                
                time.sleep(0.1)  # Small delay to prevent CPU spinning
                
            except Exception as e:
                if self.running:
                    self.log_debug(f"Receiver thread error: {e}")
                time.sleep(1)
    
    def parse_user_input(self, user_input):
        """Parse user input and execute commands or send messages."""
        user_input = user_input.strip()
        
        if not user_input:
            return True
        
        # Handle commands
        if user_input.startswith('/'):
            parts = user_input[1:].split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if command == 'quit':
                quit_message = args if args else "Goodbye!"
                print(f"Quitting with message: {quit_message}")
                self.send_raw(f"QUIT :{quit_message}")
                return False
            
            elif command == 'join':
                if args:
                    channel = args.strip()
                    if not channel.startswith('#'):
                        channel = '#' + channel
                    print(f"Joining {channel}...")
                    if self.join_channel(channel):
                        print(f"Successfully joined {channel}")
                    else:
                        print(f"Failed to join {channel}")
                else:
                    print("Usage: /join #channel")
            
            elif command == 'nick':
                if args:
                    new_nick = args.strip()
                    print(f"Changing nickname to {new_nick}...")
                    self.send_raw(f"NICK {new_nick}")
                    self.nickname = new_nick
                else:
                    print("Usage: /nick newnickname")
            
            elif command == 'help':
                print("Available commands:")
                print("  /quit [message] - Disconnect and exit")
                print("  /join #channel  - Join a channel")
                print("  /nick nickname  - Change your nickname")
                print("  /help          - Show this help")
                print("  /me action     - Send action message")
                print("Type messages directly to send to current channel")
            
            elif command == 'me':
                if args and self.current_channel:
                    action_message = f"\x01ACTION {args}\x01"
                    self.send_message(self.current_channel, action_message)
                else:
                    print("Usage: /me action (must be in a channel)")
            
            else:
                print(f"Unknown command: /{command}. Type /help for available commands.")
        
        else:
            # Send message to current channel
            if self.current_channel:
                self.send_message(self.current_channel, user_input)
                # Show our own message
                timestamp = self.format_timestamp()
                print(f"\r{' ' * 50}\r[{timestamp}] <{self.nickname}> {user_input}")
                print(self.input_prompt, end='', flush=True)
            else:
                print("You must join a channel first. Use /join #channel")
        
        return True
    
    def interactive_session(self, initial_channel=None):
        """Start an interactive chat session."""
        print("\n" + "="*50)
        print("Interactive IRC Chat Session")
        print("="*50)
        print("Type /help for available commands")
        print("Type /quit to exit")
        
        if initial_channel:
            print(f"Auto-joining {initial_channel}...")
            if self.join_channel(initial_channel):
                print(f"Successfully joined {initial_channel}")
            else:
                print(f"Failed to join {initial_channel}")
        
        print("="*50)
        
        # Start receiver thread
        self.start_receiver_thread()
        
        try:
            while self.connected and self.running:
                try:
                    user_input = input(self.input_prompt)
                    if not self.parse_user_input(user_input):
                        break
                except KeyboardInterrupt:
                    print("\nReceived Ctrl+C, exiting...")
                    break
                except EOFError:
                    print("\nEOF received, exiting...")
                    break
        
        finally:
            # Clean shutdown
            self.stop_receiver_thread()
            time.sleep(0.5)  # Give time for final messages


def main():
    """Main function for Stage 3.2 - Interactive IRC Client."""
    print("Simple IRC Chat Client - Stage 3.2 Test")
    print("========================================")
    
    # Create client instance with unique nickname
    test_nick = f"TestBot{random.randint(1000, 9999)}"
    client = InteractiveIRCClient(nickname=test_nick, debug=False)
    
    try:
        # Connect and register
        if not client.connect():
            print("Connection failed!")
            sys.exit(1)
        
        if not client.register():
            print("Registration failed!")
            client.disconnect()
            sys.exit(1)
        
        # Start interactive session
        client.interactive_session("#bottest")
    
    finally:
        # Ensure cleanup
        client.disconnect()
        print("Stage 3.2 Complete: Interactive IRC Client working!")


if __name__ == "__main__":
    main()
