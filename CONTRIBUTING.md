# 🤝 Contributing to File Organizer

Thank you for your interest in contributing to File Organizer! This project is designed to be beginner-friendly and welcomes contributions from developers of all skill levels.

## 🌟 Why Contribute?

- **Perfect for beginners**: Simple codebase with clear structure
- **Immediate impact**: Your changes help people organize their files
- **Learning opportunity**: Practice Python, testing, and open source workflows
- **Community**: Join a friendly, supportive development community

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- Git
- A GitHub account

### Setting Up Your Development Environment

1. **Fork the repository**
   - Click the "Fork" button on the GitHub page
   - Clone your fork: `git clone https://github.com/YOUR_USERNAME/file-organizer.git`

2. **Create a development environment**
   ```bash
   cd file-organizer
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests to make sure everything works**
   ```bash
   python -m pytest tests/
   ```

## 🎯 How to Contribute

### 1. Choose an Issue

Look for issues labeled with:
- `good first issue` - Perfect for beginners
- `help wanted` - Community contributions welcome
- `bug` - Fix a problem
- `enhancement` - Add a new feature

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 3. Make Your Changes

- Write clean, readable code
- Add comments for complex logic
- Follow the existing code style
- Test your changes

### 4. Test Your Changes

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_file_organizer.py

# Run with verbose output
python -m pytest tests/ -v
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Add: brief description of your changes"
```

**Commit Message Guidelines:**
- Use present tense: "Add feature" not "Added feature"
- Be descriptive but concise
- Reference issues: "Fix #123" or "Closes #456"

### 6. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference to related issues
- Screenshots if applicable

## 📝 Code Style Guidelines

### Python Style

- Follow PEP 8 (Python style guide)
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Example Good Code:

```python
def organize_files(directory_path: str, dry_run: bool = False) -> None:
    """
    Organize files in the specified directory.
    
    Args:
        directory_path: Path to the directory to organize
        dry_run: If True, only show what would be moved
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    # Rest of the function...
```

### Example Bad Code:

```python
def org(d, dr=False):  # Unclear names
    # No docstring
    p = Path(d)  # Unclear variable name
    if not p.exists():  # No error handling
        return
    # etc...
```

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for new functionality
- Test edge cases and error conditions
- Use descriptive test names
- Follow the existing test structure

### Test Structure

```python
def test_function_name_what_it_tests(self):
    """Test that function_name does what it should do."""
    # Arrange - set up test data
    test_data = "example"
    
    # Act - call the function
    result = function_name(test_data)
    
    # Assert - check the result
    self.assertEqual(result, expected_value)
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=py_sort

# Run specific test
python -m pytest tests/test_file_organizer.py::TestFileOrganizer::test_get_file_extension
```

## 🎨 Good First Issues

Here are some great issues for beginners:

### 1. Add More File Types
**Difficulty**: ⭐ (Easy)
**Description**: Add more file extensions to the sorting rules
**Files to modify**: `config.json`, `py_sort.py`

### 2. Improve Error Messages
**Difficulty**: ⭐ (Easy)
**Description**: Make error messages more helpful and user-friendly
**Files to modify**: `py_sort.py`

### 3. Add Colored Output
**Difficulty**: ⭐⭐ (Easy-Medium)
**Description**: Use a library like `rich` or `colorama` to add colors
**Files to modify**: `py_sort.py`, `requirements.txt`

### 4. Create Example Configurations
**Difficulty**: ⭐ (Easy)
**Description**: Create example config files for different use cases
**Files to create**: `examples/minimal_config.json`, `examples/extended_config.json`

### 5. Add Progress Bar
**Difficulty**: ⭐⭐ (Easy-Medium)
**Description**: Show progress when organizing many files
**Files to modify**: `py_sort.py`

### 6. Improve Documentation
**Difficulty**: ⭐ (Easy)
**Description**: Add more examples and improve README
**Files to modify**: `README.md`

## 🐛 Reporting Bugs

### Before Reporting

1. Check if the issue already exists
2. Try the latest version
3. Test with a simple example

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**
1. Go to '...'
2. Run command '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- File Organizer version: [e.g., 1.0.0]

**Additional Context**
Any other context about the problem.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Why would this feature be useful? What problem does it solve?

**Proposed Solution**
How do you think this feature should work?

**Alternatives Considered**
Any alternative solutions you've thought about.

**Additional Context**
Any other context, mockups, or examples.
```

## 📚 Resources for Beginners

### Git and GitHub
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)

### Python
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Python Testing with pytest](https://docs.pytest.org/)

### Open Source
- [First Timers Only](https://www.firsttimersonly.com/)
- [Good First Issues](https://goodfirstissues.com/)
- [Open Source Guide](https://opensource.guide/)

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## 📞 Getting Help

- 💬 **GitHub Discussions**: Ask questions and get help
- 🐛 **GitHub Issues**: Report bugs and request features
- 📧 **Email**: Contact maintainers directly
- 💬 **Discord/Slack**: Join our community chat (if available)

## 📋 Checklist for Pull Requests

Before submitting your PR, make sure:

- [ ] Code follows the style guidelines
- [ ] Tests pass: `python -m pytest`
- [ ] New functionality has tests
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear
- [ ] PR description explains the changes
- [ ] Related issues are referenced

## 🎉 Thank You!

Your contributions make this project better for everyone. Whether you're fixing a typo, adding a feature, or improving documentation, every contribution matters!

---

**Happy Contributing! 🚀**

*Remember: Every expert was once a beginner. Don't be afraid to ask questions!*
