#!/usr/bin/env python3
"""
Simple IRC Chat Client
A minimal IRC client for learning and educational purposes.
"""

import socket
import sys
import time


class IRCClient:
    """Basic IRC client with socket connection capabilities."""
    
    def __init__(self, server="irc.libera.chat", port=6667):
        """Initialize IRC client with server details."""
        self.server = server
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """Establish TCP connection to IRC server."""
        try:
            print(f"Connecting to {self.server}:{self.port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout
            self.socket.connect((self.server, self.port))
            self.connected = True
            print(f"Connected to {self.server}!")
            return True
        except socket.timeout:
            print("Error: Connection timed out")
            return False
        except socket.gaierror:
            print("Error: Could not resolve server address")
            return False
        except ConnectionRefusedError:
            print("Error: Connection refused by server")
            return False
        except Exception as e:
            print(f"Error: Failed to connect - {e}")
            return False
    
    def disconnect(self):
        """Close connection to IRC server."""
        if self.socket:
            try:
                self.socket.close()
                print("Disconnected from server")
            except Exception as e:
                print(f"Error during disconnect: {e}")
            finally:
                self.connected = False
                self.socket = None


def main():
    """Main function to test basic connection."""
    print("Simple IRC Chat Client - Stage 1 Test")
    print("====================================")
    
    # Create client instance
    client = IRCClient()
    
    # Test connection
    if client.connect():
        print("Connection test successful!")
        time.sleep(2)  # Keep connection open briefly
        client.disconnect()
        print("Stage 1.2 Complete: Basic socket connection working")
    else:
        print("Connection test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
