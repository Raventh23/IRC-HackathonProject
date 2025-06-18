# Simple IRC Chat Client

A minimal IRC chat client written in Python for learning and educational purposes.

## Project Overview

This project implements a simple, terminal-based IRC client that can connect to IRC servers, join channels, and send/receive messages in real-time. The focus is on learning IRC protocol fundamentals while building a working chat application.

## Features

- Connect to IRC servers
- Join channels and participate in chat
- Send and receive messages in real-time
- Basic IRC commands (/quit, /join, /nick)
- Simple terminal-based interface

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
- `/quit [message]` - Disconnect and exit
- `/join #channel` - Join a channel
- `/nick nickname` - Change your nickname
- `/help` - Show available commands

## Development Status

This project is currently in development. See the build plan for detailed progress.

### Current Stage: Stage 1 - Foundation Setup
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
