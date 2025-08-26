# Contributing to PlaylistCat 🐱

Thank you for your interest in contributing to PlaylistCat! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Include detailed information about your environment (OS, Python version, etc.)
- Provide steps to reproduce the issue
- Include error messages if applicable

### Suggesting Features
- Open an issue with the "enhancement" label
- Clearly describe the feature and its benefits
- Provide examples of how it would be used

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes**: Run `python test.py` to ensure everything works
5. **Commit your changes**: Use clear, descriptive commit messages
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

### Code Style
- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings to new functions and classes
- Keep functions focused and small when possible

### Testing
- Test both GUI and CLI versions before submitting
- Ensure the application works with various playlist types
- Test error handling with invalid inputs

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/playlistcat.git
   cd playlistcat
   ```

2. Set up virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Test the setup:
   ```bash
   python test.py
   ```

## Questions?

Feel free to open an issue with the "question" label if you need help or clarification.

Thanks for contributing! 🎵
