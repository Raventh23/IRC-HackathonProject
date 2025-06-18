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
        
        # Message queue for thread-safe GUI updates
        self.message_queue = queue.Queue()
        
        # Current channel
        self.current_channel = None
        
        # Setup basic window structure
        self.setup_window()
        
        # Start checking for messages
        self.check_messages()
    
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
    
    def check_messages(self):
        """Check for messages from IRC client thread (for future use)."""
        try:
            while True:
                message = self.message_queue.get_nowait()
                # Process message (will be implemented in later steps)
                pass
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_messages)
    
    def on_closing(self):
        """Handle window closing event."""
        if self.connected and self.irc_client:
            # Disconnect from IRC before closing
            try:
                self.irc_client.disconnect()
            except:
                pass
        self.root.destroy()
    
    def update_status(self, status, color="black"):
        """Update the connection status display."""
        self.status_label.config(text=f"● {status}", foreground=color)
    
    def update_channel_display(self, channel=None):
        """Update the current channel display."""
        if channel:
            self.current_channel = channel
            self.channel_label.config(text=f"Channel: {channel}")
        else:
            self.current_channel = None
            self.channel_label.config(text="No channel selected")
    
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
    
    def setup_channel_management(self):
        """Set up the channel management interface."""
        # Channel join section
        join_frame = ttk.Frame(self.channel_frame)
        join_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Join channel label
        ttk.Label(join_frame, text="Join Channel:").pack(anchor=tk.W)
        
        # Channel entry and join button frame
        entry_frame = ttk.Frame(join_frame)
        entry_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Channel name entry
        self.channel_entry = ttk.Entry(
            entry_frame,
            font=("Consolas", 9),
            width=15
        )
        self.channel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        # Join button
        self.join_button = ttk.Button(
            entry_frame,
            text="Join",
            command=self.join_channel_gui,
            width=6
        )
        self.join_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to join
        self.channel_entry.bind('<Return>', lambda event: self.join_channel_gui())
        
        # Separator
        ttk.Separator(self.channel_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # Active channels section
        ttk.Label(self.channel_frame, text="Active Channels:").pack(anchor=tk.W)
        
        # Channels listbox with scrollbar
        listbox_frame = ttk.Frame(self.channel_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
        
        # Channels listbox
        self.channels_listbox = tk.Listbox(
            listbox_frame,
            font=("Consolas", 9),
            height=8,
            selectmode=tk.SINGLE
        )
        self.channels_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for listbox
        channel_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        channel_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure scrollbar
        self.channels_listbox.config(yscrollcommand=channel_scrollbar.set)
        channel_scrollbar.config(command=self.channels_listbox.yview)
        
        # Bind channel selection
        self.channels_listbox.bind('<<ListboxSelect>>', self.on_channel_select)
        
        # Channel action buttons
        button_frame = ttk.Frame(self.channel_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Leave channel button
        self.leave_button = ttk.Button(
            button_frame,
            text="Leave",
            command=self.leave_channel_gui,
            state=tk.DISABLED
        )
        self.leave_button.pack(side=tk.LEFT)
        
        # Initially disable join functionality until connected
        self.channel_entry.config(state=tk.DISABLED)
        self.join_button.config(state=tk.DISABLED)
        
        # Store channels list
        self.channels_list = []
    
    def add_message(self, message, tag=None):
        """Add a message to the chat display."""
        self.chat_text.config(state=tk.NORMAL)
        
        if tag:
            self.chat_text.insert(tk.END, message + "\n", tag)
        else:
            self.chat_text.insert(tk.END, message + "\n")
        
        # Auto-scroll to bottom
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
    
    def add_system_message(self, message):
        """Add a system message to the chat display."""
        from datetime import datetime
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        full_message = f"{timestamp} *** {message}"
        self.add_message(full_message, "system")
    
    def add_user_message(self, username, message, timestamp=None):
        """Add a user message to the chat display with proper formatting."""
        from datetime import datetime
        if not timestamp:
            timestamp = datetime.now().strftime("[%H:%M:%S]")
        
        # Add timestamp
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, timestamp + " ", "timestamp")
        
        # Add username
        self.chat_text.insert(tk.END, f"<{username}> ", "username")
        
        # Add message
        self.chat_text.insert(tk.END, message + "\n")
        
        # Auto-scroll to bottom
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
    
    def add_join_message(self, username, channel):
        """Add a join message to the chat display."""
        from datetime import datetime
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        message = f"{timestamp} --> {username} has joined {channel}"
        self.add_message(message, "join")
    
    def add_part_message(self, username, channel, reason=None):
        """Add a part message to the chat display."""
        from datetime import datetime
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        if reason:
            message = f"{timestamp} <-- {username} has left {channel} ({reason})"
        else:
            message = f"{timestamp} <-- {username} has left {channel}"
        self.add_message(message, "part")
    
    def add_error_message(self, message):
        """Add an error message to the chat display."""
        from datetime import datetime
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        full_message = f"{timestamp} !!! ERROR: {message}"
        self.add_message(full_message, "error")
    
    def clear_chat(self):
        """Clear the chat display."""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)
    
    def setup_message_input(self):
        """Set up the message input area with entry field and send button."""
        # Message input label
        input_label = ttk.Label(self.input_frame, text="Message:")
        input_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Message entry widget
        self.message_entry = ttk.Entry(
            self.input_frame,
            font=("Consolas", 10),
            width=50
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Send button
        self.send_button = ttk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            width=8
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to send message
        self.message_entry.bind('<Return>', lambda event: self.send_message())
        
        # Initially disable input until connected
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
    
    def send_message(self):
        """Send a message from the input field."""
        message = self.message_entry.get().strip()
        
        # Validate message
        if not message:
            return
        
        if not self.connected or not self.current_channel:
            self.add_error_message("Must be connected and in a channel to send messages")
            return
        
        # Check for commands
        if message.startswith('/'):
            self.handle_command(message)
        else:
            # Send regular message
            if self.irc_client:
                try:
                    # For now, just display locally (will integrate with IRC client in Step 6)
                    self.add_user_message("You", message)
                    # TODO: Actually send to IRC client when integrated
                except Exception as e:
                    self.add_error_message(f"Failed to send message: {str(e)}")
        
        # Clear input field
        self.message_entry.delete(0, tk.END)
    
    def handle_command(self, command):
        """Handle IRC commands from the input field."""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == '/help':
            self.show_help()
        elif cmd == '/clear':
            self.clear_chat()
        elif cmd == '/join' and len(parts) > 1:
            channel = parts[1]
            self.add_system_message(f"Attempting to join {channel}...")
            # TODO: Actually join channel when IRC client is integrated
        elif cmd == '/part' or cmd == '/leave':
            if self.current_channel:
                self.add_system_message(f"Leaving {self.current_channel}...")
                # TODO: Actually leave channel when IRC client is integrated
            else:
                self.add_error_message("Not in a channel")
        elif cmd == '/quit':
            self.on_closing()
        else:
            self.add_error_message(f"Unknown command: {cmd}. Type /help for available commands.")
    
    def show_help(self):
        """Display available commands in the chat."""
        self.add_system_message("Available commands:")
        self.add_system_message("/help - Show this help message")
        self.add_system_message("/clear - Clear chat history")
        self.add_system_message("/join #channel - Join a channel")
        self.add_system_message("/part or /leave - Leave current channel")
        self.add_system_message("/quit - Exit the application")
    
    def enable_input(self):
        """Enable message input (called when connected)."""
        self.message_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.message_entry.focus()
    
    def disable_input(self):
        """Disable message input (called when disconnected)."""
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
    
    def join_channel_gui(self):
        """Handle channel joining from GUI."""
        channel = self.channel_entry.get().strip()
        
        if not channel:
            return
        
        # Add # if not present
        if not channel.startswith('#'):
            channel = '#' + channel
        
        # Validate channel name
        if not self.validate_channel_name(channel):
            self.add_error_message(f"Invalid channel name: {channel}")
            return
        
        if not self.connected:
            self.add_error_message("Must be connected to join channels")
            return
        
        # Check if already in channel
        if channel in self.channels_list:
            self.add_error_message(f"Already in channel {channel}")
            self.switch_to_channel(channel)
            return
        
        # Add to channels list
        self.channels_list.append(channel)
        self.channels_listbox.insert(tk.END, channel)
        
        # Switch to this channel
        self.switch_to_channel(channel)
        
        # Clear entry
        self.channel_entry.delete(0, tk.END)
        
        # Add system message
        self.add_system_message(f"Joined channel {channel}")
        
        # TODO: Actually join channel via IRC client when integrated
    
    def leave_channel_gui(self):
        """Handle channel leaving from GUI."""
        selection = self.channels_listbox.curselection()
        if not selection:
            self.add_error_message("No channel selected")
            return
        
        channel = self.channels_list[selection[0]]
        
        # Remove from list
        self.channels_list.remove(channel)
        self.channels_listbox.delete(selection[0])
        
        # If this was the current channel, clear it
        if self.current_channel == channel:
            self.current_channel = None
            self.update_channel_display()
            self.leave_button.config(state=tk.DISABLED)
        
        # Add system message
        self.add_system_message(f"Left channel {channel}")
        
        # TODO: Actually leave channel via IRC client when integrated
    
    def on_channel_select(self, event):
        """Handle channel selection from listbox."""
        selection = self.channels_listbox.curselection()
        if selection:
            channel = self.channels_list[selection[0]]
            self.switch_to_channel(channel)
    
    def switch_to_channel(self, channel):
        """Switch to a different channel."""
        self.current_channel = channel
        self.update_channel_display(channel)
        
        # Enable leave button
        self.leave_button.config(state=tk.NORMAL)
        
        # Select in listbox
        try:
            index = self.channels_list.index(channel)
            self.channels_listbox.selection_clear(0, tk.END)
            self.channels_listbox.selection_set(index)
            self.channels_listbox.see(index)
        except ValueError:
            pass
        
        # Add system message
        self.add_system_message(f"Switched to channel {channel}")
    
    def validate_channel_name(self, channel):
        """Validate IRC channel name."""
        if not channel.startswith('#'):
            return False
        if len(channel) < 2:
            return False
        # Basic validation - can be expanded
        return True
    
    def enable_channel_management(self):
        """Enable channel management (called when connected)."""
        self.channel_entry.config(state=tk.NORMAL)
        self.join_button.config(state=tk.NORMAL)
    
    def disable_channel_management(self):
        """Disable channel management (called when disconnected)."""
        self.channel_entry.config(state=tk.DISABLED)
        self.join_button.config(state=tk.DISABLED)
        self.leave_button.config(state=tk.DISABLED)
