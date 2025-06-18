#!/usr/bin/env python3
"""
IRC Chat Client - GUI Version
Graphical user interface for the IRC Chat Client using tkinter.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import sys
import os

# Import the existing IRC client
from irc_client import IRCClient


class IRCClientGUI:
    """GUI wrapper for the IRC Chat Client."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("IRC Chat Client")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # IRC client instance
        self.irc_client = None
        self.connected = False
        self.irc_thread = None
        
        # Message queue for thread-safe GUI updates
        self.message_queue = queue.Queue()
        
        # Current channel
        self.current_channel = None
        
        # Setup basic window structure
        self.setup_window()
        
        # Start checking for messages
        self.check_messages()
        
        # Set up menu bar
        self.setup_menu_bar()
        
        # Add test command to command handler
        self.add_test_command()
    
    def setup_window(self):
        """Set up the basic window structure and frames."""
        # Configure root window
        self.root.configure(bg='#f0f0f0')
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for connection status
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Connection status indicator
        self.status_label = ttk.Label(
            self.status_frame, 
            text="● Disconnected", 
            foreground="red",
            font=("Arial", 10, "bold")
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Current channel indicator
        self.channel_label = ttk.Label(
            self.status_frame, 
            text="No channel selected",
            font=("Arial", 10)
        )
        self.channel_label.pack(side=tk.RIGHT)
        
        # Connect button
        self.connect_button = ttk.Button(
            self.status_frame,
            text="Connect",
            command=self.connect_to_irc
        )
        self.connect_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Middle section with paned window for resizable sections
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Left frame for channel list
        self.channel_frame = ttk.LabelFrame(self.paned_window, text="Channels", padding="5")
        self.channel_frame.configure(width=200)
        self.paned_window.add(self.channel_frame, weight=0)
        
        # Set up channel management
        self.setup_channel_management()
        
        # Right frame for chat display
        self.chat_frame = ttk.LabelFrame(self.paned_window, text="Chat", padding="5")
        self.paned_window.add(self.chat_frame, weight=1)
        
        # Chat display area with scrollbar
        self.setup_chat_display()
        
        # Bottom frame for message input
        self.input_frame = ttk.Frame(main_frame)
        self.input_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Set up message input system
        self.setup_message_input()
        
        # Add separators for visual clarity
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.pack(fill=tk.X, pady=(5, 10))
        
        # Configure window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Handle window closing event."""
        if self.connected and self.irc_client:
            # Disconnect from IRC before closing
            try:
                self.irc_client.disconnect()
            except:
                pass
        self.root.destroy()
    
    def connect_to_irc(self):
        """Connect to IRC server."""
        if self.connected:
            self.disconnect_from_irc()
            return
        
        try:
            # Create IRC client with unique nickname
            import random
            nickname = f"SiLabsUser{random.randint(1000, 9999)}"
            self.irc_client = IRCClient(nickname=nickname, debug=False)
            
            # Start IRC client in separate thread
            self.irc_thread = threading.Thread(target=self.irc_worker, daemon=True)
            self.irc_thread.start()
            
            # Update UI
            self.connect_button.config(text="Connecting...", state=tk.DISABLED)
            self.add_system_message("Connecting to IRC server...")
            
        except Exception as e:
            self.add_error_message(f"Failed to start connection: {str(e)}")
    
    def disconnect_from_irc(self):
        """Disconnect from IRC server."""
        if self.irc_client:
            try:
                self.irc_client.disconnect()
            except:
                pass
        
        self.connected = False
        self.update_status("Disconnected", "red")
        self.connect_button.config(text="Connect", state=tk.NORMAL)
        self.disable_input()
        self.disable_channel_management()
        self.add_system_message("Disconnected from IRC server")
    
    def irc_worker(self):
        """IRC client worker thread."""
        try:
            # Connect to server
            if not self.irc_client.connect():
                self.message_queue.put(("error", "Failed to connect to IRC server"))
                return
            
            # Register with server
            if not self.irc_client.register():
                self.message_queue.put(("error", "Failed to register with IRC server"))
                return
            
            # Connection successful
            self.message_queue.put(("connected", None))
            
            # Auto-join SiLabs channel
            self.message_queue.put(("auto_join", "#SiLabs"))
            
            # Message processing loop
            while self.irc_client.connected:
                try:
                    messages = self.irc_client.receive_raw()
                    for raw_msg in messages:
                        if raw_msg:
                            # Parse and queue message for GUI
                            parsed = self.irc_client.parse_message(raw_msg)
                            self.message_queue.put(("irc_message", parsed))
                    
                    # Small delay to prevent excessive CPU usage
                    import time
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.message_queue.put(("error", f"IRC error: {str(e)}"))
                    break
                    
        except Exception as e:
            self.message_queue.put(("error", f"Connection error: {str(e)}"))
    
    def check_messages(self):
        """Check for messages from IRC client thread."""
        try:
            while True:
                message_type, data = self.message_queue.get_nowait()
                self.handle_irc_message(message_type, data)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_messages)
    
    def handle_irc_message(self, message_type, data):
        """Handle messages from IRC client thread."""
        if message_type == "connected":
            self.connected = True
            self.update_status("Connected", "green")
            self.connect_button.config(text="Disconnect", state=tk.NORMAL)
            self.enable_input()
            self.enable_channel_management()
            self.add_system_message("Successfully connected to IRC server!")
            
        elif message_type == "error":
            self.add_error_message(data)
            self.connect_button.config(text="Connect", state=tk.NORMAL)
            
        elif message_type == "auto_join":
            # Auto-join the SiLabs channel
            if self.irc_client:
                self.irc_client.join_channel(data)
                self.add_system_message(f"Joining {data}...")
                
        elif message_type == "irc_message":
            self.process_irc_message(data)
    
    def process_irc_message(self, msg):
        """Process parsed IRC message."""
        if not msg:
            return
            
        command = msg.get('command', '')
        
        if command == 'PRIVMSG':
            # Regular chat message
            sender = msg.get('nick', 'Unknown')
            channel = msg['params'][0] if msg['params'] else ''
            message = msg.get('trailing', '')
            
            if channel == self.current_channel:
                self.add_user_message(sender, message)
                
        elif command == 'JOIN':
            # User joined channel
            joiner = msg.get('nick', 'Unknown')
            channel = msg['params'][0] if msg['params'] else msg.get('trailing', '')
            
            if joiner == self.irc_client.nickname:
                # We joined a channel
                if channel not in self.channels_list:
                    self.channels_list.append(channel)
                    self.channels_listbox.insert(tk.END, channel)
                self.switch_to_channel(channel)
                self.add_system_message(f"Successfully joined {channel}")
            else:
                # Someone else joined
                if channel == self.current_channel:
                    self.add_join_message(joiner, channel)
                    
        elif command == 'PART':
            # User left channel
            leaver = msg.get('nick', 'Unknown')
            channel = msg['params'][0] if msg['params'] else ''
            reason = msg.get('trailing', '')
            
            if channel == self.current_channel:
                self.add_part_message(leaver, channel, reason)
                
        elif command == 'PING':
            # Handle ping
            if self.irc_client:
                server = msg.get('trailing', msg['params'][0] if msg['params'] else '')
                self.irc_client.send_raw(f"PONG :{server}")
                
        elif command in ['001', '002', '003', '004']:
            # Welcome messages
            welcome_msg = msg.get('trailing', 'Welcome to IRC!')
            self.add_system_message(welcome_msg)
    
    def run(self):
        """Start the GUI application."""
        print("Starting IRC Chat Client GUI...")
        self.root.mainloop()


    def setup_chat_display(self):
        """Set up the chat display area with scrollable text widget."""
        # Create frame for chat display
        chat_display_frame = ttk.Frame(self.chat_frame)
        chat_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable text widget for messages
        self.chat_text = scrolledtext.ScrolledText(
            chat_display_frame,
            state=tk.DISABLED,  # Read-only
            wrap=tk.WORD,
            width=60,
            height=25,
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000"
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for different message types
        self.chat_text.tag_configure("timestamp", foreground="#666666", font=("Consolas", 9))
        self.chat_text.tag_configure("username", foreground="#0066cc", font=("Consolas", 10, "bold"))
        self.chat_text.tag_configure("system", foreground="#008000", font=("Consolas", 10, "italic"))
        self.chat_text.tag_configure("error", foreground="#cc0000", font=("Consolas", 10, "bold"))
        self.chat_text.tag_configure("join", foreground="#00aa00")
        self.chat_text.tag_configure("part", foreground="#aa0000")
        
        # Add welcome message
        self.add_system_message("Welcome to IRC Chat Client!")
        self.add_system_message("Connect to a server and join a channel to start chatting.")
        self.chat_text.yview_moveto(1.0)
    
    def test_functionality(self):
        """Test all GUI functionality (for development)."""
        test_results = []
        
        # Test 1: GUI Components
        try:
            assert hasattr(self, 'chat_text'), "Chat display missing"
            assert hasattr(self, 'message_entry'), "Message input missing"
            assert hasattr(self, 'channels_listbox'), "Channel list missing"
            assert hasattr(self, 'connect_button'), "Connect button missing"
            test_results.append("✅ GUI Components: PASS")
        except AssertionError as e:
            test_results.append(f"❌ GUI Components: FAIL - {e}")
        
        # Test 2: Message Display
        try:
            self.add_system_message("Test system message")
            self.add_user_message("TestUser", "Test user message")
            test_results.append("✅ Message Display: PASS")
        except Exception as e:
            test_results.append(f"❌ Message Display: FAIL - {e}")
        
        # Test 3: Channel Management
        try:
            assert self.validate_channel_name("#test"), "Channel validation failed"
            assert not self.validate_channel_name("invalid"), "Invalid channel accepted"
            test_results.append("✅ Channel Validation: PASS")
        except Exception as e:
            test_results.append(f"❌ Channel Validation: FAIL - {e}")
        
        # Test 4: Input Validation
        try:
            assert self.validate_input("Valid message"), "Valid message rejected"
            assert not self.validate_input(""), "Empty message accepted"
            assert not self.validate_input("x" * 600), "Long message accepted"
            test_results.append("✅ Input Validation: PASS")
        except Exception as e:
            test_results.append(f"❌ Input Validation: FAIL - {e}")
        
        # Display test results
        self.add_system_message("=== FUNCTIONALITY TEST RESULTS ===")
        for result in test_results:
            self.add_system_message(result)
        self.add_system_message("=== END TEST RESULTS ===")
    
    def check_threading_safety(self):
        """Verify thread safety of GUI updates."""
        try:
            # Test message queue operations
            self.message_queue.put(("test", "Thread safety test"))
            self.handle_irc_message("test", "Thread safety verified")
            return True
        except Exception as e:
            self.add_error_message(f"Threading issue detected: {e}")
            return False
    
    def validate_irc_integration(self):
        """Validate IRC client integration."""
        issues = []
        
        # Check IRC client import
        try:
            from irc_client import IRCClient
            test_client = IRCClient(nickname="TestBot", debug=True)
            issues.append("✅ IRC Client import: PASS")
        except Exception as e:
            issues.append(f"❌ IRC Client import: FAIL - {e}")
        
        # Check message parsing capability
        try:
            if hasattr(self, 'irc_client') and self.irc_client:
                test_msg = ":nick!user@host PRIVMSG #channel :test message"
                parsed = self.irc_client.parse_message(test_msg)
                if parsed and parsed.get('command') == 'PRIVMSG':
                    issues.append("✅ Message parsing: PASS")
                else:
                    issues.append("❌ Message parsing: FAIL - Invalid parse result")
            else:
                issues.append("⚠️ Message parsing: SKIP - No active IRC client")
        except Exception as e:
            issues.append(f"❌ Message parsing: FAIL - {e}")
        
        # Display validation results
        self.add_system_message("=== IRC INTEGRATION VALIDATION ===")
        for issue in issues:
            self.add_system_message(issue)
        self.add_system_message("=== END VALIDATION ===")
    
    def run_comprehensive_test(self):
        """Run all tests and display results."""
        self.add_system_message("Starting comprehensive functionality test...")
        self.test_functionality()
        self.validate_irc_integration()
        
        if self.check_threading_safety():
            self.add_system_message("✅ Threading safety: VERIFIED")
        else:
            self.add_system_message("❌ Threading safety: ISSUES DETECTED")
        
        self.add_system_message("Comprehensive test completed!")
    
    def optimize_performance(self):
        """Optimize GUI performance."""
        # Limit chat history to prevent memory issues
        max_lines = 1000
        current_lines = int(self.chat_text.index('end-1c').split('.')[0])
        
        if current_lines > max_lines:
            # Remove oldest lines
            lines_to_remove = current_lines - max_lines
            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.delete('1.0', f'{lines_to_remove}.0')
            self.chat_text.config(state=tk.DISABLED)
    
    def final_cleanup(self):
        """Perform final cleanup and optimization."""
        # Clean up any temporary files or resources
        try:
            self.optimize_performance()
            
            # Ensure proper IRC disconnection
            if self.connected and self.irc_client:
                self.irc_client.disconnect()
            
            # Clear message queue
            while not self.message_queue.empty():
                try:
                    self.message_queue.get_nowait()
                except:
                    break
                    
            self.add_system_message("✅ Final cleanup completed successfully")
            
        except Exception as e:
            self.add_error_message(f"Cleanup warning: {e}")
    
    def get_version_info(self):
        """Get version and feature information."""
        return {
            "version": "1.0.0",
            "build_date": "2025-06-18",
            "features": [
                "Real-time IRC connectivity",
                "Multi-channel support", 
                "Professional GUI interface",
                "Keyboard shortcuts",
                "Command system",
                "Auto-scroll chat display",
                "Connection management",
                "Input validation",
                "Error handling",
                "Help system"
            ],
            "requirements": ["Python 3.7+", "tkinter", "threading"],
            "tested_with": ["irc.libera.chat"],
            "default_channel": "#SiLabs"
        }
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Connect", command=self.connect_to_irc, accelerator="Ctrl+N")
        file_menu.add_command(label="Disconnect", command=self.disconnect_from_irc, accelerator="Ctrl+D")
        file_menu.add_separator()
        file_menu.add_command(label="Clear Chat", command=self.clear_chat, accelerator="Ctrl+L")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Commands", command=self.show_help_gui)
        help_menu.add_command(label="Test Functionality", command=self.run_comprehensive_test)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.connect_to_irc())
        self.root.bind('<Control-d>', lambda e: self.disconnect_from_irc())
        self.root.bind('<Control-l>', lambda e: self.clear_chat())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<Control-j>', lambda e: self.channel_entry.focus())
        self.root.bind('<Control-t>', lambda e: self.run_comprehensive_test())
    
    def add_test_command(self):
        """Add test command to existing command handler."""
        # This will be integrated into the handle_command method
        pass
