# Contributing to Data Analyst Agent

Thank you for your interest in contributing to the Data Analyst Agent! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue templates** when available
3. **Provide clear, detailed descriptions** including:
   - Steps to reproduce the issue
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots or error messages if applicable

### Submitting Pull Requests

1. **Fork the repository** and create a new branch
2. **Make your changes** following the coding standards
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Commit your changes** with clear, descriptive messages
6. **Submit a pull request** with a detailed description

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Instructions

1. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Data-Analyst-Agent.git
   cd Data-Analyst-Agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run tests**:
   ```bash
   pytest tests/
   ```

## 📝 Coding Standards

### Python Code Style

- **Follow PEP 8** style guidelines
- **Use type hints** where appropriate
- **Write docstrings** for all public functions and classes
- **Keep functions focused** and reasonably sized
- **Use meaningful variable and function names**

### Example Function Format:

```python
def process_data(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Process the input data by selecting and cleaning specified columns.
    
    Args:
        data: Input DataFrame to process
        columns: List of column names to select
        
    Returns:
        Processed DataFrame with selected columns
        
    Raises:
        ValueError: If specified columns don't exist in data
    """
    # Implementation here
    pass
```

### Code Organization

- **Separate concerns** into different modules
- **Use meaningful file and directory names**
- **Keep imports organized** (standard library, third-party, local)
- **Add comments** for complex logic

## 🧪 Testing

### Writing Tests

- **Write unit tests** for all new functionality
- **Use pytest** as the testing framework
- **Mock external dependencies** (API calls, file I/O)
- **Test edge cases** and error conditions

### Test Structure:

```python
import pytest
from src.data_processor import DataProcessor

class TestDataProcessor:
    def setup_method(self):
        self.processor = DataProcessor()
    
    def test_process_csv_file(self):
        # Test implementation
        pass
    
    def test_invalid_file_format(self):
        with pytest.raises(ValueError):
            # Test error handling
            pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_data_processor.py
```

## 📚 Documentation

### Updating Documentation

- **Update README.md** for major changes
- **Add docstrings** to new functions and classes
- **Update configuration** examples when needed
- **Add usage examples** for new features

### Documentation Format

- Use **Markdown** for documentation files
- Include **code examples** where helpful
- Keep documentation **up-to-date** with code changes
- Use **clear, concise language**

## 🔄 Git Workflow

### Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow the conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(ai): add support for GPT-4 model`
- `fix(data): handle missing values in CSV processing`
- `docs(readme): update installation instructions`
- `test(processor): add tests for image processing`

## 🚀 Release Process

1. **Version bumping** follows semantic versioning (SemVer)
2. **Changelog** is updated for each release
3. **Tests must pass** before release
4. **Documentation** is updated as needed

## 💡 Feature Requests

When proposing new features:

1. **Check existing issues** and discussions
2. **Describe the use case** clearly
3. **Explain the expected benefit**
4. **Consider the implementation complexity**
5. **Discuss potential breaking changes**

## 🐛 Bug Reports

Good bug reports include:

- **Clear, descriptive title**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment information**
- **Error messages or logs**
- **Screenshots** if applicable

## 📞 Getting Help

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and general discussion
- **Email** - For security issues or private concerns

## 🎯 Areas for Contribution

We especially welcome contributions in:

- **New file format support** (JSON, XML, databases)
- **Additional AI model integrations**
- **Performance optimizations**
- **UI/UX improvements**
- **Documentation and examples**
- **Test coverage improvements**
- **Bug fixes and stability improvements**

## 📋 Code Review Process

1. **All changes** require review before merging
2. **Address feedback** promptly and professionally
3. **Keep discussions** focused on the code
4. **Be respectful** of different approaches and opinions

## 🏆 Recognition

Contributors are recognized in:

- **README.md** contributors section
- **CHANGELOG.md** for significant contributions
- **GitHub contributors** page

Thank you for contributing to Data Analyst Agent! Your help makes this project better for everyone. 🙌
