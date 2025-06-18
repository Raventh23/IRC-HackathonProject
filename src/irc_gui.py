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


def main():
    """Main function to start the GUI application."""
    app = IRCClientGUI()
    app.run()


if __name__ == "__main__":
    main()
