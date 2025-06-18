# IRC Client Usage Guide - Stage 5 Features

## Overview
Stage 5 introduces enhanced stability, connection reliability, and improved user experience features to the IRC client.

## New Features in Stage 5

### 🔄 Connection Reliability
- **Auto-reconnect**: Automatically reconnect when connection is lost
- **Connection monitoring**: Real-time monitoring of connection health
- **Graceful disconnection handling**: Better handling of unexpected disconnections
- **Channel rejoining**: Automatically rejoin channels after reconnection

### 📊 Status and Statistics
- **Session statistics**: Track messages sent/received, uptime, reconnection attempts
- **Connection status**: Monitor connection stability and server response times
- **Uptime tracking**: View total session time and connection duration

### ⚙️ Configuration Management
- **JSON configuration files**: Save and load settings from files
- **Command-line arguments**: Override settings via command line
- **Runtime configuration**: Change settings while the client is running

### 🎨 Enhanced User Experience
- **Improved message formatting**: Better visual organization of chat messages
- **Status messages**: Informative messages about connection events and user actions
- **Enhanced help system**: More detailed command documentation and examples

## Usage Examples

### Basic Usage
```bash
# Start with default settings
python3 tests/test_stage5.py

# Connect to a different server
python3 tests/test_stage5.py -s irc.freenode.net

# Use a custom nickname
python3 tests/test_stage5.py -n MyNickname

# Enable auto-reconnect
python3 tests/test_stage5.py --auto-reconnect
```

### Configuration File Usage
```bash
# Use a configuration file
python3 tests/test_stage5.py -c config/example_config.json

# Connect with custom settings and save config
python3 tests/test_stage5.py -n MyBot --auto-reconnect -c my_config.json
```

### Advanced Options
```bash
# Full feature demonstration
python3 tests/test_stage5.py \
  --server irc.libera.chat \
  --nickname StableBot \
  --channel "#mychannel" \
  --auto-reconnect \
  --reconnect-delay 15 \
  --max-reconnect 10 \
  --config my_settings.json \
  --debug
```

## New Commands

### Status and Information Commands
- `/status` - Show detailed connection and session status
- `/stats` - Display session statistics (messages, uptime, etc.)
- `/uptime` - Show current session uptime
- `/reconnect` - Manually reconnect to the server

### Configuration Commands
- `/config show` - Display current configuration settings
- `/config save [filename]` - Save current settings to file
- `/config toggle reconnect` - Toggle auto-reconnect on/off
- `/config toggle status` - Toggle status messages on/off

## Configuration File Format

Example `config.json`:
```json
{
  "server": "irc.libera.chat",
  "port": 6667,
  "nickname": "MyBot",
  "username": "myuser",
  "realname": "My IRC Bot",
  "auto_reconnect": true,
  "reconnect_delay": 30,
  "show_status_messages": true
}
```

## Command Line Arguments

```
Usage: test_stage5.py [options]

Connection Options:
  -s, --server SERVER       IRC server (default: irc.libera.chat)
  -p, --port PORT          Port number (default: 6667)
  -n, --nickname NICK      Your nickname
  --channel CHANNEL        Initial channel to join

Reliability Options:
  --auto-reconnect         Enable automatic reconnection
  --reconnect-delay SEC    Delay between reconnect attempts (default: 30)
  --max-reconnect NUM      Maximum reconnect attempts (default: 5)

Configuration Options:
  -c, --config FILE        Configuration file to use
  --no-status             Disable status messages
  --debug                 Enable debug mode

Examples:
  python test_stage5.py                           # Basic usage
  python test_stage5.py -s irc.freenode.net      # Different server
  python test_stage5.py -n MyNick -c config.json # Custom nick and config
  python test_stage5.py --auto-reconnect         # Enable auto-reconnect
```

## Enhanced Message Display

Stage 5 improves message formatting with:
- Better timestamp alignment
- Enhanced action message display
- Clear join/part/quit notifications
- Improved visual organization

Example output:
```
                                        [12:34] <User1> Hello everyone!
                                        [12:34] * ActionUser waves
                                        [12:35] → NewUser joined #channel
                                        [12:35] <User2> Welcome!
                                        [12:36] ← OldUser left #channel (Goodbye!)
```

## Status Monitoring

The client now provides comprehensive status information:

```
📊 IRC Client Status:
   🌐 Server: irc.libera.chat:6667
   👤 Nickname: StableBot
   📺 Current Channel: #bottest
   📱 Joined Channels: #bottest, #mychannel
   ⏱️  Uptime: 1:23:45
   📤 Messages Sent: 42
   📥 Messages Received: 156
   🔗 Connection: Stable
   🔄 Auto-reconnect: Enabled
```

## Troubleshooting

### Connection Issues
- Use `--debug` flag for detailed connection information
- Check `/status` command for connection health
- Enable `--auto-reconnect` for automatic recovery

### Configuration Problems
- Use `/config show` to verify current settings
- Check JSON syntax if using configuration files
- Use `/config save` to create a working configuration

### Performance Issues
- Monitor `/stats` for message counts and timing
- Use `/uptime` to check session stability
- Consider reducing reconnect attempts if experiencing issues
