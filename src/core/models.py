"""
Data models for Croquis application
"""

from dataclasses import dataclass


@dataclass
class CroquisSettings:
    """Croquis settings data class"""
    image_folder: str = ""
    image_width: int = 400
    image_height: int = 700
    grayscale: bool = False
    flip_horizontal: bool = False
    timer_position: str = "bottom_right"
    timer_font_size: str = "large"
    time_seconds: int = 5
    language: str = "ko"
    dark_mode: bool = False
    study_mode: bool = False
    today_croquis_count_position: str = "top_right"
    today_croquis_count_font_size: str = "medium"


@dataclass
class CroquisRecord:
    """Croquis record data class"""
    date: str
    count: int
