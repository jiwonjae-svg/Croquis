"""
Common utility functions for Croquis application
"""

import sys
import os
import logging
from pathlib import Path
from datetime import datetime
from PyQt6.QtGui import QIcon
from utils.log_manager import LOG_MESSAGES

logger = logging.getLogger('Croquis')


def get_data_path():
    """Get base path for data files (dat, logs, croquis_pairs etc.).
    Returns the project root directory."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - use executable's directory
        return Path(sys.executable).parent
    else:
        # Running as script - use project root (parent of src directory)
        return Path(__file__).parent.parent.parent


def get_icon_path():
    """Get the icon file path for toast notifications.
    For compiled executables, icon.ico is bundled into _MEIPASS."""
    if getattr(sys, 'frozen', False):
        # Compiled executable: icon is in _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            icon_path = Path(sys._MEIPASS) / "icon.ico"
        else:
            icon_path = Path(sys.executable).parent / "icon.ico"
    else:
        # Script mode: icon is in src/assets directory
        icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
    
    return str(icon_path) if icon_path.exists() else None


def get_app_icon() -> QIcon:
    """Load application icon from file (optimized for PyInstaller)"""
    icon_path = None
    
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        # PyInstaller extracts files to sys._MEIPASS (temp directory)
        bundled_icon = Path(sys._MEIPASS) / "icon.ico"
        if bundled_icon.exists():
            icon_path = bundled_icon
        else:
            # Fallback: check executable directory
            icon_path = get_data_path() / "icon.ico"
    else:
        # Running as script - icon is in src/assets
        icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
    
    if icon_path and icon_path.exists():
        return QIcon(str(icon_path))
    
    return QIcon()


def setup_logging():
    """Initialize logging system"""
    # Use execution path for logs directory (not script path)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - use executable's directory
        base_dir = Path(sys.executable).parent
    else:
        # Running as script - use project root
        base_dir = Path(__file__).parent.parent.parent
    
    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"croquis_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('Croquis')


def tr(key: str, lang: str = "ko") -> str:
    """Translation helper"""
    from utils.language_manager import TRANSLATIONS
    return TRANSLATIONS.get(lang, TRANSLATIONS["ko"]).get(key, key)


def show_toast_notification(title: str, message: str, icon_path: str = None):
    """Display Windows toast notification"""
    # Set icon path
    if icon_path is None:
        icon_path = get_icon_path()
    
    icon_exists = icon_path and os.path.exists(icon_path)
    logger.info(LOG_MESSAGES["toast_notification_requested"].format(title, message, icon_path))
    logger.info(f"Icon exists: {icon_exists}")
    
    # Priority 1: win11toast (Windows 10/11 native notifications)
    try:
        from win11toast import toast_async
        import asyncio
        
        async def show_toast():
            # 5 second timeout
            try:
                await asyncio.wait_for(
                    toast_async(
                        title,
                        message,
                        icon=icon_path if icon_exists else None,
                        app_id="Croquis"
                    ),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                logger.warning(LOG_MESSAGES["toast_notification_timeout"])
        
        asyncio.run(show_toast())
        logger.info(LOG_MESSAGES["toast_notification_success"].format("win11toast"))
        return
    except Exception as e:
        logger.error(LOG_MESSAGES["toast_notification_failed"].format("win11toast", e))
    
    # Priority 2: plyer (cross-platform)
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="Croquis",
            app_icon=icon_path if icon_exists else None,
            timeout=10
        )
        logger.info(LOG_MESSAGES["toast_notification_success"].format("plyer"))
        return
    except Exception as e:
        logger.error(LOG_MESSAGES["toast_notification_failed"].format("plyer", e))
    
    # Last resort: console output
    fallback_msg = f"[ALARM] {title}: {message}"
    print(fallback_msg)
    logger.info(LOG_MESSAGES["toast_notification_fallback"].format(fallback_msg))


# Size constants
# Deck editor list item sizes
DECK_ICON_WIDTH = 100
DECK_ICON_HEIGHT = 120
DECK_GRID_WIDTH = 120
DECK_GRID_HEIGHT = 160
DECK_SPACING = 3

# History window list item sizes
HISTORY_ICON_WIDTH = 300
HISTORY_ICON_HEIGHT = 150
HISTORY_GRID_WIDTH = 320
HISTORY_GRID_HEIGHT = 185
HISTORY_SPACING = 5
