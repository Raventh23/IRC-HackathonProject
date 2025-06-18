# Simple IRC Chat - Design Document

## Project Overview

A minimal IRC (Internet Relay Chat) client application written in Python. This project aims to create a simple, terminal-based chat client that can connect to IRC servers, join channels, and send/receive messages in real-time.

**Goals:**
- Learn IRC protocol fundamentals
- Build a working chat client with minimal complexity
- Create a foundation for future enhancements
- Focus on core functionality over advanced features

**Target Users:**
- Developers wanting to understand IRC protocol
- Users needing a simple, lightweight IRC client
- Educational purposes for network programming

**Scope:**
- Single server connection
- Single channel participation
- Basic message sending/receiving
- Simple terminal interface
- Essential IRC commands only

## Core Requirements

**Functional Requirements:**
- Connect to an IRC server using TCP socket connection
- Authenticate with nickname and user information
- Join a specified IRC channel
- Send text messages to the channel
- Receive and display messages from other users in real-time
- Handle basic IRC commands (/quit, /join, /nick)
- Gracefully disconnect from server

**Non-Functional Requirements:**
- Simple terminal-based user interface
- Responsive message handling (no significant delays)
- Stable connection handling with basic error recovery
- Cross-platform compatibility (Windows, macOS, Linux)
- Minimal resource usage
- Clear, readable code structure

**Technical Constraints:**
- Python 3.7+ (using built-in libraries where possible)
- No external dependencies for core functionality
- Single-threaded or simple multi-threading approach
- Plain text communication (no encryption initially)
- Standard IRC protocol compliance (RFC 1459/2812 basics)

**Out of Scope (for initial version):**
- Multiple server connections
- Multiple channel management
- User authentication beyond basic nickname
- Message logging/history
- File transfers
- Advanced IRC features (modes, operator commands)
- Graphical user interface

## Minimal Tool Set

### Core Python Libraries

**Built-in Libraries (No Installation Required):**
- `socket` - TCP connection to IRC server
- `threading` - Handle simultaneous send/receive operations
- `time` - Delays and timestamps
- `sys` - System operations and exit handling
- `re` - Regular expressions for parsing IRC messages
- `json` - Configuration file handling (optional)

**Standard Library Modules:**
- `select` - Non-blocking socket operations (alternative to threading)
- `ssl` - For secure connections (if needed later)
- `logging` - Debug and error logging

### Development Tools

**Essential:**
- Python 3.7+ interpreter
- Text editor or IDE (VS Code, PyCharm, vim, etc.)
- Terminal/command prompt for testing

**Recommended:**
- `pytest` - Unit testing (can install later)
- `black` - Code formatting (can install later)
- `flake8` - Code linting (can install later)

**For Version 1 - Absolutely Minimal:**
- Just Python built-in libraries
- No external package installations
- Keep dependencies at zero for maximum simplicity

## Simple Architecture

### Connection Flow

1. **Initialize Socket**: Create TCP socket connection
2. **Connect to Server**: Connect to IRC server (e.g., irc.libera.chat:6667)
3. **Send Registration**: Send NICK and USER commands
4. **Wait for Welcome**: Receive 001 welcome message from server
5. **Join Channel**: Send JOIN command for target channel
6. **Start Message Loop**: Begin sending/receiving messages
7. **Handle Disconnect**: Clean shutdown on /quit or connection loss

### Message Handling

**Receiving Messages (Background Thread):**
- Continuously listen on socket for incoming data
- Parse IRC protocol messages (PRIVMSG, JOIN, PART, etc.)
- Extract sender, channel, and message content
- Display formatted messages to user terminal
- Handle server commands (PING/PONG for keepalive)

**Sending Messages (Main Thread):**
- Read user input from terminal
- Check if input is a command (starts with /)
- Format as IRC protocol message
- Send via socket to server
- Handle special commands locally (/quit, /help)

### User Interface

**Terminal-Based Interface:**
- Simple input/output using `input()` and `print()`
- Message format: `[HH:MM] <nickname> message`
- User types messages directly, presses Enter to send
- Commands start with / (e.g., /quit, /join #channel)
- No fancy formatting - just plain text output
- Clear separation between received messages and user input

**Flow:**
```
[12:34] <alice> Hello everyone!
[12:35] <bob> Hey alice!
> your message here_
```

## Starting Point Features

**Version 1.0 - Core Features:**
- Connect to a single IRC server (hardcoded or configurable)
- Set nickname and basic user info
- Join one channel automatically or via command
- Send plain text messages to the channel
- Receive and display messages from other users
- Basic timestamp display for messages
- Graceful disconnect with /quit command

**Essential Commands:**
- `/quit` - Disconnect and exit application
- `/join #channel` - Join a different channel
- `/nick newnick` - Change nickname
- `/help` - Show available commands

**Message Display:**
- Show channel messages in chronological order
- Display user joins/parts (optional)
- Simple error messages for connection issues
- Basic status messages (connected, joined channel, etc.)

## Basic Commands

**User Commands:**
- `/quit [message]` - Disconnect from server and exit
  - Example: `/quit Goodbye!`
- `/join #channel` - Join a new channel
  - Example: `/join #python`
- `/nick nickname` - Change your nickname
  - Example: `/nick alice123`
- `/help` - Display list of available commands
- `/me action` - Send action message (optional)
  - Example: `/me waves hello`

**IRC Protocol Commands (Internal):**
- `NICK nickname` - Set/change nickname
- `USER username hostname servername realname` - User registration
- `JOIN #channel` - Join channel
- `PRIVMSG #channel :message` - Send message to channel
- `QUIT :message` - Disconnect from server
- `PONG :server` - Respond to server PING

## Technical Implementation

### Socket Connection

**Connection Setup:**
```python
import socket

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to server
sock.connect((server, port))  # e.g., ('irc.libera.chat', 6667)
# Send registration
sock.send(b'NICK mynick\r\n')
sock.send(b'USER myuser 0 * :My Real Name\r\n')
```

**Error Handling:**
- Connection timeouts
- Server disconnections
- Invalid server responses
- Network interruptions

### Threading Model

**Two-Thread Approach:**
1. **Main Thread**: Handle user input and sending messages
2. **Receiver Thread**: Continuously listen for incoming messages

**Thread Communication:**
- Use thread-safe methods for shared data
- Graceful shutdown coordination between threads
- Exception handling in both threads

**Alternative: Select-based (Single Thread):**
- Use `select.select()` for non-blocking I/O
- Poll both socket and stdin for activity
- More complex but avoids threading issues

### Message Protocol

**IRC Message Format:**
```
:prefix COMMAND params :trailing
```

**Common Message Types:**
- `PRIVMSG #channel :Hello world` - Channel message
- `:nick!user@host PRIVMSG #channel :message` - Received message
- `PING :server` - Server keepalive (respond with PONG)
- `001 nick :Welcome message` - Connection successful

**Parsing Strategy:**
- Split on spaces and colons
- Extract command, sender, target, message
- Handle different message types appropriately

## Future Enhancements

**Phase 2 Features:**
- Multiple channel support
- Private messaging between users
- Message history/logging
- Configuration file for server settings
- Better error handling and reconnection
- User list for channels

**Phase 3 Features:**
- SSL/TLS secure connections
- SASL authentication
- IRC color code support
- File transfer (DCC)
- Bot functionality and scripting

**UI Improvements:**
- Curses-based terminal interface
- Multiple window/pane support
- Tab completion for nicknames
- Scrollback buffer
- Eventually: GUI version (tkinter/PyQt)

**Advanced Features:**
- Plugin system
- IRC bouncer support
- Multiple server connections
- Advanced IRC features (channel modes, operator commands)

## Testing Strategy

**Manual Testing:**
- Connect to test IRC server (e.g., irc.libera.chat)
- Test basic message sending/receiving
- Verify command handling
- Test connection error scenarios
- Cross-platform testing (Windows, macOS, Linux)

**Automated Testing (Future):**
- Unit tests for message parsing
- Mock IRC server for integration testing
- Connection handling tests
- Command processing tests

**Test Scenarios:**
- Normal operation flow
- Server disconnection handling
- Invalid command handling
- Network timeout scenarios
- Multiple user interaction

## Deployment Considerations

**Distribution:**
- Single Python file for simplicity
- No external dependencies (initially)
- Cross-platform compatibility
- Clear installation/usage instructions

**Configuration:**
- Command-line arguments for server/channel
- Optional config file (JSON/INI format)
- Environment variable support
- Sensible defaults

**Documentation:**
- README with quick start guide
- Example usage scenarios
- Troubleshooting common issues
- IRC basics for new users

**Performance:**
- Minimal memory footprint
- Efficient message handling
- Responsive user interface
- Graceful handling of high-traffic channels
