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
        
        # Right frame for chat display
        self.chat_frame = ttk.LabelFrame(self.paned_window, text="Chat", padding="5")
        self.paned_window.add(self.chat_frame, weight=1)
        
        # Chat display area with scrollbar
        self.setup_chat_display()
        
        # Bottom frame for message input
        self.input_frame = ttk.Frame(main_frame)
        self.input_frame.pack(fill=tk.X, pady=(0, 5))
        
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
