# 📁 File Organizer

A simple, beginner-friendly Python tool that automatically organizes files in your directories by moving them into subdirectories based on their file type.

Perfect for cleaning up messy folders like Downloads, Desktop, or any directory that needs organizing!

## ✨ Features

- **Automatic File Sorting**: Moves files into organized folders based on file extensions
- **Configurable Rules**: Customize sorting rules via JSON configuration
- **Dry Run Mode**: Preview changes before actually moving files
- **Beginner Friendly**: Uses only Python standard library - no external dependencies
- **Safe Operation**: Won't overwrite existing files
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- No additional packages required!

### Installation

1. Clone or download this repository
2. Navigate to the project directory
3. You're ready to go!

### Basic Usage

```bash
# Organize files in your Downloads folder
python py_sort.py ~/Downloads

# Preview what would be organized (dry run)
python py_sort.py ~/Downloads --dry-run

# Use a custom configuration file
python py_sort.py ~/Downloads --config my_rules.json
```

## 📖 Detailed Usage

### Command Line Options

```bash
python py_sort.py [directory] [options]

Arguments:
  directory              Path to the directory to organize

Options:
  --dry-run             Show what would be moved without actually moving files
  --config CONFIG       Path to JSON configuration file (default: config.json)
  -h, --help           Show help message
```

### Examples

```bash
# Organize your Downloads folder
python py_sort.py ~/Downloads

# Organize Desktop with dry run first
python py_sort.py ~/Desktop --dry-run
python py_sort.py ~/Desktop

# Organize a specific folder with custom rules
python py_sort.py /path/to/messy/folder --config custom_rules.json
```

## ⚙️ Configuration

The tool uses a JSON configuration file (`config.json`) to define how files should be sorted. Here's the default structure:

```json
{
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
  "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
  "Videos": [".mp4", ".avi", ".mov", ".wmv", ".flv"],
  "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
  "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
  "Code": [".py", ".js", ".html", ".css", ".java"],
  "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
  "Presentations": [".ppt", ".pptx", ".odp", ".key"],
  "Executables": [".exe", ".msi", ".deb", ".rpm", ".dmg"],
  "Other": []
}
```

### Customizing Rules

1. Copy `config.json` to create your own rules
2. Modify the file extensions for each category
3. Add new categories as needed
4. Use your custom config: `python py_sort.py ~/Downloads --config my_rules.json`

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
python -m pytest tests/
```

Or run individual tests:

```bash
python tests/test_file_organizer.py
```

## 🤝 Contributing

We welcome contributions from beginners and experienced developers alike! This project is perfect for:

- **First-time contributors** to open source
- **Python beginners** looking to practice
- **Anyone** who wants to help improve file organization

### Good First Issues

Check out our [Issues](https://github.com/yourusername/file-organizer/issues) page for beginner-friendly tasks:

- 🎨 Add more file types to sorting rules
- 🎨 Add colored output to the terminal
- 🎨 Improve error handling and user feedback
- 📚 Write documentation and examples
- 🧪 Add more test cases
- 🎨 Create a GUI version

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Test** your changes: `python -m pytest`
5. **Commit** your changes: `git commit -m 'Add amazing feature'`
6. **Push** to your branch: `git push origin feature/amazing-feature`
7. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📋 Project Structure

```
file-organizer/
├── py_sort.py              # Main script
├── config.json             # Default sorting rules
├── requirements.txt        # Dependencies
├── README.md              # This file
├── CONTRIBUTING.md        # Contribution guidelines
├── LICENSE                # MIT License
├── tests/                 # Test files
│   ├── test_file_organizer.py
│   └── test_data/         # Sample files for testing
└── examples/              # Example configurations
    ├── minimal_config.json
    └── extended_config.json
```

## 🐛 Troubleshooting

### Common Issues

**"Permission denied" errors:**
- Make sure you have write permissions to the target directory
- On Windows, try running as administrator if needed

**"No files found to organize":**
- Check that the directory path is correct
- Make sure there are files (not just folders) in the directory

**"Config file not found":**
- The script will use default rules if `config.json` is missing
- Create a `config.json` file or specify a custom path with `--config`

### Getting Help

- 📖 Check the [Issues](https://github.com/yourusername/file-organizer/issues) page
- 💬 Start a [Discussion](https://github.com/yourusername/file-organizer/discussions)
- 📧 Contact the maintainers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need to organize messy download folders
- Built with ❤️ for the open source community
- Perfect for hackathons and beginner contributions

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/file-organizer)
![GitHub forks](https://img.shields.io/github/forks/yourusername/file-organizer)
![GitHub issues](https://img.shields.io/github/issues/yourusername/file-organizer)
![Python version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

**Updates**
-managed to add color as assets and initialized python virtual env using uv

**Happy Organizing! 🎉**

*Made with ❤️ for beginners and the open source community*
