#!/usr/bin/env python3
"""
Unit tests for IRC client core functionality.
Tests the key methods without requiring network connections.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        msg = self.client.parse_message("PING :server.example.com")
        assert msg['command'] == 'PING'
        assert msg['trailing'] == 'server.example.com'
        assert msg['params'] == []
    
    def test_parse_privmsg_with_prefix(self):
        """Test parsing a PRIVMSG with prefix."""
        msg = self.client.parse_message(":nick!user@host PRIVMSG #channel :Hello world")
        assert msg['command'] == 'PRIVMSG'
        assert msg['nick'] == 'nick'
        assert msg['params'] == ['#channel']
        assert msg['trailing'] == 'Hello world'
        assert msg['host'] == 'host'
    
    def test_parse_numeric_reply(self):
        """Test parsing numeric IRC replies."""
        msg = self.client.parse_message(":server.com 001 nickname :Welcome to IRC")
        assert msg['command'] == '001'
        assert msg['params'] == ['nickname']
        assert msg['trailing'] == 'Welcome to IRC'
    
    def test_parse_join_message(self):
        """Test parsing a JOIN message."""
        msg = self.client.parse_message(":alice!user@host JOIN #test")
        assert msg['command'] == 'JOIN'
        assert msg['nick'] == 'alice'
        assert msg['params'] == ['#test']
    
    def test_parse_quit_message(self):
        """Test parsing a QUIT message."""
        msg = self.client.parse_message(":bob!user@host QUIT :Goodbye!")
        assert msg['command'] == 'QUIT'
        assert msg['nick'] == 'bob'
        assert msg['trailing'] == 'Goodbye!'
    
    def test_parse_part_message(self):
        """Test parsing a PART message."""
        msg = self.client.parse_message(":charlie!user@host PART #channel :Leaving")
        assert msg['command'] == 'PART'
        assert msg['nick'] == 'charlie'
        assert msg['params'] == ['#channel']
        assert msg['trailing'] == 'Leaving'
    
    def test_parse_mode_message(self):
        """Test parsing a MODE message."""
        msg = self.client.parse_message(":server.com MODE #channel +o alice")
        assert msg['command'] == 'MODE'
        assert msg['params'] == ['#channel', '+o', 'alice']
    
    def test_parse_empty_message(self):
        """Test parsing an empty or malformed message."""
        msg = self.client.parse_message("")
        assert msg['command'] == ''
        assert msg['params'] == []


class TestNicknameValidation:
    """Test nickname validation functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_valid_simple_nickname(self):
        """Test a simple valid nickname."""
        valid, error = self.client.validate_nickname("Alice")
        assert valid is True
        assert error == ""
    
    def test_valid_nickname_with_numbers(self):
        """Test valid nickname with numbers."""
        valid, error = self.client.validate_nickname("User123")
        assert valid is True
        assert error == ""
    
    def test_valid_nickname_with_special_chars(self):
        """Test valid nickname with allowed special characters."""
        valid, error = self.client.validate_nickname("User_Bot")
        assert valid is True
    
    def test_nickname_too_long(self):
        """Test nickname that exceeds maximum length."""
        valid, error = self.client.validate_nickname("VeryLongNicknameExceeding16Chars")
        assert valid is False
        assert "too long" in error.lower()
    
    def test_empty_nickname(self):
        """Test empty nickname."""
        valid, error = self.client.validate_nickname("")
        assert valid is False
        assert "cannot be empty" in error.lower()
    
    def test_nickname_starting_with_number(self):
        """Test invalid nickname starting with a number."""
        valid, error = self.client.validate_nickname("123User")
        assert valid is False
        assert "invalid" in error.lower()
    
    def test_reserved_nickname_nickserv(self):
        """Test reserved service nickname."""
        valid, error = self.client.validate_nickname("NickServ")
        assert valid is False
        assert "reserved" in error.lower()
    
    def test_reserved_nickname_chanserv(self):
        """Test another reserved service nickname."""
        valid, error = self.client.validate_nickname("chanserv")
        assert valid is False
        assert "reserved" in error.lower()
    
    def test_nickname_with_brackets(self):
        """Test nickname with bracket characters (allowed in IRC)."""
        valid, error = self.client.validate_nickname("Test[Bot]")
        assert valid is True


class TestChannelNameValidation:
    """Test channel name validation functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_valid_channel_with_hash(self):
        """Test valid channel name with # prefix."""
        valid, channel = self.client.validate_channel_name("#test")
        assert valid is True
        assert channel == "#test"
    
    def test_valid_channel_without_hash(self):
        """Test valid channel name auto-adds # prefix."""
        valid, channel = self.client.validate_channel_name("python")
        assert valid is True
        assert channel == "#python"
    
    def test_empty_channel_name(self):
        """Test empty channel name."""
        valid, error = self.client.validate_channel_name("")
        assert valid is False
        assert "cannot be empty" in error.lower()
    
    def test_channel_with_space(self):
        """Test invalid channel name with space."""
        valid, error = self.client.validate_channel_name("#test channel")
        assert valid is False
        assert "invalid" in error.lower()
    
    def test_channel_with_comma(self):
        """Test invalid channel name with comma."""
        valid, error = self.client.validate_channel_name("#test,room")
        assert valid is False
        assert "invalid" in error.lower()
    
    def test_channel_too_long(self):
        """Test channel name that exceeds maximum length."""
        long_name = "#" + "a" * 50
        valid, error = self.client.validate_channel_name(long_name)
        assert valid is False
        assert "invalid" in error.lower()
    
    def test_valid_channel_with_dash(self):
        """Test valid channel with dash."""
        valid, channel = self.client.validate_channel_name("#test-room")
        assert valid is True
        assert channel == "#test-room"


class TestMessageSanitization:
    """Test message sanitization functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_sanitize_normal_message(self):
        """Test sanitizing a normal message."""
        valid, sanitized = self.client.sanitize_message("Hello, world!")
        assert valid is True
        assert sanitized == "Hello, world!"
    
    def test_sanitize_empty_message(self):
        """Test sanitizing an empty message."""
        valid, error = self.client.sanitize_message("")
        assert valid is False
        assert "cannot be empty" in error.lower()
    
    def test_sanitize_action_message(self):
        """Test sanitizing an ACTION message (should preserve)."""
        action_msg = "\x01ACTION waves hello\x01"
        valid, sanitized = self.client.sanitize_message(action_msg)
        assert valid is True
        assert sanitized == action_msg
    
    def test_sanitize_removes_control_chars(self):
        """Test that control characters are removed."""
        msg_with_ctrl = "Hello\x00\x07World"
        valid, sanitized = self.client.sanitize_message(msg_with_ctrl)
        assert valid is True
        assert "\x00" not in sanitized
        assert "\x07" not in sanitized
    
    def test_sanitize_invalid_ctcp(self):
        """Test that invalid CTCP characters are removed."""
        invalid_ctcp = "Test \x01VERSION\x01 message"
        valid, sanitized = self.client.sanitize_message(invalid_ctcp)
        # Control characters are removed, making the message valid
        assert valid is True
        # The \x01 characters should be removed
        assert "\x01" not in sanitized
        assert "VERSION" in sanitized
    
    def test_sanitize_very_long_message(self):
        """Test that extremely long messages are truncated."""
        long_msg = "A" * 500
        valid, sanitized = self.client.sanitize_message(long_msg)
        assert valid is True
        assert len(sanitized) <= 400


class TestCommandValidation:
    """Test command validation functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_valid_quit_command(self):
        """Test valid /quit command."""
        assert self.client.is_valid_user_command("/quit") is True
    
    def test_valid_join_command(self):
        """Test valid /join command."""
        assert self.client.is_valid_user_command("/join #test") is True
    
    def test_valid_nick_command(self):
        """Test valid /nick command."""
        assert self.client.is_valid_user_command("/nick NewName") is True
    
    def test_valid_help_command(self):
        """Test valid /help command."""
        assert self.client.is_valid_user_command("/help") is True
    
    def test_invalid_command(self):
        """Test invalid command."""
        assert self.client.is_valid_user_command("/invalid") is False
    
    def test_not_a_command(self):
        """Test regular message (not a command)."""
        assert self.client.is_valid_user_command("Hello world") is False
    
    def test_valid_me_command(self):
        """Test valid /me command."""
        assert self.client.is_valid_user_command("/me waves") is True
    
    def test_valid_msg_command(self):
        """Test valid /msg command."""
        assert self.client.is_valid_user_command("/msg user Hello") is True


class TestMessageFormatting:
    """Test message formatting functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_format_privmsg(self):
        """Test formatting a PRIVMSG."""
        msg = {
            'command': 'PRIVMSG',
            'params': ['#test'],
            'nick': 'alice',
            'trailing': 'Hello everyone!'
        }
        formatted = self.client.format_channel_message(msg)
        assert formatted is not None
        assert 'alice' in formatted
        assert 'Hello everyone!' in formatted
        assert '<alice>' in formatted
    
    def test_format_action_message(self):
        """Test formatting an ACTION message (/me)."""
        msg = {
            'command': 'PRIVMSG',
            'params': ['#test'],
            'nick': 'bob',
            'trailing': '\x01ACTION waves hello\x01'
        }
        formatted = self.client.format_channel_message(msg)
        assert formatted is not None
        assert '* bob waves hello' in formatted
        assert '\x01' not in formatted  # Control chars should be removed from display
    
    def test_format_join_message(self):
        """Test formatting a JOIN message."""
        msg = {
            'command': 'JOIN',
            'params': ['#test'],
            'nick': 'charlie',
            'trailing': ''
        }
        formatted = self.client.format_channel_message(msg)
        assert formatted is not None
        assert 'charlie' in formatted
        assert 'joined' in formatted.lower()
        assert '#test' in formatted
    
    def test_format_part_message(self):
        """Test formatting a PART message."""
        msg = {
            'command': 'PART',
            'params': ['#test'],
            'nick': 'david',
            'trailing': 'Goodbye!'
        }
        formatted = self.client.format_channel_message(msg)
        assert formatted is not None
        assert 'david' in formatted
        assert 'left' in formatted.lower()
        assert 'Goodbye!' in formatted
    
    def test_format_quit_message(self):
        """Test formatting a QUIT message."""
        msg = {
            'command': 'QUIT',
            'params': [],
            'nick': 'eve',
            'trailing': 'Connection reset'
        }
        formatted = self.client.format_channel_message(msg)
        assert formatted is not None
        assert 'eve' in formatted
        assert 'quit' in formatted.lower()
        assert 'Connection reset' in formatted
    
    def test_format_unknown_message(self):
        """Test formatting an unknown message type."""
        msg = {
            'command': 'UNKNOWN',
            'params': [],
            'nick': '',
            'trailing': ''
        }
        formatted = self.client.format_channel_message(msg)
        assert formatted is None


class TestTimestampFormatting:
    """Test timestamp formatting functionality."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_timestamp_format(self):
        """Test that timestamp is in HH:MM format."""
        timestamp = self.client.format_timestamp()
        assert isinstance(timestamp, str)
        assert len(timestamp) == 5  # HH:MM is 5 characters
        assert ':' in timestamp
        # Validate HH:MM format
        parts = timestamp.split(':')
        assert len(parts) == 2
        assert parts[0].isdigit() and len(parts[0]) == 2  # Hours
        assert parts[1].isdigit() and len(parts[1]) == 2  # Minutes


class TestClientInitialization:
    """Test IRC client initialization."""
    
    def test_default_initialization(self):
        """Test client initialization with default values."""
        client = IRCClient()
        assert client.server == "irc.libera.chat"
        assert client.port == 6667
        assert client.nickname == "SimpleBot"
        assert client.connected is False
        assert client.registered is False
    
    def test_custom_initialization(self):
        """Test client initialization with custom values."""
        client = IRCClient(
            server="irc.example.com",
            port=6697,
            nickname="TestBot",
            debug=True
        )
        assert client.server == "irc.example.com"
        assert client.port == 6697
        assert client.nickname == "TestBot"
        assert client.debug is True
    
    def test_auto_reconnect_initialization(self):
        """Test client initialization with auto-reconnect enabled."""
        client = IRCClient(auto_reconnect=True)
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
        assert self.client.buffer == ""
    
    def test_buffer_stores_incomplete_data(self):
        """Test that buffer can store incomplete message data."""
        # Simulate incomplete data
        self.client.buffer = "PING :incomplete"
        assert "incomplete" in self.client.buffer


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
