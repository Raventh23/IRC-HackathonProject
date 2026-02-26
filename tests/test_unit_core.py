#!/usr/bin/env python3
"""
Unit tests for IRC client core functionality.
Tests the key methods without requiring network connections.
"""

import pytest
from src.irc_client import IRCClient
from datetime import datetime


class TestMessageParsing:
    """Test IRC message parsing functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_parse_simple_command(self):
        """Test parsing a simple command without parameters."""
        # Arrange: Create a simple PING command with trailing parameter
        raw_message = "PING :server.example.com"
        
        # Act: Parse the IRC message
        msg = self.client.parse_message(raw_message)
        
        # Assert: Verify all components are extracted correctly
        assert msg['command'] == 'PING'
        assert msg['trailing'] == 'server.example.com'
        assert msg['params'] == []
    
    def test_parse_privmsg_with_prefix(self):
        """Test parsing a PRIVMSG with prefix."""
        # Arrange: Create a PRIVMSG with full prefix (nick!user@host)
        raw_message = ":nick!user@host PRIVMSG #channel :Hello world"
        
        # Act: Parse the message
        msg = self.client.parse_message(raw_message)
        
        # Assert: Verify command, nick extraction, params, and trailing message
        assert msg['command'] == 'PRIVMSG'
        assert msg['nick'] == 'nick'  # Extracted from prefix
        assert msg['params'] == ['#channel']
        assert msg['trailing'] == 'Hello world'
        assert msg['host'] == 'host'  # Extracted from prefix
    
    def test_parse_numeric_reply(self):
        """Test parsing numeric IRC replies."""
        # Arrange: Create a numeric reply (001 = RPL_WELCOME)
        raw_message = ":server.com 001 nickname :Welcome to IRC"
        
        # Act: Parse the numeric reply
        msg = self.client.parse_message(raw_message)
        
        # Assert: Verify numeric command and parameters are extracted
        assert msg['command'] == '001'
        assert msg['params'] == ['nickname']
        assert msg['trailing'] == 'Welcome to IRC'
    
    def test_parse_join_message(self):
        """Test parsing a JOIN message."""
        # Arrange: Create a JOIN message from user alice
        raw_message = ":alice!user@host JOIN #test"
        
        # Act: Parse the JOIN message
        msg = self.client.parse_message(raw_message)
        
        # Assert: Verify JOIN command and channel are extracted
        assert msg['command'] == 'JOIN'
        assert msg['nick'] == 'alice'
        assert msg['params'] == ['#test']
    
    def test_parse_quit_message(self):
        """Test parsing a QUIT message."""
        # Arrange: Create a QUIT message with quit reason
        raw_message = ":bob!user@host QUIT :Goodbye!"
        
        # Act: Parse the QUIT message
        msg = self.client.parse_message(raw_message)
        
        # Assert: Verify QUIT command and quit message are extracted
        assert msg['command'] == 'QUIT'
        assert msg['nick'] == 'bob'
        assert msg['trailing'] == 'Goodbye!'
    
    def test_parse_part_message(self):
        """Test parsing a PART message."""
        # Arrange: Create a PART message with optional part reason
        raw_message = ":charlie!user@host PART #channel :Leaving"
        
        # Act: Parse the PART message
        msg = self.client.parse_message(raw_message)
        
        # Assert: Verify PART command, channel, and reason are extracted
        assert msg['command'] == 'PART'
        assert msg['nick'] == 'charlie'
        assert msg['params'] == ['#channel']
        assert msg['trailing'] == 'Leaving'
    
    def test_parse_mode_message(self):
        """Test parsing a MODE message."""
        # Arrange: Create a MODE message giving operator status
        raw_message = ":server.com MODE #channel +o alice"
        
        # Act: Parse the MODE message
        msg = self.client.parse_message(raw_message)
        
        # Assert: Verify MODE command and all parameters (channel, mode, target)
        assert msg['command'] == 'MODE'
        assert msg['params'] == ['#channel', '+o', 'alice']
    
    def test_parse_empty_message(self):
        """Test parsing an empty or malformed message."""
        # Arrange: Create an empty message string
        raw_message = ""
        
        # Act: Parse the empty message
        msg = self.client.parse_message(raw_message)
        
        # Assert: Verify parser handles empty input gracefully
        assert msg['command'] == ''
        assert msg['params'] == []


class TestNicknameValidation:
    """Test nickname validation functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_valid_simple_nickname(self):
        """Test a simple valid nickname."""
        # Arrange: Create a simple, valid nickname
        nickname = "Alice"
        
        # Act: Validate the nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Nickname should be valid with no error
        assert valid is True
        assert error == ""
    
    def test_valid_nickname_with_numbers(self):
        """Test valid nickname with numbers."""
        # Arrange: Create a nickname containing numbers
        nickname = "User123"
        
        # Act: Validate the nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Nickname with numbers should be valid
        assert valid is True
        assert error == ""
    
    def test_valid_nickname_with_special_chars(self):
        """Test valid nickname with allowed special characters."""
        # Arrange: Create a nickname with underscore (allowed in IRC)
        nickname = "User_Bot"
        
        # Act: Validate the nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Nickname with allowed special chars should be valid
        assert valid is True
    
    def test_nickname_too_long(self):
        """Test nickname that exceeds maximum length."""
        # Arrange: Create a nickname longer than 16 characters (IRC max)
        nickname = "VeryLongNicknameExceeding16Chars"
        
        # Act: Validate the nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Should be invalid with appropriate error message
        assert valid is False
        assert "too long" in error.lower()
    
    def test_empty_nickname(self):
        """Test empty nickname."""
        # Arrange: Create an empty nickname string
        nickname = ""
        
        # Act: Validate the empty nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Should be invalid with appropriate error
        assert valid is False
        assert "cannot be empty" in error.lower()
    
    def test_nickname_starting_with_number(self):
        """Test invalid nickname starting with a number."""
        # Arrange: Create a nickname starting with a digit (RFC violation)
        nickname = "123User"
        
        # Act: Validate the nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Should be invalid per IRC RFC
        assert valid is False
        assert "invalid" in error.lower()
    
    def test_reserved_nickname_nickserv(self):
        """Test reserved service nickname."""
        # Arrange: Attempt to use NickServ (reserved IRC service name)
        nickname = "NickServ"
        
        # Act: Validate the reserved nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Should be rejected as reserved
        assert valid is False
        assert "reserved" in error.lower()
    
    def test_reserved_nickname_chanserv(self):
        """Test another reserved service nickname."""
        # Arrange: Attempt to use chanserv (case-insensitive check)
        nickname = "chanserv"
        
        # Act: Validate the reserved nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Should be rejected as reserved
        assert valid is False
        assert "reserved" in error.lower()
    
    def test_nickname_with_brackets(self):
        """Test nickname with bracket characters (allowed in IRC)."""
        # Arrange: Create a nickname with brackets (valid per IRC RFC)
        nickname = "Test[Bot]"
        
        # Act: Validate the nickname
        valid, error = self.client.validate_nickname(nickname)
        
        # Assert: Brackets are allowed in IRC nicknames
        assert valid is True


class TestChannelNameValidation:
    """Test channel name validation functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_valid_channel_with_hash(self):
        """Test valid channel name with # prefix."""
        # Arrange: Create a channel name with proper # prefix
        channel_name = "#test"
        
        # Act: Validate the channel name
        valid, channel = self.client.validate_channel_name(channel_name)
        
        # Assert: Should be valid and unchanged
        assert valid is True
        assert channel == "#test"
    
    def test_valid_channel_without_hash(self):
        """Test valid channel name auto-adds # prefix."""
        # Arrange: Create a channel name without # prefix
        channel_name = "python"
        
        # Act: Validate the channel name
        valid, channel = self.client.validate_channel_name(channel_name)
        
        # Assert: Should be valid with # auto-added
        assert valid is True
        assert channel == "#python"
    
    def test_empty_channel_name(self):
        """Test empty channel name."""
        # Arrange: Create an empty channel name
        channel_name = ""
        
        # Act: Validate the empty channel name
        valid, error = self.client.validate_channel_name(channel_name)
        
        # Assert: Should be invalid
        assert valid is False
        assert "cannot be empty" in error.lower()
    
    def test_channel_with_space(self):
        """Test invalid channel name with space."""
        # Arrange: Create a channel name with space (not allowed per RFC)
        channel_name = "#test channel"
        
        # Act: Validate the channel name
        valid, error = self.client.validate_channel_name(channel_name)
        
        # Assert: Should be invalid
        assert valid is False
        assert "invalid" in error.lower()
    
    def test_channel_with_comma(self):
        """Test invalid channel name with comma."""
        # Arrange: Create a channel name with comma (not allowed per RFC)
        channel_name = "#test,room"
        
        # Act: Validate the channel name
        valid, error = self.client.validate_channel_name(channel_name)
        
        # Assert: Should be invalid
        assert valid is False
        assert "invalid" in error.lower()
    
    def test_channel_too_long(self):
        """Test channel name that exceeds maximum length."""
        # Arrange: Create a channel name longer than 50 chars (IRC limit)
        long_name = "#" + "a" * 50
        
        # Act: Validate the overly long channel name
        valid, error = self.client.validate_channel_name(long_name)
        
        # Assert: Should be invalid
        assert valid is False
        assert "invalid" in error.lower()
    
    def test_valid_channel_with_dash(self):
        """Test valid channel with dash."""
        # Arrange: Create a channel name with dash (allowed in IRC)
        channel_name = "#test-room"
        
        # Act: Validate the channel name
        valid, channel = self.client.validate_channel_name(channel_name)
        
        # Assert: Should be valid
        assert valid is True
        assert channel == "#test-room"


class TestMessageSanitization:
    """Test message sanitization functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_sanitize_normal_message(self):
        """Test sanitizing a normal message."""
        # Arrange: Create a normal message with no special characters
        message = "Hello, world!"
        
        # Act: Sanitize the message
        valid, sanitized = self.client.sanitize_message(message)
        
        # Assert: Should be valid and unchanged
        assert valid is True
        assert sanitized == "Hello, world!"
    
    def test_sanitize_empty_message(self):
        """Test sanitizing an empty message."""
        # Arrange: Create an empty message
        message = ""
        
        # Act: Sanitize the empty message
        valid, error = self.client.sanitize_message(message)
        
        # Assert: Should be invalid
        assert valid is False
        assert "cannot be empty" in error.lower()
    
    def test_sanitize_action_message(self):
        """Test sanitizing an ACTION message (should preserve)."""
        # Arrange: Create an IRC ACTION message (/me command)
        action_msg = "\x01ACTION waves hello\x01"
        
        # Act: Sanitize the ACTION message
        valid, sanitized = self.client.sanitize_message(action_msg)
        
        # Assert: ACTION messages should be preserved as-is
        assert valid is True
        assert sanitized == action_msg
    
    def test_sanitize_removes_control_chars(self):
        """Test that control characters are removed."""
        # Arrange: Create a message with control characters (security risk)
        msg_with_ctrl = "Hello\x00\x07World"
        
        # Act: Sanitize the message
        valid, sanitized = self.client.sanitize_message(msg_with_ctrl)
        
        # Assert: Control chars should be removed
        assert valid is True
        assert "\x00" not in sanitized  # NULL removed
        assert "\x07" not in sanitized  # BELL removed
    
    def test_sanitize_invalid_ctcp(self):
        """Test that invalid CTCP characters are removed."""
        # Arrange: Create a message with CTCP injection attempt
        invalid_ctcp = "Test \x01VERSION\x01 message"
        
        # Act: Sanitize the message
        valid, sanitized = self.client.sanitize_message(invalid_ctcp)
        
        # Assert: Control characters are removed, making the message valid
        assert valid is True
        assert "\x01" not in sanitized  # CTCP delimiters removed
        assert "VERSION" in sanitized    # Text content preserved
    
    def test_sanitize_very_long_message(self):
        """Test that extremely long messages are truncated."""
        # Arrange: Create a message exceeding the 400 byte limit
        long_msg = "A" * 500
        
        # Act: Sanitize the overly long message
        valid, sanitized = self.client.sanitize_message(long_msg)
        
        # Assert: Should be truncated to safe length
        assert valid is True
        assert len(sanitized) <= 400  # Maximum safe IRC message length


class TestCommandValidation:
    """Test command validation functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_valid_quit_command(self):
        """Test valid /quit command."""
        # Arrange: Create a /quit command
        command = "/quit"
        
        # Act: Validate the command
        result = self.client.is_valid_user_command(command)
        
        # Assert: Should be recognized as valid
        assert result is True
    
    def test_valid_join_command(self):
        """Test valid /join command."""
        # Arrange: Create a /join command with channel parameter
        command = "/join #test"
        
        # Act: Validate the command
        result = self.client.is_valid_user_command(command)
        
        # Assert: Should be recognized as valid
        assert result is True
    
    def test_valid_nick_command(self):
        """Test valid /nick command."""
        # Arrange: Create a /nick command to change nickname
        command = "/nick NewName"
        
        # Act: Validate the command
        result = self.client.is_valid_user_command(command)
        
        # Assert: Should be recognized as valid
        assert result is True
    
    def test_valid_help_command(self):
        """Test valid /help command."""
        # Arrange: Create a /help command
        command = "/help"
        
        # Act: Validate the command
        result = self.client.is_valid_user_command(command)
        
        # Assert: Should be recognized as valid
        assert result is True
    
    def test_invalid_command(self):
        """Test invalid command."""
        # Arrange: Create an unrecognized command
        command = "/invalid"
        
        # Act: Validate the command
        result = self.client.is_valid_user_command(command)
        
        # Assert: Should not be recognized
        assert result is False
    
    def test_not_a_command(self):
        """Test regular message (not a command)."""
        # Arrange: Create a regular chat message (no / prefix)
        message = "Hello world"
        
        # Act: Validate as command
        result = self.client.is_valid_user_command(message)
        
        # Assert: Should not be recognized as a command
        assert result is False
    
    def test_valid_me_command(self):
        """Test valid /me command."""
        # Arrange: Create a /me action command
        command = "/me waves"
        
        # Act: Validate the command
        result = self.client.is_valid_user_command(command)
        
        # Assert: Should be recognized as valid
        assert result is True
    
    def test_valid_msg_command(self):
        """Test valid /msg command."""
        # Arrange: Create a /msg private message command
        command = "/msg user Hello"
        
        # Act: Validate the command
        result = self.client.is_valid_user_command(command)
        
        # Assert: Should be recognized as valid
        assert result is True


class TestMessageFormatting:
    """Test message formatting functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_format_privmsg(self):
        """Test formatting a PRIVMSG."""
        # Arrange: Create a parsed PRIVMSG structure
        msg = {
            'command': 'PRIVMSG',
            'params': ['#test'],
            'nick': 'alice',
            'trailing': 'Hello everyone!'
        }
        
        # Act: Format the message for display
        formatted = self.client.format_channel_message(msg)
        
        # Assert: Should contain nick and message in proper format
        assert formatted is not None
        assert 'alice' in formatted
        assert 'Hello everyone!' in formatted
        assert '<alice>' in formatted  # Standard IRC format
    
    def test_format_action_message(self):
        """Test formatting an ACTION message (/me)."""
        # Arrange: Create a parsed ACTION message (/me command)
        msg = {
            'command': 'PRIVMSG',
            'params': ['#test'],
            'nick': 'bob',
            'trailing': '\x01ACTION waves hello\x01'
        }
        
        # Act: Format the ACTION message for display
        formatted = self.client.format_channel_message(msg)
        
        # Assert: Should show ACTION format (* user action)
        assert formatted is not None
        assert '* bob waves hello' in formatted
        assert '\x01' not in formatted  # Control chars removed from display
    
    def test_format_join_message(self):
        """Test formatting a JOIN message."""
        # Arrange: Create a parsed JOIN message
        msg = {
            'command': 'JOIN',
            'params': ['#test'],
            'nick': 'charlie',
            'trailing': ''
        }
        
        # Act: Format the JOIN message for display
        formatted = self.client.format_channel_message(msg)
        
        # Assert: Should show user joining the channel
        assert formatted is not None
        assert 'charlie' in formatted
        assert 'joined' in formatted.lower()
        assert '#test' in formatted
    
    def test_format_part_message(self):
        """Test formatting a PART message."""
        # Arrange: Create a parsed PART message with reason
        msg = {
            'command': 'PART',
            'params': ['#test'],
            'nick': 'david',
            'trailing': 'Goodbye!'
        }
        
        # Act: Format the PART message for display
        formatted = self.client.format_channel_message(msg)
        
        # Assert: Should show user leaving with reason
        assert formatted is not None
        assert 'david' in formatted
        assert 'left' in formatted.lower()
        assert 'Goodbye!' in formatted
    
    def test_format_quit_message(self):
        """Test formatting a QUIT message."""
        # Arrange: Create a parsed QUIT message
        msg = {
            'command': 'QUIT',
            'params': [],
            'nick': 'eve',
            'trailing': 'Connection reset'
        }
        
        # Act: Format the QUIT message for display
        formatted = self.client.format_channel_message(msg)
        
        # Assert: Should show user quit message
        assert formatted is not None
        assert 'eve' in formatted
        assert 'quit' in formatted.lower()
        assert 'Connection reset' in formatted
    
    def test_format_unknown_message(self):
        """Test formatting an unknown message type."""
        # Arrange: Create an unrecognized message type
        msg = {
            'command': 'UNKNOWN',
            'params': [],
            'nick': '',
            'trailing': ''
        }
        
        # Act: Attempt to format unknown message
        formatted = self.client.format_channel_message(msg)
        
        # Assert: Should return None for unknown types
        assert formatted is None


class TestTimestampFormatting:
    """Test timestamp formatting functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_timestamp_format(self):
        """Test that timestamp is in HH:MM format."""
        # Arrange & Act: Get current timestamp
        timestamp = self.client.format_timestamp()
        
        # Assert: Should be in HH:MM format
        assert isinstance(timestamp, str)
        assert len(timestamp) == 5  # HH:MM is 5 characters
        assert ':' in timestamp
        
        # Validate HH:MM format components
        parts = timestamp.split(':')
        assert len(parts) == 2
        assert parts[0].isdigit() and len(parts[0]) == 2  # Hours (00-23)
        assert parts[1].isdigit() and len(parts[1]) == 2  # Minutes (00-59)


class TestClientInitialization:
    """Test IRC client initialization."""
    
    def test_default_initialization(self):
        """Test client initialization with default values."""
        # Arrange & Act: Create client with defaults
        client = IRCClient()
        
        # Assert: Should have expected default values
        assert client.server == "irc.libera.chat"
        assert client.port == 6667
        assert client.nickname == "SimpleBot"
        assert client.connected is False
        assert client.registered is False
    
    def test_custom_initialization(self):
        """Test client initialization with custom values."""
        # Arrange & Act: Create client with custom parameters
        client = IRCClient(
            server="irc.example.com",
            port=6697,
            nickname="TestBot",
            debug=True
        )
        
        # Assert: Should use custom values provided
        assert client.server == "irc.example.com"
        assert client.port == 6697
        assert client.nickname == "TestBot"
        assert client.debug is True
    
    def test_auto_reconnect_initialization(self):
        """Test client initialization with auto-reconnect enabled."""
        # Arrange & Act: Create client with auto-reconnect feature
        client = IRCClient(auto_reconnect=True)
        
        # Assert: Should enable auto-reconnect with proper settings
        assert client.auto_reconnect is True
        assert client.max_reconnect_attempts == 5
        assert client.reconnect_delay == 30


class TestBufferHandling:
    """Test message buffer handling."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_initial_buffer_empty(self):
        """Test that buffer is initially empty."""
        # Arrange & Act: Create new client
        # (buffer initialized in setup_method)
        
        # Assert: Buffer should start empty
        assert self.client.buffer == ""
    
    def test_buffer_stores_incomplete_data(self):
        """Test that buffer can store incomplete message data."""
        # Arrange: Simulate incomplete IRC message data
        incomplete_message = "PING :incomplete"
        
        # Act: Store incomplete data in buffer
        self.client.buffer = incomplete_message
        
        # Assert: Buffer should retain the incomplete data
        assert "incomplete" in self.client.buffer
