# Simple IRC Chat Client

A minimal IRC chat client written in Python for learning and educational purposes.

## Project Overview

This project implements a simple, terminal-based IRC client that can connect to IRC servers, join channels, and send/receive messages in real-time. The focus is on learning IRC protocol fundamentals while building a working chat application.

## Features

### Core Functionality
- ✅ Connect to IRC servers (Libera.Chat, Freenode, etc.)
- ✅ Join channels and participate in chat
- ✅ Send and receive messages in real-time
- ✅ Interactive threaded terminal interface
- ✅ Comprehensive IRC command support

### Commands
- ✅ `/quit [message]` - Disconnect with optional quit message
- ✅ `/join #channel` - Join a channel
- ✅ `/nick nickname` - Change your nickname
- ✅ `/me action` - Send action messages
- ✅ `/msg nickname message` - Send private messages
- ✅ `/help [command]` - Show help for all or specific commands

### Advanced Features
- ✅ **Input Validation**: RFC-compliant nickname and channel validation
- ✅ **Security**: IRC injection prevention and message sanitization
- ✅ **Error Handling**: User-friendly error messages and recovery
- ✅ **Real-time**: Simultaneous send/receive with threading
- ✅ **Help System**: Comprehensive command documentation
- ✅ **Connection Monitoring**: PING/PONG handling and stability checks

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only built-in libraries)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Raventh23/simple-irc-chat.git
   cd simple-irc-chat
   ```

2. Run the IRC client:
   ```bash
   python src/irc_client.py
   ```

## Usage

### Basic Connection
The client will connect to irc.libera.chat by default. You can specify a different server in the code.

### Available Commands
- `/quit [message]` - Disconnect and exit with optional message
- `/join #channel` - Join a channel
- `/nick nickname` - Change your nickname
- `/me action` - Send action message (* nickname action)
- `/msg nickname message` - Send private message to user
- `/help [command]` - Show help for all commands or specific command

### Interactive Features
- Real-time message display with timestamps
- Threaded input handling for simultaneous chat
- Comprehensive error handling with helpful messages
- Input validation and security protection
- Connection stability monitoring

## Development Status

This project follows a structured build plan with incremental feature delivery.

### Current Stage: Stage 4 Complete ✅
**Essential Commands & Error Handling**

**Completed Stages:**
- ✅ **Stage 1**: Foundation Setup & Socket Connection
- ✅ **Stage 2**: IRC Protocol Basics & Authentication  
- ✅ **Stage 3**: Core Chat Functionality & Interactive Interface
- ✅ **Stage 4**: Essential Commands & Comprehensive Error Handling

**Next Steps:**
- **Stage 5**: Polish & Stability (Connection reliability, UX improvements)
- **Stage 6**: Testing & Documentation (Cross-platform testing, final docs)

See the [build plan](docs/build_plan.md) for detailed progress and upcoming features.
- [x] Basic project structure
- [x] Socket connection implementation
- [ ] IRC protocol basics
- [ ] Message handling
- [ ] User interface

## Documentation

- [Design Document](docs/design.md) - Comprehensive project design
- [Build Plan](docs/build_plan.md) - Development roadmap and stages

## License

This project is for educational purposes. Feel free to use and modify as needed.

## Contributing

This is a learning project, but suggestions and improvements are welcome through issues and pull requests.
