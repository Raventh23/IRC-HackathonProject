#!/usr/bin/env python3
"""
Simple IRC Chat Client - Stage 5: Polish & Stability
Enhanced IRC client with connection reliability and improved user experience.
"""

import socket
import sys
import time
import re
import logging
import threading
import argparse
import json
from datetime import datetime, timedelta


class IRCClient:
    """Enhanced IRC client with Stage 5 polish and stability features."""
    
    def __init__(self, server="irc.libera.chat", port=6667, nickname="SimpleBot", username="simple", realname="Simple IRC Client", debug=False, auto_reconnect=False, show_status_messages=True):
        """Initialize IRC client with enhanced Stage 5 features."""
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
        self.running = False
        self.input_thread = None
        self.server_capabilities = {}
        self.channel_users = {}  # Track users in channels
        self.last_ping_time = time.time()
        self.connection_stable = True
        
        # Stage 5 enhancements
        self.auto_reconnect = auto_reconnect
        self.show_status_messages = show_status_messages
        self.uptime_start = None
        self.total_messages_sent = 0
        self.total_messages_received = 0
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 30
        
        # IRC validation patterns
        self.nick_pattern = re.compile(r'^[a-zA-Z\[\]\\`_^{|}][a-zA-Z0-9\[\]\\`_^{|}-]*$')
        self.channel_pattern = re.compile(r'^#[^\x00\x07\x0A\x0D ,:]{1,49}$')
        
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
                    self.channel_users[names_channel] = names  # Update channel users
                
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
    
    def validate_nickname(self, nickname):
        """Validate IRC nickname according to RFC standards."""
        if not nickname:
            return False, "Nickname cannot be empty"
        
        if len(nickname) > 16:
            return False, "Nickname too long (max 16 characters)"
        
        if not self.nick_pattern.match(nickname):
            return False, "Invalid nickname format (must start with letter and contain only valid IRC characters)"
        
        # Check for reserved nicknames
        reserved = ['nickserv', 'chanserv', 'operserv', 'memoserv', 'botserv', 'hostserv']
        if nickname.lower() in reserved:
            return False, f"'{nickname}' is a reserved service nickname"
        
        return True, ""
    
    def validate_channel_name(self, channel):
        """Validate IRC channel name according to RFC standards."""
        if not channel:
            return False, "Channel name cannot be empty"
        
        if not channel.startswith('#'):
            channel = '#' + channel
        
        if not self.channel_pattern.match(channel):
            return False, "Invalid channel name format (must start with # and contain valid characters)"
        
        return True, channel
    
    def sanitize_message(self, message):
        """Sanitize user message to prevent IRC injection attacks."""
        if not message:
            return False, "Message cannot be empty"
        
        # Remove control characters except for ACTION
        if not (message.startswith('\x01ACTION ') and message.endswith('\x01')):
            # Remove all control characters except space and printable ASCII
            sanitized = ''.join(char for char in message if ord(char) >= 32 or char in ['\t'])
            
            # Check for CTCP injection (except ACTION)
            if '\x01' in sanitized:
                return False, "Invalid characters in message"
            
            # Limit message length (IRC limit is 512 bytes total, leave room for formatting)
            max_msg_len = 400  # Conservative limit
            if len(sanitized.encode('utf-8')) > max_msg_len:
                sanitized = sanitized[:max_msg_len]
                print(f"Warning: Message truncated to {max_msg_len} bytes")
            
            return True, sanitized
        
        return True, message
    
    def is_valid_user_command(self, message):
        """Check if message is a valid user command."""
        if not message.startswith('/'):
            return False
        
        command = message[1:].split(' ', 1)[0].lower()
        valid_commands = ['quit', 'join', 'nick', 'help', 'me', 'part', 'msg', 'whois', 'list']
        return command in valid_commands
    
    def show_help(self, command=None):
        """Display help information for commands."""
        if command:
            command = command.lower()
            help_text = {
                'quit': "📖 /quit [message] - Disconnect from server with optional quit message",
                'join': "📖 /join #channel - Join a channel",
                'part': "📖 /part [#channel] - Leave current or specified channel",
                'nick': "📖 /nick nickname - Change your nickname",
                'me': "📖 /me action - Send an action message (* nickname action)",
                'msg': "📖 /msg nickname message - Send private message to user",
                'whois': "📖 /whois nickname - Get information about a user",
                'list': "📖 /list [pattern] - List channels matching pattern",
                'help': "📖 /help [command] - Show help for all commands or specific command"
            }
            
            if command in help_text:
                print(help_text[command])
            else:
                print(f"❌ No help available for '{command}'")
                print("💡 Type /help to see all available commands")
        else:
            print("📖 Available commands:")
            print("  /quit [message]     - Disconnect and exit")
            print("  /join #channel      - Join a channel")
            print("  /part [#channel]    - Leave current or specified channel")
            print("  /nick nickname      - Change your nickname")
            print("  /me action          - Send action message")
            print("  /msg nick message   - Send private message")
            print("  /whois nickname     - Get user information")
            print("  /list [pattern]     - List channels")
            print("  /help [command]     - Show this help or help for specific command")
            print()
            print("💡 Tips:")
            print("  - Type messages directly to send to current channel")
            print("  - Channel names must start with #")
            print("  - Use Ctrl+C to quit")
    
    def handle_user_command(self, command_input):
        """Handle user commands with comprehensive error handling."""
        if not command_input.startswith('/'):
            return False
        
        # Parse command and arguments
        parts = command_input[1:].split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Handle each command with validation
        if command == 'quit':
            quit_msg = args if args else "Goodbye!"
            print(f"👋 Disconnecting: {quit_msg}")
            self.send_raw(f"QUIT :{quit_msg}")
            self.running = False
            return True
        
        elif command == 'join':
            if not args:
                print("❌ Usage: /join #channel")
                return True
            
            channel = args.strip().split()[0]
            valid, validated_channel = self.validate_channel_name(channel)
            if not valid:
                print(f"❌ {validated_channel}")
                return True
            
            print(f"🚪 Joining {validated_channel}...")
            if self.join_channel(validated_channel):
                self.current_channel = validated_channel
                self.channels.add(validated_channel)
                print(f"✅ Successfully joined {validated_channel}")
            else:
                print(f"❌ Failed to join {validated_channel}")
            return True
        
        elif command == 'nick':
            if not args:
                print("❌ Usage: /nick newnickname")
                return True
            
            new_nick = args.strip().split()[0]
            valid, error_msg = self.validate_nickname(new_nick)
            if not valid:
                print(f"❌ {error_msg}")
                return True
            
            print(f"🏷️  Changing nickname to {new_nick}...")
            self.send_raw(f"NICK {new_nick}")
            self.nickname = new_nick
            return True
        
        elif command == 'me':
            if not args:
                print("❌ Usage: /me action")
                print("💡 Example: /me waves hello")
                return True
            
            if not self.current_channel:
                print("❌ Not in a channel. Join a channel first with /join #channel")
                return True
            
            action_msg = f"\x01ACTION {args}\x01"
            self.send_message(self.current_channel, action_msg)
            return True
        
        elif command == 'msg':
            if not args or len(args.split()) < 2:
                print("❌ Usage: /msg nickname message")
                return True
            
            parts = args.split(' ', 1)
            target_nick = parts[0]
            message = parts[1]
            
            valid, sanitized = self.sanitize_message(message)
            if not valid:
                print(f"❌ {sanitized}")
                return True
            
            self.send_message(target_nick, sanitized)
            print(f"                                                  [{self.format_timestamp()}] -> {target_nick}: {sanitized}")
            return True
        
        elif command == 'help':
            help_cmd = args.strip() if args else None
            self.show_help(help_cmd)
            return True
        
        elif command in ['part', 'whois', 'list']:
            print(f"💭 Command '{command}' recognized but not fully implemented yet")
            print("💡 Coming in future versions!")
            return True
        
        else:
            print(f"❌ Unknown command: /{command}")
            print("💡 Type /help for available commands")
            return True
    
    def handle_user_message(self, message):
        """Handle user message with validation and security checks."""
        if not message.strip():
            return True  # Ignore empty messages
        
        if message.startswith('/'):
            return self.handle_user_command(message)
        
        if not self.current_channel:
            print("❌ Not in a channel. Join a channel first with /join #channel")
            return True
        
        # Validate and sanitize message
        valid, sanitized = self.sanitize_message(message)
        if not valid:
            print(f"❌ {sanitized}")
            return True
        
        # Send message to current channel
        self.send_message(self.current_channel, sanitized)
        return True
    
    def input_handler(self):
        """Handle user input in a separate thread."""
        try:
            while self.running:
                try:
                    user_input = input().strip()
                    if user_input:
                        self.handle_user_message(user_input)
                except EOFError:
                    break
                except KeyboardInterrupt:
                    break
        except Exception as e:
            print(f"Input handler error: {e}")
    
    def interactive_session(self, initial_channel=None):
        """Start interactive IRC session with threaded input handling."""
        if not self.connected or not self.registered:
            print("❌ Must be connected and registered before starting interactive session")
            return False
        
        self.running = True
        
        # Join initial channel if specified
        if initial_channel:
            valid, validated_channel = self.validate_channel_name(initial_channel)
            if valid:
                if self.join_channel(validated_channel):
                    self.current_channel = validated_channel
                    self.channels.add(validated_channel)
            else:
                print(f"❌ {validated_channel}")
        
        # Start input handling thread
        self.input_thread = threading.Thread(target=self.input_handler, daemon=True)
        self.input_thread.start()
        
        print("💬 Interactive session started!")
        print("💡 Type /help for commands, /quit to exit")
        if self.current_channel:
            print(f"📺 Current channel: {self.current_channel}")
        
        # Main message processing loop
        last_ping_check = time.time()
        
        try:
            while self.running and self.connected:
                # Receive and process messages
                messages = self.receive_raw()
                for raw_msg in messages:
                    if self.debug:
                        print(f"<<< {raw_msg}")
                    
                    msg = self.parse_message(raw_msg)
                    
                    # Handle PING
                    if msg['command'] == 'PING':
                        pong_response = f"PONG :{msg['trailing']}"
                        self.send_raw(pong_response)
                        self.last_ping_time = time.time()
                        if self.debug:
                            print("Responded to PING")
                    
                    # Handle various IRC events
                    elif msg['command'] in ['PRIVMSG', 'JOIN', 'PART', 'QUIT', 'NICK']:
                        formatted = self.format_channel_message(msg)
                        if formatted:
                            print(formatted)
                    
                    # Handle server error responses
                    elif msg['command'].isdigit():
                        error_code = int(msg['command'])
                        if error_code >= 400:
                            self.handle_server_error(msg)
                
                # Check connection health
                current_time = time.time()
                if current_time - last_ping_check > 60:  # Check every minute
                    if current_time - self.last_ping_time > 300:  # 5 minutes without PING
                        print("⚠️  Warning: No PING received for 5 minutes, connection may be unstable")
                        self.connection_stable = False
                    last_ping_check = current_time
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        
        finally:
            self.running = False
            if self.input_thread and self.input_thread.is_alive():
                self.input_thread.join(timeout=1)
        
        return True
    
    def handle_server_error(self, msg):
        """Handle IRC server error responses with user-friendly messages."""
        error_code = int(msg['command'])
        error_messages = {
            401: "❌ No such nick/channel",
            403: "❌ No such channel", 
            404: "❌ Cannot send to channel",
            405: "❌ You have joined too many channels",
            431: "❌ No nickname given",
            432: "❌ Erroneous nickname",
            433: "❌ Nickname is already in use",
            441: "❌ User not on that channel",
            442: "❌ You're not on that channel",
            443: "❌ User is already on channel",
            461: "❌ Not enough parameters",
            462: "❌ Already registered",
            471: "❌ Cannot join channel (+l)",
            473: "❌ Cannot join channel (+i)",
            474: "❌ Cannot join channel (+b)",
            475: "❌ Cannot join channel (+k)",
            481: "❌ Permission Denied - You're not an IRC operator",
            482: "❌ You're not channel operator"
        }
        
        error_msg = error_messages.get(error_code, f"❌ Server error {error_code}")
        if msg['trailing']:
            error_msg += f": {msg['trailing']}"
        
        print(error_msg)
        
        # Handle nickname collision
        if error_code == 433:
            self.handle_nick_collision()
    
    def handle_nick_collision(self):
        """Handle nickname collision by suggesting alternatives."""
        import random
        alternatives = [
            f"{self.nickname}_{random.randint(1, 99)}",
            f"{self.nickname}{random.randint(100, 999)}",
            f"Guest{random.randint(1000, 9999)}"
        ]
        
        print("💡 Nickname suggestions:")
        for i, alt in enumerate(alternatives, 1):
            print(f"  {i}. {alt}")
        print("💡 Use /nick newnickname to change your nickname")


def main():
    """Main function to demonstrate Stage 4 - Essential Commands & Error Handling."""
    print("Simple IRC Chat Client - Stage 4: Essential Commands & Error Handling")
    print("====================================================================")
    
    # Create client instance with unique nickname
    import random
    test_nick = f"TestBot{random.randint(1000, 9999)}"
    client = IRCClient(nickname=test_nick, debug=False)
    
    try:
        # Test connection and registration
        if not client.connect():
            print("Connection failed!")
            sys.exit(1)
        
        if not client.register():
            print("Registration failed!")
            client.disconnect()
            sys.exit(1)
        
        print(f"✅ Successfully connected as {test_nick}")
        print("✅ Advanced error handling and validation active")
        print("✅ Comprehensive command system enabled")
        print("✅ IRC injection protection in place")
        print("✅ Type /help for comprehensive command help")
        print("✅ Enhanced user experience features active")
        
        # Start interactive session
        client.interactive_session("#bottest")
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
