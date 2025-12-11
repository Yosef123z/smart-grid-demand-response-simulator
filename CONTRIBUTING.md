# Contributing to Smart Grid Demand-Response Simulator

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

1. **Check existing issues** to avoid duplicates
2. **Use a clear title** describing the problem
3. **Provide details**:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Python version and OS

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the code style guidelines
4. **Write/update tests** for your changes
5. **Run tests**: `python -m pytest tests/ -v`
6. **Run linting**: `python -m flake8 src/ main.py dashboard.py`
7. **Commit with clear messages**: `git commit -m "Add: Description of change"`
8. **Push to your fork**: `git push origin feature/your-feature-name`
9. **Open a Pull Request**

## Code Style Guidelines

- Follow **PEP 8** Python style guide
- Use **docstrings** for all functions and classes
- Keep functions focused and modular
- Write **unit tests** for new functionality
- Aim for **>80% test coverage**

## Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/smart-grid-simulator.git
cd smart-grid-simulator

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v --cov=src
```

## Commit Message Format

Use clear, descriptive commit messages:
- `Add: New feature description`
- `Fix: Bug fix description`
- `Update: Changed functionality description`
- `Docs: Documentation update`
- `Test: Test additions or fixes`

## Questions?

Feel free to open an issue for questions or discussions about potential contributions.
