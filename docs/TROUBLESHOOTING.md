# Troubleshooting Guide

## Quick Diagnostics

### Check Your Setup
```bash
# Verify Python version
python3 --version

# Test basic client
python3 src/irc_client.py

# Test enhanced client with debug
python3 tests/test_stage5.py --debug
```

### Common Error Messages

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `Connection failed!` | Network/server issue | Check internet, try different server |
| `Registration failed!` | Server rejected connection | Try different nickname, check server status |
| `Nickname is already in use` | Someone else has that nick | Use `/nick newnickname` |
| `Cannot join channel (+l)` | Channel is full | Try later or different channel |
| `Cannot join channel (+i)` | Invite-only channel | Need invitation from channel op |
| `Cannot join channel (+b)` | You are banned | Contact channel operators |
| `Not in a channel` | Need to join channel first | Use `/join #channelname` |

## Connection Issues

### Cannot Connect to Server

**Symptoms:**
- "Connection failed!" message
- Immediate disconnect
- Timeout errors

**Diagnostic Steps:**
1. **Check internet connection:**
   ```bash
   ping google.com
   ```

2. **Test server availability:**
   ```bash
   telnet irc.libera.chat 6667
   ```

3. **Try different server:**
   ```bash
   python3 tests/test_stage5.py -s irc.oftc.net
   ```

4. **Enable debug mode:**
   ```bash
   python3 tests/test_stage5.py --debug
   ```

**Solutions:**
- Check firewall settings
- Try different IRC server
- Check if port 6667 is blocked
- Use different network connection

### Connection Drops Frequently

**Symptoms:**
- Frequent disconnections
- "Connection lost" messages
- Auto-reconnect constantly triggering

**Diagnostic Steps:**
1. **Check connection stability:**
   ```
   /status
   ```

2. **Monitor PING/PONG:**
   ```bash
   python3 tests/test_stage5.py --debug
   ```

3. **Test with auto-reconnect disabled:**
   ```bash
   python3 tests/test_stage5.py
   ```

**Solutions:**
- Enable auto-reconnect: `--auto-reconnect`
- Increase reconnect delay: `--reconnect-delay 60`
- Check network stability
- Try different IRC server

### Registration Problems

**Symptoms:**
- "Registration failed!" message
- Stuck at registration phase
- Server doesn't respond to NICK/USER

**Diagnostic Steps:**
1. **Check nickname validity:**
   - Must start with letter
   - Only letters, numbers, and some symbols
   - Maximum 16 characters

2. **Try different nickname:**
   ```bash
   python3 tests/test_stage5.py -n TestUser123
   ```

3. **Check server requirements:**
   - Some servers require ident
   - Some have specific policies

**Solutions:**
- Use different nickname
- Try different server
- Check server documentation
- Wait and retry (server may be busy)

## Channel Issues

### Cannot Join Channel

**Error Messages and Solutions:**

**"Cannot join channel (+l)" - Channel is full**
- Solution: Wait and try again later
- Alternative: Find similar channel with space

**"Cannot join channel (+i)" - Invite-only**
- Solution: Contact channel operators for invitation
- Alternative: Look for public channels on same topic

**"Cannot join channel (+k)" - Requires password**
- Solution: Get password from channel operators
- Syntax: `/join #channel password`

**"Cannot join channel (+b)" - You are banned**
- Solution: Contact channel operators
- Alternative: Use different nickname or wait for ban to expire

### Messages Not Sending

**Symptoms:**
- Messages don't appear in channel
- "Not in a channel" error
- Other users can't see your messages

**Diagnostic Steps:**
1. **Check if in channel:**
   ```
   /status
   ```

2. **Verify channel name:**
   - Must start with #
   - Check spelling

3. **Test with simple message:**
   ```
   test message
   ```

**Solutions:**
- Join channel first: `/join #channelname`
- Check if banned or muted
- Verify channel exists
- Try different channel

### Cannot See Messages

**Symptoms:**
- Channel appears empty
- No messages displayed
- Only own messages visible

**Possible Causes:**
- Channel is actually quiet
- Display formatting issues
- Connection problems

**Solutions:**
- Wait for activity in channel
- Check channel topic: some channels are quiet
- Try busy channel like #help
- Restart client

## Performance Issues

### Client Runs Slowly

**Symptoms:**
- Delayed responses
- Slow command execution
- High CPU usage

**Diagnostic Steps:**
1. **Check system resources:**
   ```bash
   top
   # or
   htop
   ```

2. **Monitor network:**
   ```bash
   python3 tests/test_stage5.py --debug
   ```

3. **Test with minimal features:**
   ```bash
   python3 src/irc_client.py
   ```

**Solutions:**
- Close other applications
- Disable debug mode
- Reduce auto-reconnect frequency
- Check network connection quality

### High Memory Usage

**Symptoms:**
- Increasing memory usage over time
- System becomes sluggish
- Out of memory errors

**Solutions:**
- Restart client periodically
- Monitor with `/stats`
- Avoid extremely busy channels
- Report as bug if persistent

## Configuration Issues

### Configuration File Problems

**"Configuration file not found"**
```bash
⚠️ Configuration file config.json not found, using defaults
```

**Solutions:**
1. **Check file path:**
   ```bash
   ls -la config.json
   ```

2. **Use absolute path:**
   ```bash
   python3 tests/test_stage5.py -c /full/path/to/config.json
   ```

3. **Create new configuration:**
   ```
   /config save config.json
   ```

**"Error parsing configuration file"**
```bash
❌ Error parsing configuration file: Expecting ',' delimiter
```

**Solutions:**
1. **Validate JSON syntax:**
   ```bash
   python3 -m json.tool config.json
   ```

2. **Use example configuration:**
   ```bash
   cp config/example_config.json my_config.json
   ```

3. **Fix common JSON errors:**
   - Missing commas between items
   - Trailing commas (not allowed in JSON)
   - Unquoted strings
   - Wrong quote types (use " not ')

### Command Line Argument Issues

**"Unknown argument" errors**
```bash
python3 tests/test_stage5.py --invalid-option
```

**Solution:**
Check available options:
```bash
python3 tests/test_stage5.py --help
```

**Arguments not working as expected**

**Solutions:**
1. **Check argument format:**
   ```bash
   # Correct
   python3 tests/test_stage5.py --server irc.libera.chat
   
   # Incorrect
   python3 tests/test_stage5.py --server=irc.libera.chat
   ```

2. **Use quotes for complex values:**
   ```bash
   python3 tests/test_stage5.py --realname "My Real Name"
   ```

## Platform-Specific Issues

### Windows Issues

**Path separators:**
```bash
# Use forward slashes or double backslashes
python3 tests/test_stage5.py -c config/example_config.json
# or
python3 tests\\test_stage5.py -c config\\example_config.json
```

**Python not found:**
```bash
# Try these variations
python tests/test_stage5.py
py tests/test_stage5.py
py -3 tests/test_stage5.py
```

### macOS Issues

**Permission denied:**
```bash
chmod +x tests/test_stage5.py
python3 tests/test_stage5.py
```

**SSL/certificate issues:**
- Update certificates
- Try different IRC server
- Use non-SSL port (6667 instead of 6697)

### Linux Issues

**Missing Python:**
```bash
# Install Python 3
sudo apt install python3        # Ubuntu/Debian
sudo yum install python3        # CentOS/RHEL
sudo pacman -S python           # Arch Linux
```

**Permission issues:**
```bash
# Make scripts executable
chmod +x tests/test_stage5.py
chmod +x src/irc_client.py
```

## Advanced Troubleshooting

### Debug Mode Analysis

**Enable debug mode:**
```bash
python3 tests/test_stage5.py --debug
```

**What to look for:**
- Raw IRC messages (lines starting with <<<)
- Connection establishment details
- Error stack traces
- Internal state changes

**Common debug patterns:**

**Successful connection:**
```
Connecting to irc.libera.chat:6667...
Connected to irc.libera.chat!
>>> NICK YourNick
>>> USER simple 0 * :Simple IRC Client
<<< :server 001 YourNick :Welcome to...
```

**Failed connection:**
```
Connecting to irc.libera.chat:6667...
❌ Connection failed: [Errno 111] Connection refused
```

**PING/PONG keepalive:**
```
<<< PING :server.name
>>> PONG :server.name
Responded to PING
```

### Network Diagnostics

**Test raw IRC connection:**
```bash
# Connect manually to test server
telnet irc.libera.chat 6667

# Once connected, type:
NICK TestNick
USER test 0 * :Test User
```

**Check DNS resolution:**
```bash
nslookup irc.libera.chat
# or
dig irc.libera.chat
```

**Test different ports:**
```bash
# Standard IRC ports
telnet irc.libera.chat 6667    # Plain
telnet irc.libera.chat 6697    # SSL
telnet irc.libera.chat 8000    # Alternative
```

### Log Analysis

**Enable comprehensive logging:**
```python
# Add to client code for detailed logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('irc_debug.log'),
        logging.StreamHandler()
    ]
)
```

## Getting Help

### Built-in Help

**Use client help system:**
```
/help              # All commands
/help join         # Specific command help
/status            # Current status
/config show       # Configuration
```

### Community Support

**IRC Help Channels:**
- `#help` on irc.libera.chat
- `#new2irc` on various networks
- Server-specific help channels

**GitHub Issues:**
- Report bugs at project repository
- Include debug output
- Describe steps to reproduce

### Self-Help Checklist

Before asking for help:

1. **Check this troubleshooting guide**
2. **Try debug mode:** `--debug`
3. **Test with minimal configuration**
4. **Check network connectivity**
5. **Try different IRC server**
6. **Read error messages carefully**
7. **Check `/status` and `/stats`**

### Reporting Bugs

**Include this information:**
- Operating system and version
- Python version
- Exact command used
- Error messages
- Debug output (if relevant)
- Steps to reproduce

**Example bug report:**
```
Environment:
- OS: macOS 12.6
- Python: 3.9.7
- Command: python3 tests/test_stage5.py --auto-reconnect

Issue:
Auto-reconnect fails after 3 attempts

Error message:
❌ Failed to connect after 3 attempts

Debug output:
[Include relevant debug lines]

Steps to reproduce:
1. Start client with auto-reconnect
2. Disconnect network
3. Wait for reconnection attempts
4. Observe failure after 3 attempts
```

---

*If you encounter issues not covered in this guide, please check the project documentation or report the issue on GitHub.*
