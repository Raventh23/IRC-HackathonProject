# Contributing to Simple IRC Chat Client

Thank you for your interest in contributing to the Simple IRC Chat Client! This document provides guidelines for contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git for version control
- Basic understanding of IRC protocol (helpful but not required)

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/simple-irc-chat.git
   cd simple-irc-chat
   ```
3. **Set up the upstream remote**:
   ```bash
   git remote add upstream https://github.com/Raventh23/simple-irc-chat.git
   ```
4. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
5. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Project Structure

```
simple-irc-chat/
├── src/               # Main source code
│   └── irc_client.py  # Core IRC client implementation
├── tests/             # Test suite
├── docs/              # Documentation
├── config/            # Configuration examples
├── README.md          # Project overview
└── requirements.txt   # Dependencies
```

## Development Process

### Workflow

1. **Create a feature branch** from main:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following our code standards
3. **Test thoroughly** using our test suite
4. **Commit your changes** with clear messages
5. **Push to your fork** and create a pull request

### Branch Naming

- `feature/feature-name` - New features
- `bugfix/issue-description` - Bug fixes
- `docs/documentation-update` - Documentation changes
- `refactor/component-name` - Code refactoring

## Code Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use meaningful variable and function names
- Keep functions focused and small (ideally < 50 lines)
- Add docstrings for all public functions and classes

### Code Formatting

```python
def example_function(parameter1, parameter2):
    """
    Brief description of what the function does.
    
    Args:
        parameter1 (str): Description of first parameter
        parameter2 (int): Description of second parameter
        
    Returns:
        bool: Description of return value
    """
    # Implementation here
    return True
```

### Error Handling

- Always handle exceptions appropriately
- Provide meaningful error messages to users
- Log errors for debugging purposes
- Use specific exception types when possible

```python
try:
    # Risky operation
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    return False
```

## Testing Guidelines

### Running Tests

Run the complete test suite:
```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python tests/test_connection.py
python tests/test_message_handling.py
```

### Test Coverage

- All new features must include tests
- Aim for comprehensive test coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

### Manual Testing

Before submitting changes:
1. Test basic connection to IRC server
2. Verify all commands work correctly
3. Test error handling scenarios
4. Ensure stability during extended use

## Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Ensure all tests pass**
3. **Update CHANGELOG.md** if applicable
4. **Create pull request** with descriptive title and details

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings or errors
```

### Commit Message Guidelines

Use clear, descriptive commit messages:

```
feat: add auto-reconnection feature
fix: handle connection timeout properly
docs: update installation instructions
refactor: improve message parsing logic
test: add unit tests for command validation
```

Format: `type: brief description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `style`: Code formatting

## Issue Reporting

### Before Submitting Issues

1. **Search existing issues** to avoid duplicates
2. **Test with latest version** to ensure issue still exists
3. **Gather relevant information** (Python version, OS, error messages)

### Issue Template

```markdown
## Bug Description
Clear description of the issue.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., macOS 12.0]
- Python Version: [e.g., 3.9.0]
- IRC Server: [e.g., irc.libera.chat]

## Additional Information
Any other relevant details, error messages, or screenshots.
```

## Feature Requests

We welcome feature requests! Please:

1. **Check existing requests** first
2. **Provide clear use case** and rationale
3. **Consider implementation complexity**
4. **Be open to discussion** about alternatives

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature.

## Use Case
Why this feature would be valuable.

## Proposed Implementation
Ideas for how this could be implemented.

## Alternatives Considered
Other approaches you've considered.
```

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

### Enforcement

Instances of unacceptable behavior may result in temporary or permanent ban from the project.

## Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For general questions and ideas
- **Pull Request Comments**: For code-specific discussions

### Documentation

- **User Manual**: `docs/USER_MANUAL.md`
- **Installation Guide**: `docs/INSTALLATION.md`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`
- **Build Plan**: `docs/build_plan.md`

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor acknowledgments

Thank you for contributing to Simple IRC Chat Client! 🚀

---

*This document is adapted from common open-source contribution guidelines and will evolve with the project.*
