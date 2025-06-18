# Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Linux (any recent distribution)
- **Python**: Version 3.7 or higher
- **Memory**: 50 MB RAM
- **Storage**: 10 MB disk space
- **Network**: Internet connection for IRC server access

### Recommended Requirements
- **Python**: Version 3.9 or higher
- **Memory**: 100 MB RAM
- **Terminal**: Terminal application with Unicode support

### Dependencies
- **None required** - Uses only Python standard library
- **Optional**: Git for cloning repository

## Installation Methods

### Method 1: Git Clone (Recommended)

**For users familiar with Git:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Raventh23/simple-irc-chat.git
   cd simple-irc-chat
   ```

2. **Verify installation:**
   ```bash
   python3 src/irc_client.py --help
   ```

3. **Test basic functionality:**
   ```bash
   python3 tests/test_stage5.py --help
   ```

### Method 2: Download ZIP

**For users who prefer not to use Git:**

1. **Download ZIP file:**
   - Go to GitHub repository
   - Click "Code" → "Download ZIP"
   - Extract to your preferred directory

2. **Navigate to directory:**
   ```bash
   cd simple-irc-chat-main
   ```

3. **Verify installation:**
   ```bash
   python3 src/irc_client.py
   ```

### Method 3: Manual Download

**Download individual files if needed:**

1. **Create project directory:**
   ```bash
   mkdir simple-irc-chat
   cd simple-irc-chat
   ```

2. **Download main files:**
   - Download `src/irc_client.py`
   - Download `tests/test_stage5.py`
   - Download configuration files as needed

3. **Create directory structure:**
   ```bash
   mkdir src tests config docs
   # Place files in appropriate directories
   ```

## Platform-Specific Installation

### Windows Installation

#### Prerequisites
1. **Install Python:**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify: Open Command Prompt and run `python --version`

#### Installation Steps
1. **Download the project:**
   ```cmd
   # Using Git (if installed)
   git clone https://github.com/Raventh23/simple-irc-chat.git
   cd simple-irc-chat
   
   # Or download and extract ZIP file
   ```

2. **Test installation:**
   ```cmd
   python src\irc_client.py
   # or
   python3 src\irc_client.py
   # or
   py src\irc_client.py
   ```

3. **Create desktop shortcut (optional):**
   - Right-click on desktop → New → Shortcut
   - Target: `python "C:\path\to\simple-irc-chat\tests\test_stage5.py"`
   - Name: "IRC Chat Client"

#### Windows-Specific Notes
- Use backslashes (`\`) for paths in Command Prompt
- Use PowerShell for better Unicode support
- Windows Defender may scan scripts (normal behavior)

### macOS Installation

#### Prerequisites
1. **Python comes pre-installed** on macOS 10.8+
   - Verify: `python3 --version`
   - If missing, install from [python.org](https://www.python.org/downloads/)

2. **Install Git (optional):**
   ```bash
   # Using Homebrew
   brew install git
   
   # Or download from git-scm.com
   ```

#### Installation Steps
1. **Open Terminal** (Applications → Utilities → Terminal)

2. **Navigate to desired directory:**
   ```bash
   cd ~/Documents  # or your preferred location
   ```

3. **Clone repository:**
   ```bash
   git clone https://github.com/Raventh23/simple-irc-chat.git
   cd simple-irc-chat
   ```

4. **Make scripts executable:**
   ```bash
   chmod +x src/irc_client.py
   chmod +x tests/test_stage5.py
   ```

5. **Test installation:**
   ```bash
   python3 tests/test_stage5.py --help
   ```

#### macOS-Specific Notes
- Use `python3` instead of `python`
- Terminal.app supports full Unicode
- Scripts can be run directly: `./tests/test_stage5.py`

### Linux Installation

#### Prerequisites
**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

**CentOS/RHEL/Fedora:**
```bash
# CentOS/RHEL
sudo yum install python3 git
# or Fedora
sudo dnf install python3 git
```

**Arch Linux:**
```bash
sudo pacman -S python git
```

#### Installation Steps
1. **Clone repository:**
   ```bash
   git clone https://github.com/Raventh23/simple-irc-chat.git
   cd simple-irc-chat
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x src/irc_client.py tests/test_stage5.py
   ```

3. **Test installation:**
   ```bash
   python3 tests/test_stage5.py --help
   ```

4. **Create symlink for global access (optional):**
   ```bash
   sudo ln -s $(pwd)/tests/test_stage5.py /usr/local/bin/irc-client
   # Then run from anywhere: irc-client
   ```

#### Linux-Specific Notes
- Most distributions include Python 3
- Use package manager for dependencies
- Scripts can be run directly after `chmod +x`

## Verification and Testing

### Basic Verification

1. **Check Python version:**
   ```bash
   python3 --version
   # Should show 3.7 or higher
   ```

2. **Test basic client:**
   ```bash
   python3 src/irc_client.py
   # Should show connection attempt
   # Press Ctrl+C to exit
   ```

3. **Test enhanced client:**
   ```bash
   python3 tests/test_stage5.py --help
   # Should show help message
   ```

### Connection Test

1. **Test default connection:**
   ```bash
   python3 tests/test_stage5.py
   # Should connect to irc.libera.chat
   # Type /quit to exit
   ```

2. **Test with custom settings:**
   ```bash
   python3 tests/test_stage5.py -n TestUser --debug
   # Should show debug output
   ```

### Feature Testing

1. **Test configuration:**
   ```bash
   python3 tests/test_stage5.py -c config/example_config.json
   ```

2. **Test auto-reconnect:**
   ```bash
   python3 tests/test_stage5.py --auto-reconnect
   ```

3. **Test all command-line options:**
   ```bash
   python3 tests/test_stage5.py --help
   ```

## Configuration Setup

### Create Configuration Directory

```bash
mkdir -p config
```

### Create Basic Configuration

1. **Copy example configuration:**
   ```bash
   cp config/example_config.json config/my_config.json
   ```

2. **Edit configuration:**
   ```json
   {
     "server": "irc.libera.chat",
     "port": 6667,
     "nickname": "YourNickname",
     "username": "yourusername",
     "realname": "Your Real Name",
     "auto_reconnect": true,
     "reconnect_delay": 30,
     "show_status_messages": true
   }
   ```

3. **Test configuration:**
   ```bash
   python3 tests/test_stage5.py -c config/my_config.json
   ```

### Set Default Configuration

**Create shell alias (optional):**

**Bash/Zsh:**
```bash
echo 'alias irc="python3 /path/to/simple-irc-chat/tests/test_stage5.py -c /path/to/config.json"' >> ~/.bashrc
source ~/.bashrc
```

**Fish:**
```bash
echo 'alias irc="python3 /path/to/simple-irc-chat/tests/test_stage5.py -c /path/to/config.json"' >> ~/.config/fish/config.fish
```

## Troubleshooting Installation

### Common Issues

#### Python Not Found
```bash
# Try these variations
python3 tests/test_stage5.py
python tests/test_stage5.py
py tests/test_stage5.py
py -3 tests/test_stage5.py
```

#### Permission Denied
```bash
# Make scripts executable
chmod +x src/irc_client.py
chmod +x tests/test_stage5.py
```

#### Module Not Found
```bash
# Check Python path
python3 -c "import sys; print(sys.path)"

# Run from project directory
cd simple-irc-chat
python3 tests/test_stage5.py
```

#### Git Not Available
- Download ZIP file instead
- Install Git from package manager
- Use browser to download individual files

### Getting Help

If installation fails:

1. **Check system requirements**
2. **Review platform-specific notes**
3. **Try different Python command variants**
4. **Check error messages carefully**
5. **Consult troubleshooting guide**
6. **Report issues on GitHub**

## Next Steps

After successful installation:

1. **Read the User Manual:** `docs/USER_MANUAL.md`
2. **Try the Quick Start guide**
3. **Explore command-line options**
4. **Set up configuration file**
5. **Join IRC channels and start chatting!**

### Recommended First Steps

1. **Test basic connection:**
   ```bash
   python3 tests/test_stage5.py
   ```

2. **Join a beginner-friendly channel:**
   ```bash
   python3 tests/test_stage5.py --channel "#help"
   ```

3. **Learn basic commands:**
   - `/help` - Show all commands
   - `/status` - Check connection
   - `/quit` - Exit client

4. **Create your configuration:**
   ```bash
   # Start client, then use:
   /config save my_config.json
   ```

---

*Installation complete! You're ready to start using the IRC client. Refer to the User Manual for detailed usage instructions.*
