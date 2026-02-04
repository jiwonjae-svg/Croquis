"""
Language Manager Module
Loads translations from CSV file and provides them as a dictionary.
Priority (frozen): Qt resources -> file fallback
Priority (dev): file -> Qt resources fallback
"""

import sys
import csv
import logging
from pathlib import Path
from io import StringIO

logger = logging.getLogger('Croquis')

def get_base_path():
    """Get base path for resources. Handles PyInstaller bundled executables."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - use executable directory
        return Path(sys.executable).parent
    else:
        # Running as script - go up to project root (2 levels up from src/utils/)
        return Path(__file__).parent.parent.parent

def load_translations_from_csv(csv_path: str = None) -> dict:
    """Load translations from CSV file into a nested dictionary."""
    translations = {}
    loaded_from = None
    
    # For frozen executable, prioritize Qt resources
    if getattr(sys, 'frozen', False):
        # 1. Try loading from Qt resources FIRST (for compiled executable)
        try:
            # Import resources_rc first to register Qt resources
            try:
                from assets import resources_rc  # type: ignore[import-not-found]
                if hasattr(sys, 'stderr'):
                    print("[DEBUG] resources_rc imported successfully", file=sys.stderr)
            except ImportError as e:
                if hasattr(sys, 'stderr'):
                    print(f"[DEBUG] Failed to import resources_rc: {e}", file=sys.stderr)
                import resources_rc  # type: ignore[import-not-found]
            
            # Import with absolute path
            from utils.qt_resource_loader import load_text
            csv_content = load_text(":/data/translations.csv")
            
            if hasattr(sys, 'stderr'):
                print(f"[DEBUG] Qt resource load result: {len(csv_content) if csv_content else 0} bytes", file=sys.stderr)
            
            if csv_content:
                reader = csv.DictReader(StringIO(csv_content))
                languages = [col for col in reader.fieldnames if col != 'key']
                
                # Initialize language dictionaries
                for lang in languages:
                    translations[lang] = {}
                
                # Read each row and populate translations
                for row in reader:
                    key = row['key']
                    for lang in languages:
                        translations[lang][key] = row[lang]
                
                loaded_from = "Qt resources"
                logger.info(f"Loaded {len(translations)} languages from Qt resources")
                return translations
        
        except Exception as e:
            logger.warning(f"Failed to load from Qt resources: {e}")
    
    # 2. Try loading from file (for development or fallback)
    if csv_path is None:
        csv_path = get_base_path() / "translations.csv"
        # Also try src/assets/translations.csv for development
        if not csv_path.exists():
            csv_path = get_base_path() / "src" / "assets" / "translations.csv"
    else:
        csv_path = Path(csv_path)
    
    if csv_path.exists():
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Get language columns (all columns except 'key')
                languages = [col for col in reader.fieldnames if col != 'key']
                
                # Initialize language dictionaries
                for lang in languages:
                    translations[lang] = {}
                
                # Read each row and populate translations
                for row in reader:
                    key = row['key']
                    for lang in languages:
                        translations[lang][key] = row[lang]
            
            loaded_from = f"file: {csv_path}"
            logger.info(f"Loaded {len(translations)} languages from {csv_path}")
            return translations
            
        except Exception as e:
            logger.error(f"Error loading from file {csv_path}: {e}")
    
    # 3. Try loading from Qt resources as last fallback (if not frozen)
    if not getattr(sys, 'frozen', False):
        try:
            from utils.qt_resource_loader import load_text
            csv_content = load_text(":/data/translations.csv")
            
            if csv_content:
                reader = csv.DictReader(StringIO(csv_content))
                languages = [col for col in reader.fieldnames if col != 'key']
                
                # Initialize language dictionaries
                for lang in languages:
                    translations[lang] = {}
                
                # Read each row and populate translations
                for row in reader:
                    key = row['key']
                    for lang in languages:
                        translations[lang][key] = row[lang]
                
                loaded_from = "Qt resources (fallback)"
                logger.info(f"Loaded {len(translations)} languages from Qt resources")
                return translations
        
        except Exception as e:
            logger.warning(f"Failed to load from Qt resources: {e}")
    
    # 4. Return minimal translations as absolute last resort
    logger.error("Could not load translations from any source!")
    return {
        "ko": {"error": "번역 파일을 찾을 수 없습니다.", "app_title": "크로키"},
        "en": {"error": "Translation file not found.", "app_title": "Croquis"},
        "ja": {"error": "翻訳ファイルが見つかりません。", "app_title": "クロッキー"}
    }

# Load translations on module import
TRANSLATIONS = load_translations_from_csv()

# Log what was loaded
if TRANSLATIONS:
    lang_count = len(TRANSLATIONS)
    key_count = len(TRANSLATIONS.get('ko', {})) if 'ko' in TRANSLATIONS else 0
    logger.info(f"Translation system initialized: {lang_count} languages, {key_count} keys")
else:
    logger.error("Translation system failed to initialize!")
