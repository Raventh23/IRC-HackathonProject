# IRC Client Test Suite

This directory contains comprehensive tests for the IRC Chat Client project.

## Test Files

### Unit Tests
- **`test_unit_core.py`** - Core functionality unit tests (50 tests)
  - Message parsing and formatting
  - Nickname and channel name validation
  - Message sanitization and security
  - Command validation
  - Client initialization
  - Timestamp formatting
  - Buffer handling

### Integration Tests
- **`test_connection.py`** - Basic connection error handling
- **`test_message_handling.py`** - Message handling with live server
- **`test_stage3.py`** - Stage 3 development tests
- **`test_stage4.py`** - Stage 4 development tests
- **`test_stage4_automated.py`** - Automated stage 4 tests
- **`test_stage4_validation.py`** - Stage 4 validation tests
- **`test_stage5.py`** - Stage 5 development tests
- **`test_stage5_automated.py`** - Automated stage 5 tests
- **`test_interactive.py`** - Interactive session tests

## Running Tests

### Prerequisites

Install pytest (if not already installed):
```bash
pip install -r requirements.txt
```

### Run All Unit Tests

```bash
# Run all unit tests with verbose output
python -m pytest tests/test_unit_core.py -v

# Run unit tests in quiet mode
python -m pytest tests/test_unit_core.py -q

# Run all tests in the tests directory
python -m pytest tests/ -v
```

### Run Specific Test Classes

```bash
# Run only message parsing tests
python -m pytest tests/test_unit_core.py::TestMessageParsing -v

# Run only nickname validation tests
python -m pytest tests/test_unit_core.py::TestNicknameValidation -v

# Run only channel validation tests
python -m pytest tests/test_unit_core.py::TestChannelNameValidation -v
```

### Run Specific Individual Tests

```bash
# Run a specific test
python -m pytest tests/test_unit_core.py::TestMessageParsing::test_parse_privmsg_with_prefix -v
```

### Run Integration Tests

```bash
# Run specific integration test files
python tests/test_connection.py
python tests/test_stage5_automated.py
```

## Test Coverage

### Core Functionality (test_unit_core.py)

| Test Class | Tests | Coverage |
|------------|-------|----------|
| `TestMessageParsing` | 8 | IRC message parsing with various formats |
| `TestNicknameValidation` | 9 | RFC-compliant nickname validation |
| `TestChannelNameValidation` | 7 | IRC channel name validation |
| `TestMessageSanitization` | 6 | Security and message sanitization |
| `TestCommandValidation` | 8 | User command validation |
| `TestMessageFormatting` | 6 | Message display formatting |
| `TestTimestampFormatting` | 1 | Time formatting utilities |
| `TestClientInitialization` | 3 | Client initialization options |
| `TestBufferHandling` | 2 | Message buffer management |
| **Total** | **50** | **Comprehensive core coverage** |

### Key Features Tested

#### Message Parsing ✅
- PING/PONG messages
- PRIVMSG with prefixes
- Numeric replies (001, 251, etc.)
- JOIN, PART, QUIT messages
- MODE messages
- Empty/malformed messages

#### Validation ✅
- Nickname validation (length, format, reserved names)
- Channel name validation (format, special characters)
- Message sanitization (control characters, CTCP, length)
- Command validation (valid/invalid commands)

#### Security ✅
- IRC injection prevention
- Control character removal
- Message length limits
- Reserved nickname protection

#### Display Formatting ✅
- PRIVMSG formatting
- ACTION (/me) message formatting
- JOIN/PART/QUIT notifications
- Timestamp formatting

## Writing New Tests

### Test Structure

Follow the existing pattern for unit tests:

```python
class TestYourFeature:
    """Test description."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = IRCClient()
    
    def test_specific_behavior(self):
        """Test specific behavior description."""
        # Arrange
        input_data = "test input"
        
        # Act
        result = self.client.some_method(input_data)
        
        # Assert
        assert result == expected_value
```

### Test Naming Convention

- Use descriptive test names: `test_<feature>_<scenario>`
- Examples:
  - `test_validate_nickname_with_numbers`
  - `test_parse_privmsg_with_prefix`
  - `test_sanitize_empty_message`

### Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Test one specific behavior per test
3. **Completeness**: Test both valid and invalid inputs
4. **Documentation**: Include docstrings for test classes and methods
5. **Assertion**: Use clear, specific assertions

## Test Results

All 50 unit tests currently pass:
```
================================================== 50 passed in 0.11s ==================================================
```

## Continuous Integration

These tests are designed to:
- Run quickly (no network dependencies for unit tests)
- Be reliable (deterministic results)
- Catch regressions early
- Document expected behavior

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're running from the project root:
```bash
cd /path/to/IRC-HackathonProject
python -m pytest tests/test_unit_core.py -v
```

### Pytest Not Found

Install pytest:
```bash
pip install pytest
```

### Tests Fail

1. Check Python version (3.7+ required)
2. Ensure all dependencies are installed
3. Run tests with verbose output: `pytest -v`
4. Check individual test output for specific failures

## Future Enhancements

Potential areas for additional testing:
- [ ] Network connection mocking for integration tests
- [ ] Multi-threading behavior tests
- [ ] Auto-reconnection logic tests
- [ ] Configuration file handling tests
- [ ] Command history and logging tests
- [ ] Performance and stress tests

## Contributing

When adding new features:
1. Write unit tests for new functionality
2. Ensure all existing tests still pass
3. Follow the established test structure
4. Update this README if adding new test files

---

For more information about the IRC client, see the main [README.md](../README.md).
