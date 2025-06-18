#!/usr/bin/env python3
"""
Enhanced IRC Client - Stage 4: Essential Commands & Error Handling
Comprehensive error handling, input validation, and robust command processing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_interactive import InteractiveIRCClient
import re
import time
import random


class RobustIRCClient(InteractiveIRCClient):
    """Enhanced IRC client with comprehensive error handling and validation."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_capabilities = {}
        self.channel_users = {}  # Track users in channels
        self.last_ping_time = time.time()
        self.connection_stable = True
        
        # IRC command validation patterns
        self.nick_pattern = re.compile(r'^[a-zA-Z\[\]\\`_^{|}][a-zA-Z0-9\[\]\\`_^{|}-]*$')
        self.channel_pattern = re.compile(r'^#[^\x00\x07\x0A\x0D ,:]{1,49}$')
    
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
            
            # Remove IRC command injection attempts
            if sanitized.startswith('/') and not self.is_valid_user_command(sanitized):
                # If it starts with / but isn't a valid user command, treat as message
                pass
            
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
    
    def handle_server_error(self, msg):
        """Handle server error responses with user-friendly messages."""
        error_code = msg['command']
        error_msg = msg['trailing']
        
        error_messages = {
            '401': "No such nick/channel",
            '403': "No such channel", 
            '404': "Cannot send to channel",
            '405': "You have joined too many channels",
            '431': "No nickname given",
            '432': "Invalid nickname",
            '433': "Nickname is already in use",
            '436': "Nickname collision",
            '441': "User not in that channel",
            '442': "You're not on that channel",
            '443': "User is already on channel",
            '451': "You have not registered",
            '461': "Not enough parameters",
            '462': "You may not register",
            '464': "Password incorrect",
            '465': "You are banned from this server",
            '471': "Channel is full",
            '473': "Channel is invite only",
            '474': "You are banned from channel",
            '475': "Bad channel key",
            '476': "Bad channel mask",
            '477': "Channel doesn't support modes",
            '478': "Channel list is full",
            '482': "You're not channel operator",
            '483': "You can't kill a server",
            '484': "Your connection is restricted",
            '485': "You're not the original channel operator"
        }
        
        user_friendly = error_messages.get(error_code, f"Server error ({error_code})")
        print(f"❌ Error: {user_friendly} - {error_msg}")
        
        # Handle specific error recovery
        if error_code == '433':  # Nickname in use
            return self.handle_nick_collision()
        elif error_code in ['403', '405', '471', '473', '474', '475']:  # Channel join errors
            print("💡 Tip: Try a different channel or check channel requirements")
        elif error_code == '404':  # Cannot send to channel
            print("💡 Tip: Make sure you've joined the channel first")
        
        return True
    
    def handle_nick_collision(self):
        """Handle nickname collision with intelligent fallback."""
        base_nick = self.nickname.rstrip('_')
        
        # Try adding numbers
        for i in range(1, 100):
            new_nick = f"{base_nick}{i}"
            if self.validate_nickname(new_nick)[0]:
                print(f"🔄 Trying nickname: {new_nick}")
                self.send_raw(f"NICK {new_nick}")
                self.nickname = new_nick
                return True
        
        # If numbers don't work, try underscores
        new_nick = base_nick + "_"
        if self.validate_nickname(new_nick)[0]:
            print(f"🔄 Trying nickname: {new_nick}")
            self.send_raw(f"NICK {new_nick}")
            self.nickname = new_nick
            return True
        
        print("❌ Could not find available nickname")
        return False
    
    def parse_user_input(self, user_input):
        """Enhanced user input parsing with comprehensive validation."""
        user_input = user_input.strip()
        
        if not user_input:
            return True
        
        # Handle commands
        if user_input.startswith('/'):
            return self.handle_user_command(user_input)
        else:
            # Handle regular messages
            return self.handle_user_message(user_input)
    
    def handle_user_command(self, command_input):
        """Handle user commands with comprehensive validation."""
        parts = command_input[1:].split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        try:
            if command == 'quit':
                return self.cmd_quit(args)
            elif command == 'join':
                return self.cmd_join(args)
            elif command == 'part':
                return self.cmd_part(args)
            elif command == 'nick':
                return self.cmd_nick(args)
            elif command == 'help':
                return self.cmd_help(args)
            elif command == 'me':
                return self.cmd_me(args)
            elif command == 'msg' or command == 'privmsg':
                return self.cmd_msg(args)
            elif command == 'whois':
                return self.cmd_whois(args)
            elif command == 'list':
                return self.cmd_list(args)
            else:
                print(f"❌ Unknown command: /{command}")
                print("💡 Type /help for available commands")
                return True
                
        except Exception as e:
            print(f"❌ Error executing command /{command}: {e}")
            self.log_debug(f"Command error: {e}")
            return True
    
    def cmd_quit(self, args):
        """Handle /quit command with validation."""
        quit_message = args.strip() if args else "Goodbye!"
        
        # Validate quit message
        valid, sanitized = self.sanitize_message(quit_message)
        if not valid:
            print(f"❌ Invalid quit message: {sanitized}")
            return True
        
        print(f"🔌 Quitting with message: {sanitized}")
        self.send_raw(f"QUIT :{sanitized}")
        return False
    
    def cmd_join(self, args):
        """Handle /join command with validation."""
        if not args:
            print("❌ Usage: /join #channel")
            return True
        
        channel = args.strip().split()[0]  # Take first argument only
        valid, validated_channel = self.validate_channel_name(channel)
        
        if not valid:
            print(f"❌ {validated_channel}")
            return True
        
        print(f"🔗 Joining {validated_channel}...")
        if self.join_channel(validated_channel):
            print(f"✅ Successfully joined {validated_channel}")
        else:
            print(f"❌ Failed to join {validated_channel}")
        
        return True
    
    def cmd_part(self, args):
        """Handle /part command to leave channels."""
        if args:
            channel = args.strip().split()[0]
            valid, validated_channel = self.validate_channel_name(channel)
            if not valid:
                print(f"❌ {validated_channel}")
                return True
        else:
            validated_channel = self.current_channel
        
        if not validated_channel:
            print("❌ No channel specified and not currently in a channel")
            print("💡 Usage: /part #channel")
            return True
        
        print(f"👋 Leaving {validated_channel}...")
        self.send_raw(f"PART {validated_channel}")
        
        if validated_channel == self.current_channel:
            self.current_channel = None
        
        if validated_channel in self.channels:
            self.channels.remove(validated_channel)
        
        return True
    
    def cmd_nick(self, args):
        """Handle /nick command with validation."""
        if not args:
            print("❌ Usage: /nick newnickname")
            return True
        
        new_nick = args.strip().split()[0]  # Take first argument only
        valid, error_msg = self.validate_nickname(new_nick)
        
        if not valid:
            print(f"❌ {error_msg}")
            return True
        
        print(f"🏷️  Changing nickname to {new_nick}...")
        self.send_raw(f"NICK {new_nick}")
        self.nickname = new_nick
        return True
    
    def cmd_help(self, args):
        """Handle /help command with detailed information."""
        if args:
            # Help for specific command
            cmd = args.strip().lower()
            help_text = {
                'quit': '/quit [message] - Disconnect from server with optional quit message',
                'join': '/join #channel - Join a channel',
                'part': '/part [#channel] - Leave current channel or specified channel',
                'nick': '/nick nickname - Change your nickname',
                'me': '/me action - Send an action message (* nickname action)',
                'msg': '/msg nickname message - Send private message to user',
                'whois': '/whois nickname - Get information about a user',
                'list': '/list [pattern] - List channels (use with caution on large networks)',
                'help': '/help [command] - Show help for all commands or specific command'
            }
            
            if cmd in help_text:
                print(f"📖 {help_text[cmd]}")
            else:
                print(f"❌ No help available for '{cmd}'")
                print("💡 Type /help to see all available commands")
        else:
            # General help
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
        
        return True
    
    def cmd_me(self, args):
        """Handle /me command with validation."""
        if not args:
            print("❌ Usage: /me action")
            print("💡 Example: /me waves hello")
            return True
        
        if not self.current_channel:
            print("❌ You must be in a channel to use /me")
            print("💡 Use /join #channel first")
            return True
        
        valid, sanitized = self.sanitize_message(args)
        if not valid:
            print(f"❌ Invalid action: {sanitized}")
            return True
        
        action_message = f"\x01ACTION {sanitized}\x01"
        self.send_message(self.current_channel, action_message)
        
        # Show our own action
        timestamp = self.format_timestamp()
        print(f"\r{' ' * 50}\r[{timestamp}] * {self.nickname} {sanitized}")
        print(self.input_prompt, end='', flush=True)
        
        return True
    
    def cmd_msg(self, args):
        """Handle /msg command for private messages."""
        if not args:
            print("❌ Usage: /msg nickname message")
            return True
        
        parts = args.split(' ', 1)
        if len(parts) < 2:
            print("❌ Usage: /msg nickname message")
            return True
        
        target_nick = parts[0]
        message = parts[1]
        
        # Validate nickname format
        valid, error_msg = self.validate_nickname(target_nick)
        if not valid:
            print(f"❌ Invalid target nickname: {error_msg}")
            return True
        
        # Validate message
        valid, sanitized = self.sanitize_message(message)
        if not valid:
            print(f"❌ Invalid message: {sanitized}")
            return True
        
        self.send_raw(f"PRIVMSG {target_nick} :{sanitized}")
        
        # Show our own private message
        timestamp = self.format_timestamp()
        print(f"\r{' ' * 50}\r[{timestamp}] -> {target_nick}: {sanitized}")
        print(self.input_prompt, end='', flush=True)
        
        return True
    
    def cmd_whois(self, args):
        """Handle /whois command to get user information."""
        if not args:
            print("❌ Usage: /whois nickname")
            return True
        
        target_nick = args.strip().split()[0]
        valid, error_msg = self.validate_nickname(target_nick)
        if not valid:
            print(f"❌ Invalid nickname: {error_msg}")
            return True
        
        print(f"🔍 Getting information for {target_nick}...")
        self.send_raw(f"WHOIS {target_nick}")
        return True
    
    def cmd_list(self, args):
        """Handle /list command to list channels."""
        print("📋 Requesting channel list...")
        print("⚠️  Warning: This may produce a lot of output on large networks")
        
        if args:
            self.send_raw(f"LIST {args.strip()}")
        else:
            self.send_raw("LIST")
        
        return True
    
    def handle_user_message(self, message):
        """Handle regular user messages with validation."""
        if not self.current_channel:
            print("❌ You must join a channel first")
            print("💡 Use /join #channel to join a channel")
            return True
        
        valid, sanitized = self.sanitize_message(message)
        if not valid:
            print(f"❌ Invalid message: {sanitized}")
            return True
        
        self.send_message(self.current_channel, sanitized)
        
        # Show our own message
        timestamp = self.format_timestamp()
        print(f"\r{' ' * 50}\r[{timestamp}] <{self.nickname}> {sanitized}")
        print(self.input_prompt, end='', flush=True)
        
        return True
    
    def _message_receiver(self):
        """Enhanced message receiver with error handling."""
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
                        self.last_ping_time = time.time()
                        self.log_debug("Auto-responded to PING")
                        continue
                    
                    # Handle server error responses
                    elif msg['command'].isdigit() and msg['command'].startswith('4'):
                        self.handle_server_error(msg)
                        continue
                    
                    # Handle nickname change confirmations
                    elif msg['command'] == 'NICK' and msg['nick'] == self.nickname:
                        new_nick = msg['trailing'] or (msg['params'][0] if msg['params'] else "")
                        if new_nick:
                            print(f"\r{' ' * 50}\r✅ Nickname changed to {new_nick}")
                            self.nickname = new_nick
                            print(self.input_prompt, end='', flush=True)
                        continue
                    
                    # Handle private messages
                    elif msg['command'] == 'PRIVMSG' and msg['params'] and msg['params'][0] == self.nickname:
                        sender = msg['nick']
                        message_text = msg['trailing']
                        timestamp = self.format_timestamp()
                        print(f"\r{' ' * 50}\r[{timestamp}] <{sender}> {message_text}")
                        print(self.input_prompt, end='', flush=True)
                        continue
                    
                    # Format and display channel messages
                    elif msg['command'] in ['PRIVMSG', 'JOIN', 'PART', 'QUIT']:
                        formatted = self.format_channel_message(msg)
                        if formatted:
                            print(f"\r{' ' * 50}\r{formatted}")
                            print(self.input_prompt, end='', flush=True)
                    
                    # Handle other server messages
                    elif msg['command'].isdigit():
                        # Handle specific numeric responses
                        if msg['command'] in ['311', '312', '313', '317', '318', '319']:  # WHOIS responses
                            info = msg['trailing']
                            print(f"\r{' ' * 50}\r🔍 {info}")
                            print(self.input_prompt, end='', flush=True)
                        elif msg['command'] == '322':  # LIST response
                            if len(msg['params']) >= 3:
                                channel = msg['params'][1]
                                user_count = msg['params'][2]
                                topic = msg['trailing']
                                print(f"\r{' ' * 50}\r📋 {channel} ({user_count} users): {topic}")
                                print(self.input_prompt, end='', flush=True)
                
                time.sleep(0.1)
                
            except Exception as e:
                if self.running:
                    print(f"\r{' ' * 50}\r❌ Receiver error: {e}")
                    print(self.input_prompt, end='', flush=True)
                    self.log_debug(f"Receiver thread error: {e}")
                time.sleep(1)


def main():
    """Test Stage 4 - Enhanced IRC client with error handling."""
    print("Enhanced IRC Chat Client - Stage 4 Test")
    print("=======================================")
    
    # Create enhanced client
    test_nick = f"TestBot{random.randint(1000, 9999)}"
    client = RobustIRCClient(nickname=test_nick, debug=False)
    
    try:
        # Connect and register
        if not client.connect():
            print("❌ Connection failed!")
            return
        
        if not client.register():
            print("❌ Registration failed!")
            client.disconnect()
            return
        
        print("✅ Enhanced IRC client ready!")
        print("✅ Type /help for comprehensive command help")
        print("✅ Enhanced error handling and validation active")
        
        # Start interactive session
        client.interactive_session("#bottest")
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
