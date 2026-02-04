<div align="center">

# 🎨 Croquis

**Your Intelligent Figure Drawing Practice Companion**

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/jiwonjae-svg/Croquis)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*Systematic figure drawing practice with timer functionality, deck management, and progress tracking.*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Building](#-building) • [Contributing](#-contributing)

---

</div>

## 🎯 What is Croquis?

Croquis is a **desktop application designed for artists** who want to improve their figure drawing skills through **systematic timed practice**. With deck management, automatic timers, and GitHub-style progress visualization, Croquis helps you build a consistent drawing habit.

Perfect for:
- 🎨 **Artists** practicing figure drawing and gesture studies
- 📚 **Art Students** following structured practice routines
- 🖌️ **Illustrators** warming up before projects
- 🎓 **Teachers** conducting timed drawing sessions

## ✨ Features

### 🎯 Core Functionality
- **Deck Management**: Organize image folders into practice decks with custom settings
- **Smart Timer System**: Automatic image transitions with configurable durations
- **Study Mode**: Unlimited viewing time for detailed studies
- **Weighted Shuffle**: Prioritize less-viewed images automatically
- **Tag Filtering**: Filter deck images by custom tags

### 📊 Practice Tracking
- **Heatmap Visualization**: GitHub-style contribution graph tracking daily practice
- **Practice History**: Detailed statistics of all practice sessions
- **Screenshot Capture**: Save your drawings alongside reference images
- **Progress Analytics**: View practice counts and streaks

### 🌍 User Experience
- **Multi-language Support**: Korean, English, and Japanese interfaces
- **Dark Mode**: Easy on the eyes during long practice sessions
- **Customizable Timer**: Position, font size, and display options
- **Alarm System**: Schedule practice reminders with Windows integration
- **System Tray**: Minimal footprint with quick access

### 🔒 Security & Privacy
- **Machine ID Encryption**: User-specific encrypted data storage
- **SHA-256 Key Derivation**: Secure key generation from hardware UUID
- **Local-Only Storage**: All data stays on your machine
- **No Telemetry**: Zero tracking or analytics

## 📦 Installation

### Option 1: Download Executable (Recommended)
1. Download `Croquis.exe` from [Releases](https://github.com/jiwonjae-svg/Croquis/releases)
2. Run the executable - no installation needed!
3. Configure your first deck and start practicing

### Option 2: Run from Source

**Requirements:**
- Python 3.10 or higher
- Windows 10/11

**Quick Start:**
```powershell
# Clone the repository
git clone https://github.com/jiwonjae-svg/Croquis.git
cd Croquis

# Install dependencies
pip install -r requirements.txt

# Launch application
python main.py
```

## 🚀 Usage

### Creating Your First Deck

1. **Open Deck Editor**: Click **Edit Deck** button on main window
2. **Add Images**:
   - Click **Select Folder** to import entire directories
   - Or use **+** button to add individual images
3. **Configure Deck**:
   - Set **shuffle mode** (normal, weighted, or sequential)
   - Add **tags** for filtering
   - Set per-deck **timer duration**
4. **Save**: Click **Save** button

### Starting a Practice Session

1. **Select Deck**: Choose from dropdown menu
2. **Set Timer**: Enter duration in seconds (or enable Study Mode)
3. **Configure Display**:
   - **Timer Position**: Top/Bottom, Left/Center/Right
   - **Image Size**: Width and height
   - **Effects**: Grayscale and horizontal flip options
4. **Click Start**: Full-screen viewer launches automatically

### Keyboard Shortcuts (Viewer)

| Key | Action |
|-----|--------|
| `Space` | Next image |
| `S` or `Enter` | Take screenshot |
| `Esc` | Close viewer |

### Viewing Your Progress

1. **Heatmap**: Main window shows GitHub-style practice tracking
2. **History**: Click **History** button to view all sessions
3. **Statistics**: See total practice count and streak information

### Setting Practice Reminders

1. Click **Alarm** button on main window
2. Set time and select days of the week
3. Enable alarm toggle
4. Receive Windows notifications at scheduled times

## 📁 Project Structure

```
Croquis/
│
├── 📄 main.py                           # Application entry point
├── 🔧 Croquis.spec                      # PyInstaller build configuration
├── 📋 requirements.txt                  # Python dependencies
├── 📝 translations.csv                  # Multi-language translations
│
├── 📁 src/
│   ├── 📁 core/                         # Core Business Logic
│   │   ├── key_manager.py               # Encryption key management
│   │   ├── alarm_service.py             # Alarm notification system
│   │   └── models.py                    # Data models (Settings, Constants)
│   │
│   ├── 📁 gui/                          # User Interface Components
│   │   ├── image_viewer_window.py       # Full-screen image viewer
│   │   └── widgets.py                   # Reusable widgets (Heatmap, Screenshot)
│   │
│   ├── 📁 utils/                        # Utilities & Helpers
│   │   ├── language_manager.py          # Multi-language support
│   │   ├── log_manager.py               # Logging system
│   │   ├── qt_resource_loader.py        # Qt resource handling
│   │   └── helpers.py                   # Common helper functions
│   │
│   └── 📁 assets/                       # Resources
│       ├── icon.ico                     # Application icon
│       ├── resources_rc.py              # Compiled Qt resources
│       └── btn/                         # Button images
│
├── 📁 scripts/                          # Build & Utility Scripts
│   ├── build.py                         # Automated build script
│   └── compile_resources.py             # Qt resource compiler
│
├── 📁 deck/                             # User Decks (Generated)
├── 📁 dat/                              # Encrypted User Data (Generated)
├── 📁 logs/                             # Application Logs (Generated)
└── 📁 croquis_pairs/                    # Screenshots (Generated)
```

## 🏗️ Architecture

Croquis follows a **clean modular architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         UI Layer (PyQt6)                │  ← User interaction
├─────────────────────────────────────────┤
│     Business Logic (Core Services)      │  ← Deck management, timers
├─────────────────────────────────────────┤
│     Data Layer (Encrypted Storage)      │  ← Settings, history, decks
├─────────────────────────────────────────┤
│       Utils Layer (Helpers)             │  ← Logging, i18n, paths
└─────────────────────────────────────────┘
```

### Key Components

#### 🎨 ImageViewerWindow
- **Full-screen Display**: Borderless window with customizable positioning
- **Timer Management**: Countdown with automatic transitions
- **Screenshot Capture**: Saves reference + drawing pairs
- **Keyboard Control**: Space, S/Enter, Esc shortcuts

#### 📊 HeatmapWidget
- **GitHub-style Visualization**: 365-day contribution graph
- **Color Coding**: Practice intensity from 0 to 10+ sessions
- **Hover Tooltips**: Date and count on mouse-over
- **Persistent Storage**: Encrypted history in `dat/croquis_history.dat`

#### 🔒 SecurityService (key_manager.py)
- **Hybrid Encryption**: Fernet (AES-128) with SHA-256 key derivation
- **Machine-Specific Keys**: Generated from hardware UUID + OS username
- **Cross-Platform**: Windows (Registry), macOS (IOPlatformUUID), Linux (/etc/machine-id)
- **Transparent Operation**: Automatic encrypt/decrypt

#### 🌐 LanguageManager
- **CSV-Based Translations**: 176+ translation keys
- **Runtime Switching**: Change language without restart
- **Fallback Handling**: Defaults to key name if translation missing

## 🛡️ Security Features

### Encryption Architecture
- **Algorithm**: Fernet (AES-128 in CBC mode with HMAC)
- **Key Derivation**: SHA-256 hash of (Machine UUID + Username + App Salt)
- **Scope**: Deck files, settings, practice history
- **Storage**: All sensitive data encrypted at rest

### Security Benefits
1. **User Isolation**: Each user's data is encrypted with unique key
2. **Machine Binding**: Data cannot be decrypted on different hardware
3. **Tamper Protection**: HMAC ensures data integrity
4. **No Password Required**: Key automatically derived from system

### Privacy Guarantees
- ✅ **All data stays local** - no cloud sync, no network requests
- ✅ **Encrypted storage** - deck paths and history are protected
- ✅ **No telemetry** - zero analytics or tracking
- ✅ **Open source** - audit the code yourself

## 🔧 Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **UI Framework** | PyQt6 | Modern cross-platform GUI |
| **Image Processing** | Pillow (PIL) | Image loading and manipulation |
| **Encryption** | cryptography (Fernet) | Data encryption at rest |
| **Notifications** | win11toast, plyer | Windows native notifications |
| **Process Management** | psutil | System information |
| **Logging** | Python logging | Structured application logs |
| **Build** | PyInstaller | Standalone executable creation |

## ⚡ Performance

- **Startup Time**: <3 seconds to main window
- **Image Loading**: <500ms for 4K images
- **Memory Footprint**: ~80MB RAM (varies with image count)
- **CPU Usage**: <2% idle, <10% during image transitions

Optimizations:
- Lazy-loaded UI components
- Image caching for frequently accessed decks
- Efficient PyQt6 event loop
- Background threads for I/O operations

## 🚀 Building from Source

### Quick Build (Recommended)
```powershell
# One-command build
python scripts/build.py
```

Output: `dist/Croquis.exe` (single-file executable)

### Manual PyInstaller Build
```powershell
pyinstaller Croquis.spec
```

### Build Configuration
- **Spec File**: `Croquis.spec` with optimized settings
- **Icon**: `src/assets/icon.ico` embedded in executable
- **Hidden Imports**: PyQt6, cryptography, Pillow, win11toast
- **Exclusions**: matplotlib, numpy, pandas, tkinter (reduces size)
- **Console**: Disabled for clean GUI-only experience

### Build Requirements
```powershell
pip install pyinstaller
```

## ⚙️ Configuration

### Auto-Generated Files

#### settings.dat (Encrypted)
```
Stores user preferences:
- Language, dark mode, timer settings
- Image size, grayscale, flip options
- Alarm configuration
```

#### croquis_history.dat (Encrypted)
```
Practice tracking:
- Date → Practice count mapping
- Used for heatmap visualization
```

#### *.deck Files (Encrypted)
```
Deck configuration:
- Image paths and metadata
- Shuffle mode, tags, timer
- Last viewed index
```

### Manual Configuration

Edit `translations.csv` to customize UI text:
```csv
key,ko,en,ja
app_title,크로키,Croquis,クロッキー
start_button,시작,Start,開始
```

## 🐛 Troubleshooting

### Application Won't Start
1. **Missing Python**: Install Python 3.10+
2. **Dependencies**: Run `pip install -r requirements.txt`
3. **Corrupted Config**: Delete `dat/settings.dat` and restart
4. **Permission Issues**: Run as Administrator (Windows)

### Images Not Displaying
1. **Deck Path Invalid**: Re-add deck with valid image folder
2. **Supported Formats**: JPG, PNG, BMP, GIF, WebP
3. **File Permissions**: Ensure read access to image directory

### Timer Not Working
1. **Study Mode Enabled**: Disable study mode for automatic timer
2. **Zero Duration**: Set timer value > 0 seconds
3. **Process Priority**: Close CPU-intensive apps

### Heatmap Not Showing
1. **No Practice Data**: Complete at least one session
2. **Corrupted History**: Delete `dat/croquis_history.dat`
3. **Display Issues**: Restart application

### Alarms Not Triggering
1. **Windows Notifications**: Enable in Windows Settings
2. **Administrator Rights**: Required for startup service
3. **Time Zone**: Ensure system time is correct

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

Free for personal, educational, and commercial use with attribution.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
4. **Push** to your branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```powershell
# Clone your fork
git clone https://github.com/yourusername/Croquis.git
cd Croquis

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to public functions
- Keep functions focused and modular

## 🙋 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/jiwonjae-svg/Croquis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jiwonjae-svg/Croquis/discussions)
- **Security**: Report vulnerabilities via GitHub Security

## 🎯 Roadmap

### Upcoming Features
- [ ] Custom deck templates
- [ ] Export practice statistics as CSV
- [ ] Integration with online image galleries
- [ ] Mobile companion app (view only)
- [ ] Pose library with anatomical references
- [ ] Video file support for animation practice

### Under Consideration
- [ ] Cloud backup for decks
- [ ] Social features (share decks, compare progress)
- [ ] AI-powered pose suggestions
- [ ] macOS and Linux support

## 🙏 Acknowledgments

Built with these amazing open-source projects:
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Modern Python GUI framework
- [Pillow](https://python-pillow.org/) - Image processing library
- [cryptography](https://cryptography.io/) - Cryptographic recipes and primitives
- [win11toast](https://github.com/GitHub30/win11toast) - Windows 11 notifications

Special thanks to the art community for inspiration and feedback.

---

<div align="center">

**Croquis** - Practice Makes Perfect 🎨

Made with ❤️ by artists, for artists

[⬆ Back to Top](#-croquis)

</div>


