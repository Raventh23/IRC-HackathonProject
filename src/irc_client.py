#!/usr/bin/env python3
"""
Simple IRC Chat Client
A minimal IRC client for learning and educational purposes.
"""

import socket
import sys
import time
import re
import logging
from datetime import datetime


class IRCClient:
    """Basic IRC client with socket connection capabilities."""
    
    def __init__(self, server="irc.libera.chat", port=6667, nickname="SimpleBot", username="simple", realname="Simple IRC Client", debug=False):
        """Initialize IRC client with server details."""
        self.server = server
        self.port = port
        self.nickname = nickname
        self.username = username
        self.realname = realname
        self.socket = None
        self.connected = False
        self.registered = False
        self.buffer = ""  # Buffer for incomplete messages
        self.debug = debug
        self.current_channel = None
        self.channels = set()  # Track joined channels
        
        # Set up logging if debug enabled
        if self.debug:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = None
    
    def log_debug(self, message):
        """Log debug message if debugging is enabled."""
        if self.logger:
            self.logger.debug(message)
    
    def format_timestamp(self):
        """Return current time formatted for display."""
        return datetime.now().strftime("%H:%M")
    
    def connect(self):
        """Establish TCP connection to IRC server."""
        try:
            print(f"Connecting to {self.server}:{self.port}...")
            self.log_debug(f"Creating socket connection to {self.server}:{self.port}")
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout
            self.socket.connect((self.server, self.port))
            self.connected = True
            
            print(f"Connected to {self.server}!")
            self.log_debug("Socket connection established successfully")
            return True
            
        except socket.timeout:
            print("Error: Connection timed out")
            self.log_debug("Connection attempt timed out")
            return False
        except socket.gaierror as e:
            print("Error: Could not resolve server address")
            self.log_debug(f"DNS resolution failed: {e}")
            return False
        except ConnectionRefusedError:
            print("Error: Connection refused by server")
            self.log_debug("Server refused connection")
            return False
        except Exception as e:
            print(f"Error: Failed to connect - {e}")
            self.log_debug(f"Connection failed with exception: {e}")
            return False
    
    def send_raw(self, message):
        """Send raw IRC message to server."""
        if not self.connected or not self.socket:
            print("Error: Not connected to server")
            return False
        
        try:
            # Ensure message ends with \r\n
            if not message.endswith('\r\n'):
                message += '\r\n'
            
            self.socket.send(message.encode('utf-8'))
            print(f">>> {message.strip()}")
            self.log_debug(f"Sent: {message.strip()}")
            return True
            
        except Exception as e:
            print(f"Error sending message: {e}")
            self.log_debug(f"Send failed: {e}")
            return False
    
    def receive_raw(self):
        """Receive raw data from server and return complete IRC messages."""
        if not self.connected or not self.socket:
            return []
        
        try:
            # Set socket to non-blocking for this receive
            self.socket.settimeout(0.1)
            data = self.socket.recv(4096).decode('utf-8', errors='ignore')
            
            if data:
                self.log_debug(f"Received raw data: {repr(data)}")
                self.buffer += data
            
            # Split buffer into complete messages
            messages = []
            while '\r\n' in self.buffer:
                line, self.buffer = self.buffer.split('\r\n', 1)
                if line.strip():
                    messages.append(line.strip())
                    self.log_debug(f"Complete message extracted: {line.strip()}")
            
            return messages
            
        except socket.timeout:
            return []
        except Exception as e:
            print(f"Error receiving data: {e}")
            self.log_debug(f"Receive failed: {e}")
            return []
        finally:
            # Reset socket timeout
            self.socket.settimeout(10)
    
    def parse_message(self, raw_message):
        """Parse IRC message into components."""
        # IRC message format: [:prefix] <command> [params] [:trailing]
        message = {'raw': raw_message, 'prefix': '', 'command': '', 'params': [], 'trailing': '', 'nick': '', 'host': ''}
        
        working_msg = raw_message
        
        # Extract prefix if present
        if working_msg.startswith(':'):
            prefix_end = working_msg.find(' ')
            if prefix_end != -1:
                message['prefix'] = working_msg[1:prefix_end]
                working_msg = working_msg[prefix_end + 1:]
                
                # Extract nickname from prefix (nick!user@host format)
                if '!' in message['prefix']:
                    message['nick'] = message['prefix'].split('!')[0]
                    if '@' in message['prefix']:
                        message['host'] = message['prefix'].split('@')[1]
        
        # Extract trailing if present
        trailing_start = working_msg.find(' :')
        if trailing_start != -1:
            message['trailing'] = working_msg[trailing_start + 2:]
            working_msg = working_msg[:trailing_start]
        
        # Split remaining into command and params
        parts = working_msg.split()
        if parts:
            message['command'] = parts[0]
            message['params'] = parts[1:]
        
        self.log_debug(f"Parsed message: {message}")
        return message
    
    def register(self):
        """Register with IRC server using NICK and USER commands."""
        if not self.connected:
            print("Error: Must be connected before registering")
            return False
        
        print(f"Registering as {self.nickname}...")
        self.log_debug(f"Starting registration process for nickname: {self.nickname}")
        
        # Send NICK command
        if not self.send_raw(f"NICK {self.nickname}"):
            return False
        
        # Send USER command
        if not self.send_raw(f"USER {self.username} 0 * :{self.realname}"):
            return False
        
        # Wait for registration to complete
        start_time = time.time()
        while time.time() - start_time < 30:  # 30 second timeout
            messages = self.receive_raw()
            for raw_msg in messages:
                print(f"<<< {raw_msg}")
                msg = self.parse_message(raw_msg)
                
                # Handle PING during registration
                if msg['command'] == 'PING':
                    pong_response = f"PONG :{msg['trailing']}"
                    self.send_raw(pong_response)
                    self.log_debug("Responded to PING during registration")
                
                # Check for welcome message (001)
                elif msg['command'] == '001':
                    print(f"Successfully registered! Welcome: {msg['trailing']}")
                    self.log_debug("Registration successful - received 001 welcome")
                    self.registered = True
                    return True
                
                # Check for nickname collision (433)
                elif msg['command'] == '433':
                    print(f"Nickname '{self.nickname}' is already in use")
                    # Try with a number suffix
                    old_nick = self.nickname
                    self.nickname += "_"
                    print(f"Trying nickname: {self.nickname}")
                    self.log_debug(f"Nickname collision: {old_nick} -> {self.nickname}")
                    self.send_raw(f"NICK {self.nickname}")
                
                # Check for other error codes
                elif msg['command'].isdigit() and msg['command'].startswith('4'):
                    print(f"Registration error: {msg['trailing']}")
                    self.log_debug(f"Registration error code: {msg['command']}")
                    return False
            
            time.sleep(0.1)
        
        print("Registration timed out")
        self.log_debug("Registration timed out after 30 seconds")
        return False
    
    def join_channel(self, channel):
        """Join an IRC channel."""
        if not self.registered:
            print("Error: Must be registered before joining channels")
            return False
        
        if not channel.startswith('#'):
            channel = '#' + channel
        
        print(f"Joining channel {channel}...")
        self.log_debug(f"Attempting to join channel: {channel}")
        
        if not self.send_raw(f"JOIN {channel}"):
            return False
        
        # Wait for join confirmation
        start_time = time.time()
        while time.time() - start_time < 15:  # 15 second timeout
            messages = self.receive_raw()
            for raw_msg in messages:
                print(f"<<< {raw_msg}")
                msg = self.parse_message(raw_msg)
                
                # Handle PING
                if msg['command'] == 'PING':
                    pong_response = f"PONG :{msg['trailing']}"
                    self.send_raw(pong_response)
                
                # Check for successful join (we receive our own JOIN message)
                elif msg['command'] == 'JOIN' and msg['nick'] == self.nickname:
                    joined_channel = msg['params'][0] if msg['params'] else msg['trailing']
                    print(f"Successfully joined {joined_channel}!")
                    self.current_channel = joined_channel
                    self.channels.add(joined_channel)
                    self.log_debug(f"Successfully joined channel: {joined_channel}")
                    return True
                
                # Handle channel topic (332)
                elif msg['command'] == '332':
                    topic_channel = msg['params'][1] if len(msg['params']) > 1 else ""
                    topic = msg['trailing']
                    print(f"[{self.format_timestamp()}] Topic for {topic_channel}: {topic}")
                
                # Handle names list (353)
                elif msg['command'] == '353':
                    names_channel = msg['params'][2] if len(msg['params']) > 2 else ""
                    names = msg['trailing'].split()
                    print(f"[{self.format_timestamp()}] Users in {names_channel}: {', '.join(names)}")
                
                # Handle end of names (366)
                elif msg['command'] == '366':
                    end_channel = msg['params'][1] if len(msg['params']) > 1 else ""
                    print(f"[{self.format_timestamp()}] End of names list for {end_channel}")
                
                # Check for join errors
                elif msg['command'].isdigit() and msg['command'].startswith('4'):
                    error_msg = msg['trailing']
                    print(f"Join error: {error_msg}")
                    self.log_debug(f"Join error code: {msg['command']}")
                    return False
            
            time.sleep(0.1)
        
        print("Join timed out")
        self.log_debug("Join operation timed out")
        return False
    
    def send_message(self, channel, message):
        """Send a message to a channel."""
        if not self.registered:
            print("Error: Must be registered before sending messages")
            return False
        
        if not channel.startswith('#'):
            channel = '#' + channel
        
        return self.send_raw(f"PRIVMSG {channel} :{message}")
    
    def format_channel_message(self, msg):
        """Format a channel message for display."""
        if msg['command'] == 'PRIVMSG':
            channel = msg['params'][0] if msg['params'] else ""
            sender = msg['nick']
            message_text = msg['trailing']
            timestamp = self.format_timestamp()
            
            # Check if it's an action message (/me)
            if message_text.startswith('\x01ACTION ') and message_text.endswith('\x01'):
                action_text = message_text[8:-1]  # Remove \x01ACTION and \x01
                return f"[{timestamp}] * {sender} {action_text}"
            else:
                return f"[{timestamp}] <{sender}> {message_text}"
        
        elif msg['command'] == 'JOIN':
            joined_channel = msg['params'][0] if msg['params'] else msg['trailing']
            joiner = msg['nick']
            timestamp = self.format_timestamp()
            return f"[{timestamp}] --> {joiner} has joined {joined_channel}"
        
        elif msg['command'] == 'PART':
            left_channel = msg['params'][0] if msg['params'] else ""
            leaver = msg['nick']
            part_message = msg['trailing']
            timestamp = self.format_timestamp()
            if part_message:
                return f"[{timestamp}] <-- {leaver} has left {left_channel} ({part_message})"
            else:
                return f"[{timestamp}] <-- {leaver} has left {left_channel}"
        
        elif msg['command'] == 'QUIT':
            quitter = msg['nick']
            quit_message = msg['trailing']
            timestamp = self.format_timestamp()
            if quit_message:
                return f"[{timestamp}] <-- {quitter} has quit ({quit_message})"
            else:
                return f"[{timestamp}] <-- {quitter} has quit"
        
        return None
    
    def handle_ping_pong(self):
        """Handle PING/PONG keepalive messages."""
        messages = self.receive_raw()
        for raw_msg in messages:
            if raw_msg.strip():
                print(f"<<< {raw_msg}")
                msg = self.parse_message(raw_msg)
                
                if msg['command'] == 'PING':
                    pong_response = f"PONG :{msg['trailing']}"
                    self.send_raw(pong_response)
                    print("Responded to PING")
                    self.log_debug(f"PING/PONG keepalive: {msg['trailing']}")
    
    def send_command(self, command, *args):
        """Send IRC command with arguments."""
        if args:
            # If last argument contains spaces, prefix with :
            if ' ' in str(args[-1]):
                cmd_args = ' '.join(str(arg) for arg in args[:-1])
                if cmd_args:
                    message = f"{command} {cmd_args} :{args[-1]}"
                else:
                    message = f"{command} :{args[-1]}"
            else:
                message = f"{command} {' '.join(str(arg) for arg in args)}"
        else:
            message = command
        
        return self.send_raw(message)
    
    def disconnect(self):
        """Close connection to IRC server."""
        if self.socket:
            try:
                if self.connected and self.registered:
                    self.send_raw("QUIT :Goodbye!")
                    time.sleep(1)  # Give server time to process QUIT
                
                self.socket.close()
                print("Disconnected from server")
                self.log_debug("Socket connection closed")
                
            except Exception as e:
                print(f"Error during disconnect: {e}")
                self.log_debug(f"Disconnect error: {e}")
            finally:
                self.connected = False
                self.registered = False
                self.socket = None


def main():
    """Main function to test Stage 3.1 - Channel Operations."""
    print("Simple IRC Chat Client - Stage 3.1 Test")
    print("========================================")
    
    # Create client instance with unique nickname
    import random
    test_nick = f"TestBot{random.randint(1000, 9999)}"
    client = IRCClient(nickname=test_nick, debug=False)
    
    # Test connection and registration
    if not client.connect():
        print("Connection failed!")
        sys.exit(1)
    
    if not client.register():
        print("Registration failed!")
        client.disconnect()
        sys.exit(1)
    
    # Test joining a channel
    test_channel = "#bottest"  # Use a bot testing channel
    if not client.join_channel(test_channel):
        print(f"Failed to join {test_channel}")
        client.disconnect()
        sys.exit(1)
    
    # Test sending a message
    test_message = f"Hello from {test_nick}! Testing Stage 3.1"
    print(f"Sending test message: {test_message}")
    client.send_message(test_channel, test_message)
    
    # Listen for channel messages for 30 seconds
    print("Listening for channel messages for 30 seconds...")
    start_time = time.time()
    message_count = 0
    
    while time.time() - start_time < 30:
        messages = client.receive_raw()
        for raw_msg in messages:
            print(f"<<< {raw_msg}")
            msg = client.parse_message(raw_msg)
            
            # Handle PING
            if msg['command'] == 'PING':
                pong_response = f"PONG :{msg['trailing']}"
                client.send_raw(pong_response)
                print("Responded to PING")
            
            # Format and display channel messages
            elif msg['command'] in ['PRIVMSG', 'JOIN', 'PART', 'QUIT']:
                formatted = client.format_channel_message(msg)
                if formatted:
                    print(formatted)
                    message_count += 1
        
        time.sleep(0.1)
    
    print(f"Processed {message_count} channel messages")
    
    # Disconnect
    client.disconnect()
    print("Stage 3.1 Complete: Channel Operations working!")


if __name__ == "__main__":
    main()
