#!/usr/bin/env python
"""
Croquis Application Entry Point
Professional croquis practice tool with encryption and learning features
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import and run main
if __name__ == "__main__":
    from src.main import main
    main()
