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
        message = {'raw': raw_message, 'prefix': '', 'command': '', 'params': [], 'trailing': ''}
        
        working_msg = raw_message
        
        # Extract prefix if present
        if working_msg.startswith(':'):
            prefix_end = working_msg.find(' ')
            if prefix_end != -1:
                message['prefix'] = working_msg[1:prefix_end]
                working_msg = working_msg[prefix_end + 1:]
        
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
    """Main function to test IRC protocol basics."""
    print("Simple IRC Chat Client - Stage 2 Complete Test")
    print("===============================================")
    
    # Create client instance with unique nickname and debug enabled
    import random
    test_nick = f"TestBot{random.randint(1000, 9999)}"
    client = IRCClient(nickname=test_nick, debug=True)
    
    # Test connection
    if not client.connect():
        print("Connection failed!")
        sys.exit(1)
    
    # Test registration
    if not client.register():
        print("Registration failed!")
        client.disconnect()
        sys.exit(1)
    
    # Test some IRC commands using the new send_command method
    print("\nTesting IRC commands...")
    client.send_command("VERSION")
    client.send_command("TIME")
    
    # Test PING/PONG handling for a few seconds
    print("Testing PING/PONG handling for 5 seconds...")
    start_time = time.time()
    message_count = 0
    while time.time() - start_time < 5:
        messages = client.receive_raw()
        for raw_msg in messages:
            message_count += 1
            print(f"<<< {raw_msg}")
            msg = client.parse_message(raw_msg)
            
            if msg['command'] == 'PING':
                pong_response = f"PONG :{msg['trailing']}"
                client.send_raw(pong_response)
                print("Responded to PING")
        
        time.sleep(0.1)
    
    print(f"Processed {message_count} messages")
    
    # Disconnect
    client.disconnect()
    print("Stage 2 Complete: IRC Protocol Basics working perfectly!")


if __name__ == "__main__":
    main()
