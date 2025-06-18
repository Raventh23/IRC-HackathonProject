#!/usr/bin/env python3
"""
Enhanced IRC Client - Stage 5: Polish & Stability
Connection reliability, enhanced UX, and configuration support.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.irc_client import IRCClient
import argparse
import time
import json
import signal
import threading
from datetime import datetime, timedelta


class StableIRCClient(IRCClient):
    """Enhanced IRC client with connection reliability and improved UX."""
    
    def __init__(self, *args, **kwargs):
        # Extract new Stage 5 parameters
        self.auto_reconnect = kwargs.pop('auto_reconnect', False)
        self.reconnect_delay = kwargs.pop('reconnect_delay', 30)
        self.max_reconnect_attempts = kwargs.pop('max_reconnect_attempts', 5)
        self.connection_timeout = kwargs.pop('connection_timeout', 60)
        self.show_status_messages = kwargs.pop('show_status_messages', True)
        self.config_file = kwargs.pop('config_file', None)
        
        super().__init__(*args, **kwargs)
        
        # Stage 5 enhancements
        self.reconnect_attempts = 0
        self.last_activity_time = time.time()
        self.connection_start_time = None
        self.total_messages_sent = 0
        self.total_messages_received = 0
        self.uptime_start = None
        self.status_thread = None
        self.monitoring_enabled = True
        
        # Load configuration if provided
        if self.config_file:
            self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
            # Apply configuration settings
            self.server = config.get('server', self.server)
            self.port = config.get('port', self.port)
            self.nickname = config.get('nickname', self.nickname)
            self.username = config.get('username', self.username)
            self.realname = config.get('realname', self.realname)
            self.auto_reconnect = config.get('auto_reconnect', self.auto_reconnect)
            self.reconnect_delay = config.get('reconnect_delay', self.reconnect_delay)
            self.show_status_messages = config.get('show_status_messages', self.show_status_messages)
            
            if self.show_status_messages:
                print(f"📋 Configuration loaded from {self.config_file}")
                
        except FileNotFoundError:
            print(f"⚠️  Configuration file {self.config_file} not found, using defaults")
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing configuration file: {e}")
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
    
    def save_config(self, filename=None):
        """Save current configuration to JSON file."""
        if not filename:
            filename = self.config_file or "irc_config.json"
        
        config = {
            'server': self.server,
            'port': self.port,
            'nickname': self.nickname,
            'username': self.username,
            'realname': self.realname,
            'auto_reconnect': self.auto_reconnect,
            'reconnect_delay': self.reconnect_delay,
            'show_status_messages': self.show_status_messages
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"💾 Configuration saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
    
    def enhanced_connect(self):
        """Enhanced connection with retry logic and monitoring."""
        attempt = 0
        while attempt <= self.max_reconnect_attempts:
            if attempt > 0:
                if self.show_status_messages:
                    print(f"🔄 Reconnection attempt {attempt}/{self.max_reconnect_attempts}")
                time.sleep(self.reconnect_delay)
            
            try:
                if self.connect():
                    self.connection_start_time = time.time()
                    self.uptime_start = time.time()
                    self.reconnect_attempts = 0
                    if self.show_status_messages:
                        print(f"✅ Connected to {self.server}:{self.port}")
                    return True
                    
            except Exception as e:
                if self.show_status_messages:
                    print(f"❌ Connection attempt {attempt + 1} failed: {e}")
            
            attempt += 1
        
        print(f"❌ Failed to connect after {self.max_reconnect_attempts} attempts")
        return False
    
    def enhanced_register(self):
        """Enhanced registration with better error handling."""
        try:
            if self.register():
                if self.show_status_messages:
                    print(f"✅ Successfully registered as {self.nickname}")
                return True
            else:
                print("❌ Registration failed")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
    
    def monitor_connection_health(self):
        """Monitor connection health in background thread."""
        while self.running and self.monitoring_enabled:
            try:
                current_time = time.time()
                
                # Check for PING timeout
                if current_time - self.last_ping_time > 300:  # 5 minutes
                    if self.show_status_messages:
                        print("⚠️  Connection may be unstable (no PING in 5 minutes)")
                    self.connection_stable = False
                    
                    # Attempt to send PING to server
                    try:
                        self.send_raw("PING :keepalive")
                        if self.debug:
                            print("Sent keepalive PING")
                    except:
                        if self.auto_reconnect:
                            self.handle_disconnection()
                            break
                
                # Update activity time
                self.last_activity_time = current_time
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                if self.debug:
                    print(f"Connection monitor error: {e}")
                time.sleep(30)
    
    def handle_disconnection(self):
        """Handle unexpected disconnection with auto-reconnect."""
        if self.show_status_messages:
            print("🔌 Connection lost! Attempting to reconnect...")
        
        self.connected = False
        self.registered = False
        
        if self.auto_reconnect and self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            if self.enhanced_connect() and self.enhanced_register():
                # Rejoin channels
                channels_to_rejoin = list(self.channels)
                for channel in channels_to_rejoin:
                    if self.join_channel(channel):
                        if self.show_status_messages:
                            print(f"🔄 Rejoined {channel}")
                    time.sleep(1)  # Avoid flooding
                
                if self.show_status_messages:
                    print("✅ Successfully reconnected and rejoined channels")
                return True
        
        print("❌ Unable to reconnect")
        return False
    
    def format_enhanced_message(self, msg):
        """Enhanced message formatting with better visual organization."""
        if not msg or 'command' not in msg:
            return None
        
        timestamp = self.format_timestamp()
        
        if msg['command'] == 'PRIVMSG':
            channel = msg['params'][0] if msg['params'] else ""
            message_text = msg['trailing']
            nick = msg['nick']
            
            # Handle ACTION messages
            if message_text.startswith('\x01ACTION ') and message_text.endswith('\x01'):
                action_text = message_text[8:-1]  # Remove \x01ACTION and \x01
                return f"                                        [{timestamp}] * {nick} {action_text}"
            
            # Regular messages with enhanced formatting
            if channel == self.current_channel:
                return f"                                        [{timestamp}] <{nick}> {message_text}"
            else:
                return f"                                        [{timestamp}] [{channel}] <{nick}> {message_text}"
        
        elif msg['command'] == 'JOIN':
            channel = msg['params'][0] if msg['params'] else msg['trailing']
            nick = msg['nick']
            if nick != self.nickname:
                return f"                                        [{timestamp}] → {nick} joined {channel}"
        
        elif msg['command'] == 'PART':
            channel = msg['params'][0] if msg['params'] else ""
            nick = msg['nick']
            part_msg = msg['trailing'] if msg['trailing'] else ""
            if nick != self.nickname:
                if part_msg:
                    return f"                                        [{timestamp}] ← {nick} left {channel} ({part_msg})"
                else:
                    return f"                                        [{timestamp}] ← {nick} left {channel}"
        
        elif msg['command'] == 'QUIT':
            nick = msg['nick']
            quit_msg = msg['trailing'] if msg['trailing'] else ""
            if nick != self.nickname:
                if quit_msg:
                    return f"                                        [{timestamp}] ⚡ {nick} quit ({quit_msg})"
                else:
                    return f"                                        [{timestamp}] ⚡ {nick} quit"
        
        elif msg['command'] == 'NICK':
            old_nick = msg['nick']
            new_nick = msg['trailing']
            return f"                                        [{timestamp}] 🏷️  {old_nick} is now known as {new_nick}"
        
        return None
    
    def show_status(self):
        """Show current connection and session status."""
        if not self.uptime_start:
            print("📊 IRC Client Status: Not connected")
            return
        
        uptime = time.time() - self.uptime_start
        uptime_str = str(timedelta(seconds=int(uptime)))
        
        print("📊 IRC Client Status:")
        print(f"   🌐 Server: {self.server}:{self.port}")
        print(f"   👤 Nickname: {self.nickname}")
        print(f"   📺 Current Channel: {self.current_channel or 'None'}")
        print(f"   📱 Joined Channels: {', '.join(self.channels) if self.channels else 'None'}")
        print(f"   ⏱️  Uptime: {uptime_str}")
        print(f"   📤 Messages Sent: {self.total_messages_sent}")
        print(f"   📥 Messages Received: {self.total_messages_received}")
        print(f"   🔗 Connection: {'Stable' if self.connection_stable else 'Unstable'}")
        print(f"   🔄 Auto-reconnect: {'Enabled' if self.auto_reconnect else 'Disabled'}")
    
    def enhanced_send_message(self, target, message):
        """Enhanced message sending with statistics tracking."""
        result = self.send_message(target, message)
        if result:
            self.total_messages_sent += 1
        return result
    
    def enhanced_interactive_session(self, initial_channel=None):
        """Enhanced interactive session with improved UX and monitoring."""
        if not self.connected or not self.registered:
            print("❌ Must be connected and registered before starting interactive session")
            return False
        
        self.running = True
        self.monitoring_enabled = True
        
        # Join initial channel if specified
        if initial_channel:
            valid, validated_channel = self.validate_channel_name(initial_channel)
            if valid:
                if self.join_channel(validated_channel):
                    self.current_channel = validated_channel
                    self.channels.add(validated_channel)
                    if self.show_status_messages:
                        print(f"✅ Joined {validated_channel}")
            else:
                print(f"❌ {validated_channel}")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_connection_health, daemon=True)
        monitor_thread.start()
        
        # Start input handling thread
        self.input_thread = threading.Thread(target=self.input_handler, daemon=True)
        self.input_thread.start()
        
        # Show enhanced startup message
        print("🚀 Enhanced IRC Client - Stage 5: Polish & Stability")
        print("====================================================")
        print("💬 Interactive session started with enhanced features!")
        print("✨ New Stage 5 features:")
        print("   🔄 Connection monitoring and auto-reconnect")
        print("   📊 Session statistics and status reporting")
        print("   🎨 Enhanced message formatting")
        print("   ⚙️  Configuration file support")
        print()
        print("💡 Enhanced commands:")
        print("   /status    - Show connection and session status")
        print("   /config    - Manage configuration settings")
        print("   /uptime    - Show session uptime")
        print("   /stats     - Show session statistics")
        print("   /reconnect - Manually reconnect to server")
        print("   /help      - Show all available commands")
        print()
        if self.current_channel:
            print(f"📺 Current channel: {self.current_channel}")
        print("🔗 Connection monitoring active")
        if self.auto_reconnect:
            print("🔄 Auto-reconnect enabled")
        print()
        
        # Main message processing loop with enhanced error handling
        last_ping_check = time.time()
        
        try:
            while self.running and self.connected:
                # Receive and process messages
                messages = self.receive_raw()
                for raw_msg in messages:
                    if self.debug:
                        print(f"<<< {raw_msg}")
                    
                    msg = self.parse_message(raw_msg)
                    self.total_messages_received += 1
                    
                    # Handle PING
                    if msg['command'] == 'PING':
                        pong_response = f"PONG :{msg['trailing']}"
                        self.send_raw(pong_response)
                        self.last_ping_time = time.time()
                        if self.debug:
                            print("Responded to PING")
                    
                    # Handle various IRC events with enhanced formatting
                    elif msg['command'] in ['PRIVMSG', 'JOIN', 'PART', 'QUIT', 'NICK']:
                        formatted = self.format_enhanced_message(msg)
                        if formatted:
                            print(formatted)
                    
                    # Handle server error responses
                    elif msg['command'].isdigit():
                        error_code = int(msg['command'])
                        if error_code >= 400:
                            self.handle_server_error(msg)
                
                # Enhanced connection health check
                current_time = time.time()
                if current_time - last_ping_check > 60:  # Check every minute
                    if current_time - self.last_ping_time > 300:  # 5 minutes without PING
                        if not self.connection_stable:
                            print("⚠️  Connection unstable - consider reconnecting with /reconnect")
                    last_ping_check = current_time
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
        
        except KeyboardInterrupt:
            print("\n👋 Shutting down gracefully...")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            if self.auto_reconnect:
                self.handle_disconnection()
        
        finally:
            self.running = False
            self.monitoring_enabled = False
            if self.input_thread and self.input_thread.is_alive():
                self.input_thread.join(timeout=1)
            
            if self.show_status_messages:
                self.show_final_stats()
        
        return True
    
    def show_final_stats(self):
        """Show final session statistics."""
        if self.uptime_start:
            uptime = time.time() - self.uptime_start
            uptime_str = str(timedelta(seconds=int(uptime)))
            print(f"\n📊 Session Summary:")
            print(f"   ⏱️  Total uptime: {uptime_str}")
            print(f"   📤 Messages sent: {self.total_messages_sent}")
            print(f"   📥 Messages received: {self.total_messages_received}")
            print(f"   🔄 Reconnection attempts: {self.reconnect_attempts}")
    
    def handle_enhanced_user_command(self, command_input):
        """Handle enhanced user commands including Stage 5 features."""
        if not command_input.startswith('/'):
            return False
        
        # Parse command and arguments
        parts = command_input[1:].split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Handle Stage 5 enhanced commands
        if command == 'status':
            self.show_status()
            return True
        
        elif command == 'uptime':
            if self.uptime_start:
                uptime = time.time() - self.uptime_start
                uptime_str = str(timedelta(seconds=int(uptime)))
                print(f"⏱️  Session uptime: {uptime_str}")
            else:
                print("❌ No uptime information available")
            return True
        
        elif command == 'stats':
            print(f"📊 Session Statistics:")
            print(f"   📤 Messages sent: {self.total_messages_sent}")
            print(f"   📥 Messages received: {self.total_messages_received}")
            print(f"   🔄 Reconnection attempts: {self.reconnect_attempts}")
            if self.uptime_start:
                uptime = time.time() - self.uptime_start
                uptime_str = str(timedelta(seconds=int(uptime)))
                print(f"   ⏱️  Uptime: {uptime_str}")
            return True
        
        elif command == 'reconnect':
            if self.connected:
                print("🔄 Manually reconnecting...")
                self.disconnect()
                time.sleep(2)
                if self.enhanced_connect() and self.enhanced_register():
                    print("✅ Reconnection successful")
                    # Rejoin channels
                    channels_to_rejoin = list(self.channels)
                    for channel in channels_to_rejoin:
                        self.join_channel(channel)
                        time.sleep(1)
                else:
                    print("❌ Reconnection failed")
            else:
                print("❌ Not currently connected")
            return True
        
        elif command == 'config':
            if args.strip():
                subcommand = args.strip().split()[0].lower()
                if subcommand == 'save':
                    filename = args.strip().split()[1] if len(args.strip().split()) > 1 else None
                    self.save_config(filename)
                elif subcommand == 'show':
                    print("⚙️  Current Configuration:")
                    print(f"   🌐 Server: {self.server}:{self.port}")
                    print(f"   👤 Nickname: {self.nickname}")
                    print(f"   🔄 Auto-reconnect: {self.auto_reconnect}")
                    print(f"   ⏰ Reconnect delay: {self.reconnect_delay}s")
                    print(f"   📢 Status messages: {self.show_status_messages}")
                elif subcommand == 'toggle':
                    setting = args.strip().split()[1] if len(args.strip().split()) > 1 else None
                    if setting == 'reconnect':
                        self.auto_reconnect = not self.auto_reconnect
                        print(f"🔄 Auto-reconnect: {'Enabled' if self.auto_reconnect else 'Disabled'}")
                    elif setting == 'status':
                        self.show_status_messages = not self.show_status_messages
                        print(f"📢 Status messages: {'Enabled' if self.show_status_messages else 'Disabled'}")
                    else:
                        print("❌ Usage: /config toggle [reconnect|status]")
                else:
                    print("❌ Usage: /config [save|show|toggle]")
            else:
                print("⚙️  Configuration commands:")
                print("   /config show              - Show current settings")
                print("   /config save [filename]   - Save configuration")
                print("   /config toggle reconnect  - Toggle auto-reconnect")
                print("   /config toggle status     - Toggle status messages")
            return True
        
        # Fall back to parent class command handling
        return self.handle_user_command(command_input)
    
    def handle_user_message(self, message):
        """Override to use enhanced command handling."""
        if not message.strip():
            return True  # Ignore empty messages
        
        if message.startswith('/'):
            return self.handle_enhanced_user_command(message)
        
        if not self.current_channel:
            print("❌ Not in a channel. Join a channel first with /join #channel")
            return True
        
        # Validate and sanitize message
        valid, sanitized = self.sanitize_message(message)
        if not valid:
            print(f"❌ {sanitized}")
            return True
        
        # Send message to current channel with enhanced tracking
        self.enhanced_send_message(self.current_channel, sanitized)
        return True


def parse_arguments():
    """Parse command line arguments for Stage 5 configuration."""
    parser = argparse.ArgumentParser(
        description="Enhanced IRC Chat Client - Stage 5: Polish & Stability",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_stage5.py                           # Connect with defaults
  python test_stage5.py -s irc.freenode.net      # Connect to different server
  python test_stage5.py -n MyNick -c config.json # Use custom nick and config
  python test_stage5.py --auto-reconnect         # Enable auto-reconnect
  python test_stage5.py --debug                  # Enable debug mode
        """
    )
    
    parser.add_argument('-s', '--server', default='irc.libera.chat',
                        help='IRC server to connect to (default: irc.libera.chat)')
    parser.add_argument('-p', '--port', type=int, default=6667,
                        help='IRC server port (default: 6667)')
    parser.add_argument('-n', '--nickname',
                        help='Nickname to use (default: auto-generated)')
    parser.add_argument('-u', '--username', default='simple',
                        help='Username (default: simple)')
    parser.add_argument('-r', '--realname', default='Simple IRC Client',
                        help='Real name (default: Simple IRC Client)')
    parser.add_argument('-c', '--config',
                        help='Configuration file to load/save')
    parser.add_argument('--channel',
                        help='Initial channel to join (default: #bottest)')
    parser.add_argument('--auto-reconnect', action='store_true',
                        help='Enable automatic reconnection')
    parser.add_argument('--reconnect-delay', type=int, default=30,
                        help='Delay between reconnection attempts (default: 30s)')
    parser.add_argument('--max-reconnect', type=int, default=5,
                        help='Maximum reconnection attempts (default: 5)')
    parser.add_argument('--no-status', action='store_true',
                        help='Disable status messages')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    
    return parser.parse_args()


def main():
    """Main function for Stage 5 - Enhanced IRC Client."""
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n👋 Received interrupt signal, shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parse command line arguments
    args = parse_arguments()
    
    print("🚀 IRC Chat Client - Stage 5: Polish & Stability")
    print("==================================================")
    
    # Generate nickname if not provided
    if not args.nickname:
        import random
        args.nickname = f"StableBot{random.randint(1000, 9999)}"
    
    # Create enhanced client with Stage 5 features
    client = StableIRCClient(
        server=args.server,
        port=args.port,
        nickname=args.nickname,
        username=args.username,
        realname=args.realname,
        debug=args.debug,
        auto_reconnect=args.auto_reconnect,
        reconnect_delay=args.reconnect_delay,
        max_reconnect_attempts=args.max_reconnect,
        show_status_messages=not args.no_status,
        config_file=args.config
    )
    
    try:
        # Enhanced connection process
        print(f"🌐 Connecting to {args.server}:{args.port}...")
        if not client.enhanced_connect():
            print("❌ Failed to establish connection")
            sys.exit(1)
        
        print(f"🔐 Registering as {args.nickname}...")
        if not client.enhanced_register():
            print("❌ Failed to register with server")
            client.disconnect()
            sys.exit(1)
        
        # Show enhanced startup information
        print("✅ Stage 5 Enhanced Features Active:")
        print(f"   🔄 Auto-reconnect: {'Enabled' if client.auto_reconnect else 'Disabled'}")
        print(f"   📊 Status monitoring: {'Enabled' if client.show_status_messages else 'Disabled'}")
        print(f"   ⚙️  Configuration: {'Loaded' if client.config_file else 'Default'}")
        print(f"   🎨 Enhanced formatting: Enabled")
        print()
        
        # Start enhanced interactive session
        initial_channel = args.channel or "#bottest"
        client.enhanced_interactive_session(initial_channel)
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        if client.connected:
            client.disconnect()


if __name__ == "__main__":
    main()
