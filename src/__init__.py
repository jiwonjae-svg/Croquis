"""
Croquis Application Package
Professional croquis practice tool with encryption and learning features
"""

__version__ = "2.0.0"
__author__ = "Croquis Team"

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
