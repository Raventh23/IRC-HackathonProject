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
        self.root.title("IRC Chat Client - GUI")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
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
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top frame for connection status
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(self.status_frame, text="Status: Not connected")
        self.status_label.pack(side=tk.LEFT)
        
        # Middle section with chat and channels
        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Left frame for channel list (placeholder for now)
        self.channel_frame = ttk.LabelFrame(middle_frame, text="Channels", width=150)
        self.channel_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        self.channel_frame.pack_propagate(False)
        
        # Center frame for chat display (placeholder for now)
        self.chat_frame = ttk.LabelFrame(middle_frame, text="Chat")
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Bottom frame for message input (placeholder for now)
        self.input_frame = ttk.Frame(main_frame)
        self.input_frame.pack(fill=tk.X)
        
        # Placeholder labels for development
        ttk.Label(self.channel_frame, text="Channel list\n(Coming in Step 5)").pack(pady=20)
        ttk.Label(self.chat_frame, text="Chat display area\n(Coming in Step 3)").pack(pady=50)
        ttk.Label(self.input_frame, text="Message input area (Coming in Step 4)").pack(pady=10)
    
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
