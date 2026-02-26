# Simple IRC Chat Client

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/badge/release-v1.0.0-green.svg)](https://github.com/Raventh23/simple-irc-chat/releases)

A comprehensive, terminal-based IRC chat client written in Python for learning and educational purposes.

> **📢 Recent Updates:** Default channel updated to #SiLabs for community alignment. See [CHANGELOG.md](CHANGELOG.md) for details.

## 🌟 Project Overview

This project implements a fully-featured IRC client that demonstrates network programming fundamentals while providing a robust, real-world chat application. Built through a structured 6-stage development process, it serves as both an educational resource and a functional IRC client.

### 🎯 Educational Focus
- Learn IRC protocol implementation from scratch
- Understand socket programming and network communication
- Explore multi-threaded application design
- Practice error handling and user experience design
- Study real-time application architecture

## ✨ Features

### 🔧 Core Functionality
- ✅ **IRC Protocol**: Complete implementation of essential IRC commands
- ✅ **Real-time Chat**: Connect to IRC servers and participate in live conversations
- ✅ **Multi-threading**: Simultaneous message sending and receiving
- ✅ **Channel Support**: Join and participate in IRC channels
- ✅ **Private Messaging**: Send direct messages to other users

### 💻 Interactive Interface
- ✅ **Terminal UI**: Clean, intuitive command-line interface
- ✅ **Enhanced Formatting**: Timestamps, user highlighting, and organized display
- ✅ **Real-time Updates**: Live message display with threading
- ✅ **Status Reporting**: Connection health and session information

### 🛠 Advanced Features
- ✅ **Auto-reconnection**: Automatic recovery from network failures
- ✅ **Configuration Management**: JSON config files and command-line options
- ✅ **Session Statistics**: Track uptime, messages, and connection metrics
- ✅ **Input Validation**: RFC-compliant nickname and channel validation
- ✅ **Security Features**: IRC injection prevention and message sanitization
- ✅ **Error Handling**: Comprehensive error recovery with user-friendly messages

### 📋 Available Commands

| Command | Description | Example Usage |
|---------|-------------|---------------|
| `/quit [message]` | Disconnect with optional message | `/quit See you later!` |
| `/join #channel` | Join an IRC channel | `/join #python` |
| `/nick nickname` | Change your nickname | `/nick NewName` |
| `/me action` | Send action message | `/me waves hello` |
| `/msg user message` | Send private message | `/msg friend Hello!` |
| `/help [command]` | Show help information | `/help nick` |
| `/status` | Show connection status | `/status` |
| `/stats` | Display session statistics | `/stats` |
| `/uptime` | Show session uptime | `/uptime` |
| `/reconnect` | Manually reconnect to server | `/reconnect` |
| `/config [action]` | Manage configuration | `/config show` |

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** (No external dependencies required)
- **Terminal/Command Prompt**
- **Internet connection** for IRC server access

### 💾 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Raventh23/simple-irc-chat.git
   cd simple-irc-chat
   ```

2. **Run the IRC client**:
   ```bash
   python src/irc_client.py
   ```

3. **Start chatting**:
   - Connects to irc.libera.chat (default server)
   - Automatically joins #SiLabs channel (default channel)
   - Send messages: Just type and press Enter
   - Get help: `/help`
   - Join other channels: `/join #channelname`

### ⚙️ Configuration Options

#### Command Line Usage
```bash
# Basic usage (connects to default server)
python src/irc_client.py

# Connect to specific server and channel
python src/irc_client.py -s irc.libera.chat -n MyBot --channel "#python"

# Use configuration file
python src/irc_client.py -c config/example_config.json

# Enable auto-reconnect and debug mode
python src/irc_client.py --auto-reconnect --debug
```

#### Configuration File Example
Create `config/my_config.json`:
```json
{
  "server": "irc.libera.chat",
  "port": 6667,
  "nickname": "MyBot",
  "channel": "#SiLabs",
  "auto_reconnect": true,
  "debug": false,
  "reconnect_delay": 5
}
```

## 📖 Usage Examples

### Basic Chat Session
```
$ python src/irc_client.py
Connected to irc.libera.chat:6667
[12:34:56] Connected as: SiLabsUser1234
[12:34:56] Joined #SiLabs
[12:34:56] Type /help for commands or just start typing to chat

> Hello everyone!
[12:35:05] <SiLabsUser1234> Hello everyone!

> /join #python
[12:35:10] Joined #python

> /me is learning IRC protocols
[12:35:15] * SiLabsUser1234 is learning IRC protocols

> /nick MyNewNick
[12:35:20] Nick changed to: MyNewNick

> /stats
[12:35:25] Session Statistics:
            Uptime: 0:01:29
            Messages sent: 3
            Connection: Stable

> /quit Thanks for the chat!
[12:35:30] Disconnected: Thanks for the chat!
```

### Advanced Configuration
```bash
# Connect with custom settings
python src/irc_client.py \
  --server irc.libera.chat \
  --port 6667 \
  --nickname "MyBot" \
  --channel "#python" \
  --auto-reconnect \
  --debug

# Use environment-specific config
python src/irc_client.py -c config/production.json
```

## 🧪 Testing

The project includes comprehensive testing:

```bash
# Run all tests
python -m pytest tests/ -v

# Test specific functionality
python tests/test_connection.py      # Basic connection tests
python tests/test_stage5_automated.py  # Advanced feature tests

# Manual testing with demo
python irc_demo.py
```

## 📚 Documentation

Comprehensive documentation is available:

- **[📖 User Manual](docs/USER_MANUAL.md)** - Complete guide with tutorials and examples
- **[🔧 Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[🔍 Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[📋 Build Plan](docs/build_plan.md)** - Development methodology and stage breakdown
- **[🏗️ Architecture Design](docs/design.md)** - Technical design and implementation details

## 🎓 Educational Value

This project is designed for learning:

### 📖 Topics Covered
- **Network Programming**: Socket programming with Python
- **IRC Protocol**: Real-world protocol implementation
- **Multi-threading**: Concurrent programming patterns
- **Error Handling**: Robust application design
- **User Experience**: Terminal interface design
- **Testing**: Comprehensive test-driven development

### 🎯 Learning Outcomes
After studying this project, you'll understand:
- How IRC protocol works at the network level
- Socket programming and network communication
- Multi-threaded application architecture
- Real-time data processing and display
- Error recovery and connection management
- Command parsing and validation
- Configuration management and user preferences

## 🏗️ Architecture

### 🔧 Technical Design
- **Modular Architecture**: Clear separation between networking, UI, and commands
- **Multi-threaded**: Separate threads for input handling and message receiving
- **Event-driven**: Responsive to user input and network events
- **Extensible**: Well-structured for adding new features

### 📊 Performance
- **Stability**: Tested for extended sessions (2+ hours)
- **Scalability**: Handles high-traffic channels (100+ messages/minute)
- **Recovery**: Automatic reconnection from network failures
- **Compatibility**: Works across major IRC servers and platforms

## 🤝 Contributing

We welcome contributions from the community! This project is designed to be educational and beginner-friendly.

### 🚀 Getting Started
1. Read our **[Contributing Guidelines](CONTRIBUTING.md)**
2. Check out **[open issues](https://github.com/Raventh23/simple-irc-chat/issues)**
3. Fork the repository and create a feature branch
4. Submit a pull request with your improvements

### 💡 Ways to Contribute
- **🐛 Bug Reports**: Help us identify and fix issues
- **✨ Feature Requests**: Suggest new functionality
- **📖 Documentation**: Improve guides and tutorials
- **🧪 Testing**: Add test cases and improve coverage
- **💻 Code**: Implement new features or optimizations

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 🔓 What this means:
- ✅ **Free to use** for personal and commercial projects
- ✅ **Modify and distribute** as needed
- ✅ **No warranty** - use at your own risk
- ✅ **Attribution appreciated** but not required

## 🌟 Acknowledgments

### 🙏 Special Thanks
- **IRC Community**: For protocol documentation and testing opportunities
- **Python Community**: For excellent standard library networking support
- **Open Source Contributors**: For inspiration and best practices
- **Educational Resources**: RFCs, tutorials, and community knowledge

### 📚 References
- **RFC 1459**: Internet Relay Chat Protocol specification
- **RFC 2812**: Internet Relay Chat: Client Protocol
- **Python Documentation**: Socket programming guides
- **IRC.org**: Community resources and server information

## 🔮 Future Roadmap

While v1.0.0 is feature-complete for educational purposes, potential enhancements include:

### 🎯 Short-term Possibilities
- **Multi-channel tabs**: Better multi-channel support
- **Color themes**: Customizable terminal colors
- **Logging**: Chat history and session logs
- **Notifications**: Desktop notifications for mentions

### 🚀 Long-term Vision
- **GUI Version**: Graphical user interface option
- **Plugin System**: Extensible architecture for custom features
- **Advanced IRC**: DCC file transfer, channel modes, user lists
- **Mobile Support**: Terminal-based mobile client

## 📊 Project Statistics

- **📅 Development Time**: 6 weeks (structured staging approach)
- **📝 Lines of Code**: ~800 (core client) + comprehensive documentation
- **🧪 Test Coverage**: Full feature coverage across all stages
- **📖 Documentation**: 5+ comprehensive guides
- **🎯 Supported Commands**: 11 built-in commands with help system
- **🖥️ Platform Support**: macOS, Linux, Windows
- **🌐 IRC Compatibility**: Libera.Chat, Freenode, and standard IRC servers

## 🆘 Support

### 📞 Getting Help
- **📖 Documentation**: Check our comprehensive guides first
- **🐛 Issues**: Report bugs via [GitHub Issues](https://github.com/Raventh23/simple-irc-chat/issues)
- **💬 Discussions**: Ask questions in [GitHub Discussions](https://github.com/Raventh23/simple-irc-chat/discussions)
- **📧 Contact**: Reach out for educational or collaboration inquiries

### 🔍 Troubleshooting
Common issues and solutions are documented in our [Troubleshooting Guide](docs/TROUBLESHOOTING.md).

---

## 🚀 Ready to Get Started?

1. **📥 Clone the repository**: `git clone https://github.com/Raventh23/simple-irc-chat.git`
2. **🏃 Run the client**: `python src/irc_client.py`
3. **💬 Start chatting**: You'll auto-join #SiLabs channel
4. **📖 Explore the docs**: Check out our comprehensive guides
5. **🤝 Get involved**: Contribute to the project!

**Happy chatting and learning! 🎉💬**

---

*Simple IRC Chat Client v1.0.0 - Built with ❤️ for the learning community*
