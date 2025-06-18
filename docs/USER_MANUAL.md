# Simple IRC Chat Client - User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Basic Usage](#basic-usage)
5. [Advanced Features](#advanced-features)
6. [Configuration](#configuration)
7. [Commands Reference](#commands-reference)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)
10. [IRC Basics](#irc-basics)

## Introduction

The Simple IRC Chat Client is a feature-rich, terminal-based IRC client written in Python. It provides a clean, user-friendly interface for connecting to IRC servers, joining channels, and participating in real-time chat conversations.

### Key Features
- 🌐 Connect to any IRC server
- 💬 Join multiple channels and participate in chat
- 🔄 Auto-reconnect with connection reliability
- ⚙️ Configuration file support
- 📊 Session statistics and monitoring
- 🛡️ Security features and input validation
- 🎨 Enhanced message formatting
- 💡 Comprehensive help system

### Who Should Use This?
- IRC newcomers who want a simple, reliable client
- Developers learning IRC protocol basics
- Users who prefer terminal-based applications
- Anyone needing a lightweight, cross-platform IRC client

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only built-in libraries)

### Method 1: Clone from GitHub
```bash
git clone https://github.com/Raventh23/simple-irc-chat.git
cd simple-irc-chat
python3 src/irc_client.py
```

### Method 2: Download ZIP
1. Download the ZIP file from GitHub
2. Extract to your preferred directory
3. Open terminal in the extracted directory
4. Run: `python3 src/irc_client.py`

### Verify Installation
```bash
# Test the basic client
python3 src/irc_client.py

# Test the enhanced Stage 5 client
python3 tests/test_stage5.py --help
```

## Quick Start

### Connect and Chat in 3 Steps

1. **Start the client:**
   ```bash
   python3 tests/test_stage5.py
   ```

2. **The client will automatically:**
   - Connect to irc.libera.chat
   - Register with a random nickname
   - Join #bottest channel

3. **Start chatting:**
   - Type messages directly to chat
   - Use `/help` to see available commands
   - Use `/quit` to exit

### Your First IRC Session
```bash
# Example session
python3 tests/test_stage5.py -n YourNickname --channel "#beginners"
```

Once connected, try these commands:
- `Hello everyone!` - Send a message
- `/me waves` - Send an action
- `/status` - Check connection status
- `/help` - See all commands

## Basic Usage

### Connecting to IRC

#### Using Default Settings
```bash
python3 tests/test_stage5.py
```
Connects to irc.libera.chat with auto-generated nickname.

#### Custom Connection
```bash
python3 tests/test_stage5.py -s irc.freenode.net -n MyNick --channel "#python"
```

#### With Auto-Reconnect
```bash
python3 tests/test_stage5.py --auto-reconnect --reconnect-delay 15
```

### Basic Chat Commands

| Command | Description | Example |
|---------|-------------|---------|
| `message` | Send message to current channel | `Hello everyone!` |
| `/join #channel` | Join a channel | `/join #python` |
| `/quit [message]` | Leave IRC | `/quit Good night!` |
| `/nick newnick` | Change nickname | `/nick CoolUser` |
| `/me action` | Send action message | `/me is learning IRC` |
| `/help` | Show help | `/help` or `/help join` |

### Channel Operations

#### Joining Channels
```
/join #python          # Join Python discussion
/join #help            # Join help channel
/join #mychannel       # Join any channel
```

#### Leaving Channels
```
/part                  # Leave current channel
/part #python          # Leave specific channel
```

#### Switching Channels
Simply join a new channel - it becomes your active channel automatically.

## Advanced Features

### Connection Reliability

#### Auto-Reconnect
```bash
# Enable auto-reconnect with custom settings
python3 tests/test_stage5.py --auto-reconnect --max-reconnect 10 --reconnect-delay 20
```

When enabled, the client will:
- Automatically reconnect if connection is lost
- Rejoin all previously joined channels
- Retry up to the specified maximum attempts
- Wait the specified delay between attempts

#### Manual Reconnection
Use `/reconnect` command to manually reconnect to the server.

#### Connection Monitoring
The client continuously monitors connection health:
- PING/PONG keepalive handling
- Connection stability reporting
- Network timeout detection

### Session Statistics

#### View Current Statistics
```
/status     # Complete status overview
/stats      # Session statistics
/uptime     # Session duration
```

#### Statistics Include:
- Messages sent and received
- Session uptime
- Connection stability
- Reconnection attempts
- Active channels

### Enhanced Message Display

The client provides rich message formatting:
```
                                        [12:34] <User1> Hello everyone!
                                        [12:34] * ActionUser waves
                                        [12:35] → NewUser joined #channel
                                        [12:35] ← OldUser left #channel (Goodbye!)
                                        [12:36] 🏷️  User1 is now known as User1_away
```

## Configuration

### Configuration Files

#### Creating a Configuration File
```json
{
  "server": "irc.libera.chat",
  "port": 6667,
  "nickname": "MyIRCBot",
  "username": "myuser",
  "realname": "My IRC Client",
  "auto_reconnect": true,
  "reconnect_delay": 30,
  "show_status_messages": true
}
```

#### Using Configuration Files
```bash
# Load configuration
python3 tests/test_stage5.py -c config/my_config.json

# Save current settings
# (Use /config save command while running)
```

### Runtime Configuration

#### View Current Settings
```
/config show
```

#### Toggle Settings
```
/config toggle reconnect    # Toggle auto-reconnect
/config toggle status       # Toggle status messages
```

#### Save Settings
```
/config save                # Save to default file
/config save my_config.json # Save to specific file
```

### Command Line Options

```bash
# Server and connection options
-s, --server SERVER          # IRC server (default: irc.libera.chat)
-p, --port PORT             # Port number (default: 6667)
-n, --nickname NICK         # Your nickname
--channel CHANNEL           # Initial channel to join

# Reliability options
--auto-reconnect            # Enable auto-reconnect
--reconnect-delay SECONDS   # Delay between attempts
--max-reconnect NUMBER      # Maximum attempts

# Configuration options
-c, --config FILE           # Configuration file
--no-status                 # Disable status messages
--debug                     # Enable debug mode
```

## Commands Reference

### Basic Commands

| Command | Syntax | Description |
|---------|---------|-------------|
| `/help` | `/help [command]` | Show help for all commands or specific command |
| `/quit` | `/quit [message]` | Disconnect and exit with optional message |
| `/join` | `/join #channel` | Join a channel |
| `/part` | `/part [#channel]` | Leave current or specified channel |
| `/nick` | `/nick nickname` | Change your nickname |
| `/me` | `/me action` | Send action message |
| `/msg` | `/msg nickname message` | Send private message |

### Status Commands

| Command | Description |
|---------|-------------|
| `/status` | Show detailed connection and session status |
| `/stats` | Display session statistics |
| `/uptime` | Show current session uptime |
| `/reconnect` | Manually reconnect to server |

### Configuration Commands

| Command | Description |
|---------|-------------|
| `/config show` | Display current configuration |
| `/config save [file]` | Save configuration to file |
| `/config toggle reconnect` | Toggle auto-reconnect |
| `/config toggle status` | Toggle status messages |

### Command Examples

#### Help System
```
/help                    # Show all commands
/help join              # Help for join command
/help config            # Help for config commands
```

#### Channel Management
```
/join #python           # Join Python channel
/join #help             # Join help channel
/part                   # Leave current channel
/part #python           # Leave Python channel
```

#### Communication
```
Hello everyone!         # Send message to current channel
/me is learning IRC     # Send action message
/msg friend Hey there!  # Send private message
/nick CoolUser          # Change nickname
```

#### Status and Monitoring
```
/status                 # Full status report
/stats                  # Session statistics
/uptime                 # Session duration
/reconnect              # Manual reconnect
```

## Troubleshooting

### Common Issues

#### Connection Problems

**Issue: Cannot connect to server**
```
❌ Connection failed!
```
**Solutions:**
1. Check your internet connection
2. Verify server address and port
3. Try a different IRC server
4. Use debug mode: `--debug`

**Issue: Nickname already in use**
```
❌ Nickname is already in use
```
**Solutions:**
1. Choose a different nickname: `/nick NewNickname`
2. Use underscore or numbers: `MyNick_` or `MyNick123`
3. The client will suggest alternatives

#### Channel Issues

**Issue: Cannot join channel**
```
❌ Cannot join channel (+l)
```
**Solutions:**
1. Channel may be full (mode +l)
2. Channel may be invite-only (mode +i)
3. You may be banned (mode +b)
4. Try a different channel

**Issue: Messages not sending**
```
❌ Not in a channel. Join a channel first with /join #channel
```
**Solution:**
Join a channel first: `/join #general`

#### Performance Issues

**Issue: Client seems slow or unresponsive**
**Solutions:**
1. Check connection with `/status`
2. Enable auto-reconnect: `/config toggle reconnect`
3. Restart client if necessary
4. Check for network issues

#### Configuration Issues

**Issue: Configuration file not loading**
```
⚠️ Configuration file config.json not found, using defaults
```
**Solutions:**
1. Check file path and name
2. Verify JSON syntax
3. Use absolute path if needed
4. Create new config with `/config save`

### Debug Mode

Enable debug mode for detailed troubleshooting:
```bash
python3 tests/test_stage5.py --debug
```

Debug mode shows:
- Raw IRC protocol messages
- Connection details
- Error stack traces
- Internal state information

### Getting Help

1. **Use built-in help:** `/help`
2. **Check status:** `/status`
3. **Review this manual**
4. **Check project documentation on GitHub**

## FAQ

### General Questions

**Q: What IRC servers can I connect to?**
A: Any standard IRC server. Popular servers include:
- irc.libera.chat (default)
- irc.freenode.net
- irc.oftc.net
- irc.rizon.net

**Q: Can I connect to multiple servers?**
A: Currently, the client connects to one server at a time. You can run multiple instances for different servers.

**Q: Is this client secure?**
A: Yes, it includes security features:
- IRC injection prevention
- Message sanitization
- Input validation
- No plain text password storage

### Usage Questions

**Q: How do I change my nickname?**
A: Use `/nick newnickname` or set it when starting: `-n newnickname`

**Q: How do I join a private channel?**
A: Use `/join #channelname`. If it's invite-only, you'll need an invitation from a channel operator.

**Q: Can I send private messages?**
A: Yes, use `/msg nickname your message here`

**Q: How do I see who's in a channel?**
A: This feature is planned for future versions. Currently, you'll see users as they join/leave/speak.

### Technical Questions

**Q: What Python version do I need?**
A: Python 3.7 or higher. The client uses only built-in libraries.

**Q: Does it work on Windows/Mac/Linux?**
A: Yes, it's cross-platform and works on all major operating systems.

**Q: Can I customize the interface?**
A: Limited customization is available through configuration files. The interface is designed to be clean and consistent.

**Q: How do I report bugs or request features?**
A: Visit the GitHub repository and create an issue.

### Advanced Questions

**Q: Can I use this in scripts or automation?**
A: The client is designed for interactive use. For automation, you might want to modify the code or use the core classes.

**Q: How does auto-reconnect work?**
A: The client monitors connection health and automatically reconnects if the connection is lost, then rejoins all previously joined channels.

**Q: Can I log conversations?**
A: Basic logging is available in debug mode. Full conversation logging is not currently implemented.

## IRC Basics

### What is IRC?

IRC (Internet Relay Chat) is a text-based chat protocol that has been around since 1988. It allows real-time communication in channels (rooms) or private messages.

### Key Concepts

#### Servers and Networks
- **Server**: A computer running IRC server software
- **Network**: A group of connected servers (like Libera.Chat)
- **Client**: Software you use to connect to IRC (like this client)

#### Channels
- **Channel**: A chat room where multiple people can talk
- **Channel names**: Start with # (like #python, #help)
- **Topic**: A description of what the channel is about
- **Modes**: Settings that control channel behavior

#### Users and Nicknames
- **Nickname**: Your identity on IRC (like a username)
- **Real name**: Optional full name (usually not displayed)
- **Username**: Technical identifier (usually not important for users)

#### Common IRC Terms

| Term | Description |
|------|-------------|
| **Nick** | Your nickname/identity |
| **Channel** | Chat room (starts with #) |
| **Op** | Channel operator (has special privileges) |
| **Kick** | Forcibly remove someone from channel |
| **Ban** | Prevent someone from joining channel |
| **Mode** | Channel or user setting |
| **PING/PONG** | Keepalive messages to maintain connection |
| **Quit** | Leave IRC entirely |
| **Part** | Leave a specific channel |

### IRC Etiquette

#### General Guidelines
1. **Be respectful** - Treat others as you'd like to be treated
2. **Stay on topic** - Keep discussions relevant to the channel
3. **Don't spam** - Avoid repeating messages or flooding
4. **Use proper channels** - Ask questions in appropriate places
5. **Be patient** - People may not respond immediately

#### Channel-Specific Rules
- Read channel topic and rules when joining
- Some channels have specific purposes (help, development, social)
- Respect channel operators and their decisions
- Use `/help` channels for getting assistance

#### Common Mistakes to Avoid
- Don't ask to ask - just ask your question
- Don't send the same message to multiple channels
- Don't use ALL CAPS (considered shouting)
- Don't share personal information publicly
- Don't argue with channel operators

### Popular IRC Networks

| Network | Address | Description |
|---------|---------|-------------|
| **Libera.Chat** | irc.libera.chat | Open source and free software communities |
| **OFTC** | irc.oftc.net | Open and Free Technology Community |
| **Rizon** | irc.rizon.net | General purpose network |
| **EFNet** | irc.efnet.org | One of the oldest IRC networks |

### Getting Started on IRC

1. **Choose a nickname** - Pick something unique and appropriate
2. **Start with beginner channels** - Try #help or #new2irc
3. **Learn the basics** - Practice basic commands
4. **Find communities** - Look for channels matching your interests
5. **Be patient** - IRC culture can take time to understand

### Next Steps

Once you're comfortable with the basics:
- Explore different channels and communities
- Learn advanced IRC commands and features
- Consider registering your nickname (server-specific process)
- Join project-specific channels for software you use
- Participate in IRC communities related to your interests

---

*This manual covers the essential information for using the Simple IRC Chat Client. For technical details and advanced usage, refer to the project documentation on GitHub.*
