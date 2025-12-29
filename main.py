"""
크로키 연습 앱 (Croquis Practice App)
PyQt6 기반의 크로키 연습 애플리케이션
"""

import sys
import os
import json
import random
import hashlib
import tempfile
import time
import logging
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
import base64

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox,
    QSpinBox, QGroupBox, QFileDialog, QDialog, QDialogButtonBox,
    QScrollArea, QFrame, QSplitter, QMenuBar, QMenu, QToolBar,
    QListWidget, QListWidgetItem, QMessageBox, QSizePolicy, QStackedWidget,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QRubberBand,
    QTimeEdit, QDateEdit, QCalendarWidget, QSystemTrayIcon, QAbstractItemView
)
from PyQt6.QtCore import (
    Qt, QTimer, QSize, QRect, QPoint, pyqtSignal, QMimeData, QUrl,
    QPropertyAnimation, QEasingCurve, QSettings, QTime, QDate, QDateTime
)
from PyQt6.QtGui import (
    QPixmap, QImage, QPainter, QColor, QPen, QBrush, QFont, QIcon,
    QIntValidator, QScreen, QGuiApplication, QDragEnterEvent, QDropEvent,
    QMouseEvent, QPaintEvent, QKeyEvent, QAction, QDrag
)

# ============== 로깅 설정 ==============
def setup_logging():
    """로깅 시스템 초기화"""
    log_dir = Path(__file__).parent / "logs"
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

logger = setup_logging()
logger.info("프로그램 시작")


# ============== 다국어 지원 ==============
TRANSLATIONS = {
    "ko": {
        "app_title": "크로키 연습 앱",
        "heatmap_title": "크로키 히트맵",
        "croquis_count": "크로키 횟수",
        "less": "Less",
        "more": "More",
        "basic_settings": "기본 설정",
        "image_folder": "그림 폴더:",
        "select_folder": "폴더 선택",
        "image_settings": "이미지 설정",
        "image_width": "이미지 창 너비:",
        "image_height": "이미지 창 높이:",
        "random_order": "랜덤 순서",
        "grayscale": "흑백 표시",
        "flip_horizontal": "좌우 반전",
        "timer_settings": "타이머 설정",
        "timer_position": "타이머 위치:",
        "timer_font_size": "타이머 폰트 크기:",
        "time_setting": "시간 설정 (초):",
        "other_settings": "기타 설정",
        "language": "언어:",
        "dark_mode": "다크 모드",
        "start_croquis": "크로키 시작",
        "edit_deck": "크로키 덱 편집",
        "croquis_history": "크로키 히스토리",
        "croquis_alarm": "크로키 알람",
        "large": "크게",
        "medium": "보통",
        "small": "작게",
        "bottom_right": "bottom_right",
        "bottom_center": "bottom_center",
        "bottom_left": "bottom_left",
        "top_right": "top_right",
        "top_center": "top_center",
        "top_left": "top_left",
        "file": "파일",
        "new": "새로 만들기",
        "open": "불러오기",
        "save": "저장",
        "save_as": "다른 이름으로 저장",
        "import_images": "이미지 불러오기",
        "deck_images": "덱 이미지",
        "image_info": "이미지 정보",
        "save_croquis": "크로키 저장",
        "save_question": "이 크로키를 저장하시겠습니까?",
        "yes": "예",
        "no": "아니오",
        "previous": "이전",
        "next": "다음",
        "pause": "정지",
        "play": "재생",
        "stop": "종료",
        "korean": "한국어",
        "english": "English",
        "add_memo": "메모하기",
        "memo": "메모",
        "close": "닫기",
    },
    "en": {
        "app_title": "Croquis Practice App",
        "heatmap_title": "Croquis Heatmap",
        "croquis_count": "Croquis Count",
        "less": "Less",
        "more": "More",
        "basic_settings": "Basic Settings",
        "image_folder": "Image Folder:",
        "select_folder": "Select Folder",
        "image_settings": "Image Settings",
        "image_width": "Image Window Width:",
        "image_height": "Image Window Height:",
        "random_order": "Random Order",
        "grayscale": "Grayscale",
        "flip_horizontal": "Flip Horizontal",
        "timer_settings": "Timer Settings",
        "timer_position": "Timer Position:",
        "timer_font_size": "Timer Font Size:",
        "time_setting": "Time Setting (sec):",
        "other_settings": "Other Settings",
        "language": "Language:",
        "dark_mode": "Dark Mode",
        "start_croquis": "Start Croquis",
        "edit_deck": "Edit Croquis Deck",
        "croquis_history": "Croquis History",
        "croquis_alarm": "Croquis Alarm",
        "large": "Large",
        "medium": "Medium",
        "small": "Small",
        "bottom_right": "bottom_right",
        "bottom_center": "bottom_center",
        "bottom_left": "bottom_left",
        "top_right": "top_right",
        "top_center": "top_center",
        "top_left": "top_left",
        "file": "File",
        "new": "New",
        "open": "Open",
        "save": "Save",
        "save_as": "Save As",
        "import_images": "Import Images",
        "deck_images": "Deck Images",
        "image_info": "Image Info",
        "save_croquis": "Save Croquis",
        "save_question": "Do you want to save this croquis?",
        "yes": "Yes",
        "no": "No",
        "previous": "Previous",
        "next": "Next",
        "pause": "Pause",
        "play": "Play",
        "stop": "Stop",
        "korean": "한국어",
        "english": "English",
        "add_memo": "Add Memo",
        "memo": "Memo",
        "close": "Close",
    }
}


def tr(key: str, lang: str = "ko") -> str:
    """번역 함수"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["ko"]).get(key, key)


# ============== 암호화 유틸리티 ==============
def encrypt_data(data: dict) -> bytes:
    """데이터 압축 및 암호화"""
    import zlib
    key = base64.urlsafe_b64encode(hashlib.sha256(b"croquis_secret_key").digest())
    fernet = Fernet(key)
    json_str = json.dumps(data, ensure_ascii=False)
    # zlib로 압축 (레벨 9 = 최대 압축)
    compressed = zlib.compress(json_str.encode(), level=9)
    encrypted = fernet.encrypt(compressed)
    return encrypted

def decrypt_data(encrypted: bytes) -> dict:
    """데이터 복호화 및 압축 해제"""
    import zlib
    key = base64.urlsafe_b64encode(hashlib.sha256(b"croquis_secret_key").digest())
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    # 압축 해제
    decompressed = zlib.decompress(decrypted)
    data = json.loads(decompressed.decode())
    return data


# ============== 데이터 클래스 ==============
@dataclass
class CroquisSettings:
    """크로키 설정 데이터 클래스"""
    image_folder: str = ""
    image_width: int = 400
    image_height: int = 700
    random_order: bool = False
    grayscale: bool = False
    flip_horizontal: bool = False
    timer_position: str = "bottom_right"
    timer_font_size: str = "large"
    time_seconds: int = 5
    language: str = "ko"
    dark_mode: bool = False
    study_mode: bool = False


@dataclass
class CroquisRecord:
    """크로키 기록 데이터 클래스"""
    date: str
    count: int


# ============== 히트맵 위젯 ==============
class HeatmapWidget(QWidget):
    """GitHub 스타일의 크로키 히트맵 위젯"""
    
    def __init__(self, parent=None, lang: str = "ko"):
        super().__init__(parent)
        self.lang = lang
        self.data: Dict[str, int] = {}
        self.cell_size = 8
        self.cell_gap = 1
        self.weeks = 53
        self.days = 7
        self.total_count = 0
        self.load_data()
        self.setMinimumHeight(120)
        self.setMaximumHeight(120)
        self.setMouseTracking(True)
        self.hover_date = None
        self.hover_pos = None
        
    def load_data(self):
        """히스토리 데이터 로드"""
        dat_dir = Path(__file__).parent / "dat"
        dat_dir.mkdir(exist_ok=True)
        data_path = dat_dir / "croquis_history.dat"
        if data_path.exists():
            try:
                with open(data_path, "rb") as f:
                    encrypted = f.read()
                decrypted = decrypt_data(encrypted)
                self.data = decrypted
                self.total_count = sum(self.data.values())
            except Exception:
                self.data = {}
                self.total_count = 0
        else:
            self.data = {}
            self.total_count = 0
    
    def save_data(self):
        """히스토리 데이터 저장"""
        dat_dir = Path(__file__).parent / "dat"
        dat_dir.mkdir(exist_ok=True)
        data_path = dat_dir / "croquis_history.dat"
        encrypted = encrypt_data(self.data)
        with open(data_path, "wb") as f:
            f.write(encrypted)
    
    def add_croquis(self, count: int = 1):
        """크로키 횟수 추가"""
        today = date.today().isoformat()
        self.data[today] = self.data.get(today, 0) + count
        self.total_count += count
        self.save_data()
        self.update()
    
    def get_color(self, count: int) -> QColor:
        """횟수에 따른 색상 반환"""
        if count == 0:
            return QColor(235, 237, 240)
        elif count <= 2:
            return QColor(155, 233, 168)
        elif count <= 5:
            return QColor(64, 196, 99)
        elif count <= 10:
            return QColor(48, 161, 78)
        else:
            return QColor(33, 110, 57)
    
    def paintEvent(self, event: QPaintEvent):
        """히트맵 그리기"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 월 라벨
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        today = date.today()
        start_date = today - timedelta(days=365)
        
        # 월 라벨 그리기
        painter.setFont(QFont("Arial", 9))
        painter.setPen(QColor(100, 100, 100))
        
        x_offset = 60
        y_offset = 20
        
        # 월별 시작 위치 계산 및 라벨 그리기
        current_month = 0
        for week in range(self.weeks):
            check_date = start_date + timedelta(weeks=week)
            if check_date.month != current_month:
                current_month = check_date.month
                x = x_offset + week * (self.cell_size + self.cell_gap)
                painter.drawText(x, y_offset - 8, months[current_month - 1])
        
        # 히트맵 셀 그리기
        for week in range(self.weeks):
            for day in range(self.days):
                cell_date = start_date + timedelta(weeks=week, days=day)
                if cell_date > today:
                    continue
                
                date_str = cell_date.isoformat()
                count = self.data.get(date_str, 0)
                color = self.get_color(count)
                
                x = x_offset + week * (self.cell_size + self.cell_gap)
                y = y_offset + day * (self.cell_size + self.cell_gap)
                
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(x, y, self.cell_size, self.cell_size, 2, 2)
        
        # 범례 그리기
        legend_x = x_offset
        legend_y = y_offset + self.days * (self.cell_size + self.cell_gap) + 10
        
        painter.setPen(QColor(100, 100, 100))
        painter.drawText(legend_x, legend_y + 10, tr("less", self.lang))
        
        legend_colors = [0, 1, 3, 6, 11]
        for i, c in enumerate(legend_colors):
            color = self.get_color(c)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            lx = legend_x + 35 + i * (self.cell_size + 2)
            painter.drawRoundedRect(lx, legend_y, self.cell_size, self.cell_size, 2, 2)
        
        painter.setPen(QColor(100, 100, 100))
        painter.drawText(legend_x + 35 + 5 * (self.cell_size + 2) + 5, legend_y + 10, tr("more", self.lang))
        
        # 호버링 툴팁 표시
        if self.hover_date and self.hover_pos:
            count = self.data.get(self.hover_date, 0)
            tooltip_text = f"{self.hover_date}: {count}회"
            
            painter.setFont(QFont("Arial", 10))
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(tooltip_text)
            text_height = fm.height()
            
            # 툴팁 배경 - 화면을 벗어나지 않도록 위치 조정
            padding = 5
            tooltip_width = text_width + padding * 2
            tooltip_height = text_height + padding * 2
            
            tooltip_x = self.hover_pos.x() + 10
            tooltip_y = self.hover_pos.y() - 25
            
            # 오른쪽으로 벗어나면 왼쪽에 표시
            if tooltip_x + tooltip_width > self.width():
                tooltip_x = self.hover_pos.x() - tooltip_width - 10
            
            # 위로 벗어나면 아래에 표시
            if tooltip_y < 0:
                tooltip_y = self.hover_pos.y() + 10
            
            painter.setBrush(QBrush(QColor(50, 50, 50, 230)))
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawRoundedRect(
                tooltip_x, tooltip_y,
                tooltip_width, tooltip_height,
                3, 3
            )
            
            # 툴팁 텍스트
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(
                tooltip_x + padding,
                tooltip_y + padding + fm.ascent(),
                tooltip_text
            )
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """마우스 움직임 감지"""
        today = date.today()
        start_date = today - timedelta(days=365)
        x_offset = 60
        y_offset = 20  # 월 표시 아래부터 시작
        
        mx = event.pos().x()
        my = event.pos().y()
        
        found = False
        for week in range(self.weeks):
            for day in range(self.days):
                cell_date = start_date + timedelta(weeks=week, days=day)
                if cell_date > today:
                    continue
                
                x = x_offset + week * (self.cell_size + self.cell_gap)
                y = y_offset + day * (self.cell_size + self.cell_gap)
                
                if x <= mx <= x + self.cell_size and y <= my <= y + self.cell_size:
                    self.hover_date = cell_date.isoformat()
                    self.hover_pos = event.pos()
                    found = True
                    self.update()
                    break
            if found:
                break
        
        if not found:
            if self.hover_date is not None:
                self.hover_date = None
                self.hover_pos = None
                self.update()
    
    def leaveEvent(self, event):
        """마우스가 위젯을 떠날 때"""
        self.hover_date = None
        self.hover_pos = None
        self.update()


# ============== 스크린샷 모드 위젯 ==============
class ScreenshotOverlay(QWidget):
    """스크린샷 모드 오버레이"""
    
    screenshot_taken = pyqtSignal(QPixmap)
    cancelled = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        
        self.start_pos = None
        self.end_pos = None
        self.selecting = False
        self.screenshot = None
        
    def start_capture(self):
        """스크린샷 캡처 시작"""
        screen = QGuiApplication.primaryScreen()
        self.screenshot = screen.grabWindow(0)
        self.setGeometry(screen.geometry())
        self.showFullScreen()
        self.activateWindow()
        
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        
        if self.screenshot:
            painter.drawPixmap(0, 0, self.screenshot)
        
        # 반투명 검은색 오버레이
        overlay = QColor(0, 0, 0, 128)
        painter.fillRect(self.rect(), overlay)
        
        # 선택 영역 그리기
        if self.start_pos and self.end_pos:
            rect = QRect(self.start_pos, self.end_pos).normalized()
            
            # 선택 영역에 원본 이미지 표시 (1:1 대응)
            if self.screenshot:
                # devicePixelRatio를 고려한 실제 영역 계산
                ratio = self.screenshot.devicePixelRatio()
                source_rect = QRect(
                    int(rect.x() * ratio),
                    int(rect.y() * ratio),
                    int(rect.width() * ratio),
                    int(rect.height() * ratio)
                )
                # 원본 크기로 그리기
                painter.drawPixmap(rect, self.screenshot, source_rect)
            
            # 흰색 테두리
            pen = QPen(QColor(255, 255, 255), 2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(rect)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.selecting = True
            self.update()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.selecting:
            self.end_pos = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.selecting:
            self.selecting = False
            self.end_pos = event.pos()
            
            if self.start_pos and self.end_pos:
                rect = QRect(self.start_pos, self.end_pos).normalized()
                if rect.width() > 10 and rect.height() > 10:
                    # devicePixelRatio를 고려하여 정확한 스크린샷 영역 계산
                    ratio = self.screenshot.devicePixelRatio()
                    scaled_rect = QRect(
                        int(rect.x() * ratio),
                        int(rect.y() * ratio),
                        int(rect.width() * ratio),
                        int(rect.height() * ratio)
                    )
                    cropped = self.screenshot.copy(scaled_rect)
                    self.hide()
                    self.screenshot_taken.emit(cropped)
                    return
            
            self.update()
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
            self.cancelled.emit()


# ============== 이미지 뷰어 윈도우 ==============
class ImageViewerWindow(QWidget):
    """크로키 이미지 뷰어 윈도우"""
    
    croquis_completed = pyqtSignal()
    croquis_saved = pyqtSignal(QPixmap, QPixmap, int, str, dict)  # 원본, 스크린샷, 시간, 파일명, 메타데이터
    
    def __init__(self, settings: CroquisSettings, images: List[Any], lang: str = "ko", parent=None):
        super().__init__(parent)
        self.settings = settings
        self.images = images  # str (파일 경로) 또는 dict (이미지 데이터) 리스트
        self.lang = lang
        self.current_index = 0
        self.paused = False
        self.remaining_time = settings.time_seconds if not settings.study_mode else 0
        self.elapsed_time = 0  # 학습 모드용 경과 시간
        self.random_seed = None
        
        if settings.random_order:
            self.random_seed = random.randint(0, 1000000)
            random.seed(self.random_seed)
            # 난이도 기반 가중치 랜덤 선택
            self.images = self.weighted_shuffle(self.images)
        
        self.setup_ui()
        self.setup_timer()
        self.load_current_image()
    
    def weighted_shuffle(self, images: List[Any]) -> List[Any]:
        """난이도 기반 가중치 랜덤 선택"""
        if not images:
            return images
        
        # 가중치 계산 (난이도가 높을수록 더 자주 나옴)
        weights = []
        for img in images:
            if isinstance(img, dict):
                difficulty = img.get("difficulty", 1)
                # 난이도^2로 가중치 계산 (1→1, 2→4, 3→9, 4→16, 5→25)
                weight = difficulty * difficulty
                weights.append(weight)
            else:
                weights.append(1)
        
        # 가중치 기반 무작위 선택
        total_weight = sum(weights)
        if total_weight == 0:
            return images
        
        result = []
        remaining = images.copy()
        remaining_weights = weights.copy()
        
        while remaining:
            # 확률 계산
            cumulative = []
            cumsum = 0
            for w in remaining_weights:
                cumsum += w
                cumulative.append(cumsum)
            
            # 무작위 선택
            rand_val = random.random() * cumsum
            for i, cum in enumerate(cumulative):
                if rand_val <= cum:
                    result.append(remaining[i])
                    remaining.pop(i)
                    remaining_weights.pop(i)
                    break
        
        return result
        
    def setup_ui(self):
        self.setWindowTitle(tr("app_title", self.lang))
        self.resize(self.settings.image_width, self.settings.image_height + 50)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 이미지 표시 영역
        self.image_container = QWidget()
        self.image_container.setMinimumSize(self.settings.image_width, self.settings.image_height)
        image_layout = QVBoxLayout(self.image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #2a2a2a;")
        image_layout.addWidget(self.image_label)
        
        # 타이머 라벨 (이미지 위에 오버레이)
        self.timer_label = QLabel(self.image_container)
        self.timer_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                padding: 5px 10px;
                border-radius: 5px;
            }
        """)
        self.update_timer_position()
        self.update_timer_font()
        
        layout.addWidget(self.image_container, 1)
        
        # 컨트롤 버튼 영역
        control_widget = QWidget()
        control_widget.setStyleSheet("background-color: #333;")
        control_layout = QHBoxLayout(control_widget)
        control_layout.setContentsMargins(10, 5, 10, 5)
        
        # 아이콘 버튼들
        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setToolTip(tr("previous", self.lang))
        self.prev_btn.clicked.connect(self.previous_image)
        
        self.pause_btn = QPushButton("⏸")
        self.pause_btn.setToolTip(tr("pause", self.lang))
        self.pause_btn.clicked.connect(self.toggle_pause)
        
        self.next_btn = QPushButton("⏭")
        self.next_btn.setToolTip(tr("next", self.lang))
        self.next_btn.clicked.connect(self.next_image_no_screenshot)
        
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setToolTip(tr("stop", self.lang))
        self.stop_btn.clicked.connect(self.stop_croquis)
        
        for btn in [self.prev_btn, self.pause_btn, self.next_btn, self.stop_btn]:
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #555;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
            """)
        
        control_layout.addStretch()
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.next_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        
        layout.addWidget(control_widget)
        
        # 스크린샷 오버레이
        self.screenshot_overlay = ScreenshotOverlay()
        self.screenshot_overlay.screenshot_taken.connect(self.on_screenshot_taken)
        self.screenshot_overlay.cancelled.connect(self.on_screenshot_cancelled)
        
    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.start(1000)
        
    def update_timer_position(self):
        pos = self.settings.timer_position
        margin = 10
        
        self.timer_label.adjustSize()
        w = self.timer_label.width()
        h = self.timer_label.height()
        cw = self.image_container.width()
        ch = self.image_container.height()
        
        positions = {
            "bottom_right": (cw - w - margin, ch - h - margin),
            "bottom_center": ((cw - w) // 2, ch - h - margin),
            "bottom_left": (margin, ch - h - margin),
            "top_right": (cw - w - margin, margin),
            "top_center": ((cw - w) // 2, margin),
            "top_left": (margin, margin),
        }
        
        x, y = positions.get(pos, positions["bottom_right"])
        self.timer_label.move(x, y)
        
    def update_timer_font(self):
        sizes = {"large": 24, "medium": 18, "small": 12}
        size = sizes.get(self.settings.timer_font_size, 24)
        font = QFont("Arial", size, QFont.Weight.Bold)
        self.timer_label.setFont(font)
        
    def load_current_image(self):
        if 0 <= self.current_index < len(self.images):
            image_item = self.images[self.current_index]
            
            # 이미지 로드 (dict 또는 str)
            if isinstance(image_item, dict):
                # 새로운 형식: dict에서 image_data 디코딩
                try:
                    image_data_b64 = image_item.get("image_data", "")
                    image_bytes = base64.b64decode(image_data_b64)
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_bytes)
                    self.current_filename = image_item.get("filename", "unknown")
                except Exception as e:
                    print(f"이미지 로드 실패: {e}")
                    return
            else:
                # 구버전 형식: 파일 경로에서 직접 로드
                pixmap = QPixmap(image_item)
                self.current_filename = os.path.basename(image_item)
            
            if self.settings.grayscale:
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_Grayscale8)
                pixmap = QPixmap.fromImage(image)
            
            if self.settings.flip_horizontal:
                pixmap = pixmap.transformed(pixmap.transform().scale(-1, 1))
            
            scaled = pixmap.scaled(
                self.settings.image_width, 
                self.settings.image_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
            self.current_pixmap = pixmap
            
            if self.settings.study_mode:
                self.elapsed_time = 0
            else:
                self.remaining_time = self.settings.time_seconds
            self.update_timer_display()
            
    def update_timer_display(self):
        if self.settings.study_mode:
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
        else:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
        self.timer_label.adjustSize()
        self.update_timer_position()
        
    def on_timer_tick(self):
        if not self.paused and hasattr(self, 'timer') and self.timer:
            if self.settings.study_mode:
                # 학습 모드: 시간 증가
                self.elapsed_time += 1
                self.update_timer_display()
            else:
                # 일반 모드: 시간 감소
                if self.remaining_time > 0:
                    self.remaining_time -= 1
                    self.update_timer_display()
                    
                    if self.remaining_time == 0:
                        self.timer.stop()
                        self.start_screenshot_mode()
                
    def start_screenshot_mode(self):
        logger.info("스크린샷 모드 돌입")
        self.screenshot_overlay.start_capture()
        
    def on_screenshot_taken(self, screenshot: QPixmap):
        # 커스텀 다이얼로그 생성
        dialog = QDialog(self)
        dialog.setWindowTitle(tr("save_croquis", self.lang))
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # 큰 이미지 표시
        image_label = QLabel()
        preview = screenshot.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(preview)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)
        
        # 질문 문구
        question_label = QLabel(tr("save_question", self.lang))
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_label.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(question_label)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        yes_btn = QPushButton(tr("yes", self.lang))
        yes_btn.setMinimumWidth(100)
        yes_btn.setMinimumHeight(35)
        yes_btn.clicked.connect(dialog.accept)
        
        no_btn = QPushButton(tr("no", self.lang))
        no_btn.setMinimumWidth(100)
        no_btn.setMinimumHeight(35)
        no_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(yes_btn)
        button_layout.addWidget(no_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            self.save_croquis_pair(screenshot)
            self.next_image()
        else:
            self.start_screenshot_mode()
            
    def on_screenshot_cancelled(self):
        logger.info("스크린샷 모드 취소")
        self.start_screenshot_mode()
        
    def save_croquis_pair(self, screenshot: QPixmap):
        """크로키 이미지 페어 암호화 저장"""
        logger.info("크로키 페어 저장")
        # 크로키 시간 계산
        if self.settings.study_mode:
            croquis_time = self.elapsed_time
        else:
            croquis_time = self.settings.time_seconds
        
        # 현재 이미지 정보 추출
        current_image = self.images[self.current_index]
        
        if isinstance(current_image, dict):
            # 새로운 형식: dict에서 메타데이터 직접 사용
            image_filename = os.path.splitext(current_image.get("filename", "unknown"))[0]
            image_metadata = {
                "filename": current_image.get("filename", "unknown"),
                "path": current_image.get("original_path", ""),
                "width": current_image.get("width", self.current_pixmap.width()),
                "height": current_image.get("height", self.current_pixmap.height()),
                "size": current_image.get("size", 0)
            }
        else:
            # 구버전 형식: 파일 경로에서 메타데이터 추출
            current_image_path = current_image
            image_filename = os.path.splitext(os.path.basename(current_image_path))[0]
            image_metadata = {
                "filename": os.path.basename(current_image_path),
                "path": current_image_path,
                "width": self.current_pixmap.width(),
                "height": self.current_pixmap.height(),
                "size": os.path.getsize(current_image_path) if os.path.exists(current_image_path) else 0
            }
        
        self.croquis_saved.emit(self.current_pixmap, screenshot, croquis_time, image_filename, image_metadata)
        
    def previous_image(self):
        logger.info("이전 크로키")
        if self.settings.study_mode:
            # 학습 모드: 스크린샷 모드로 전환
            self.timer.stop()
            self.start_screenshot_mode()
        elif self.current_index > 0:
            self.current_index -= 1
            self.load_current_image()
            self.timer.start(1000)
            
    def next_image(self):
        logger.info("다음 크로키")
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
        else:
            # 무한 반복: 처음으로 돌아감
            self.current_index = 0
        self.load_current_image()
        self.timer.start(1000)
            
    def next_image_no_screenshot(self):
        if self.settings.study_mode:
            # 학습 모드: 스크린샷 모드로 전환
            self.timer.stop()
            self.start_screenshot_mode()
        else:
            self.next_image()
        
    def toggle_pause(self):
        self.paused = not self.paused
        logger.info(f"크로키 {'정지' if self.paused else '재생'}")
        if self.paused:
            self.pause_btn.setText("▶")
            self.pause_btn.setToolTip(tr("play", self.lang))
        else:
            self.pause_btn.setText("⏸")
            self.pause_btn.setToolTip(tr("pause", self.lang))
            if self.remaining_time == 0:
                self.next_image()
                
    def stop_croquis(self):
        logger.info("크로키 종료")
        if hasattr(self, 'timer') and self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        if hasattr(self, 'screenshot_overlay'):
            self.screenshot_overlay.hide()
            self.screenshot_overlay.close()
            self.screenshot_overlay = None
        self.croquis_completed.emit()
        self.close()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_timer_position()


# ============== 난이도 위젯 ==============
class DifficultyWidget(QWidget):
    """난이도 표시 위젯 (숫자 + 색상별 별표)"""
    
    def __init__(self, difficulty: int, parent=None):
        super().__init__(parent)
        self.difficulty = difficulty
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(3)
        
        # 배경 설정
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 8px;
            }
        """)
        
        # 1층: 난이도 숫자 (흰색)
        number_label = QLabel(str(self.difficulty))
        number_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 11px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        layout.addWidget(number_label)
        
        # 2층: 별표 위젯 (투명 배경, 색상별 별표)
        star_label = QLabel("★")
        colors = ["#FFD700", "#FFA500", "#FF8C00", "#FF4500", "#FF0000"]
        color = colors[self.difficulty - 1] if 1 <= self.difficulty <= 5 else "#FFD700"
        star_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 11px;
                font-weight: bold;
                background-color: transparent;
            }}
        """)
        layout.addWidget(star_label)
        
        self.setFixedHeight(20)


# ============== 덱 아이템 위젯 ==============
class DeckItemWidget(QWidget):
    """덱 편집창의 아이템 위젯 (이미지 + 클릭 가능한 난이도)"""
    
    def __init__(self, pixmap: QPixmap, img_data: dict, parent_window, parent=None):
        super().__init__(parent)
        self.pixmap = pixmap
        self.img_data = img_data
        self.parent_window = parent_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # 이미지 컨테이너
        container = QWidget()
        container.setFixedSize(100, 120)
        
        # 이미지 라벨
        image_label = QLabel(container)
        image_label.setPixmap(self.pixmap)
        image_label.setFixedSize(100, 120)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 난이도 버튼 (클릭 가능)
        difficulty = self.img_data.get("difficulty", 1)
        self.difficulty_btn = QPushButton(container)
        self.difficulty_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_difficulty_display()
        self.difficulty_btn.clicked.connect(self.cycle_difficulty)
        
        layout.addWidget(container)
        
        # 파일명
        filename_label = QLabel(f"{self.img_data['filename']})")
        filename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filename_label.setWordWrap(True)
        filename_label.setStyleSheet("font-size: 9px;")
        layout.addWidget(filename_label)
        
        self.filename_label = filename_label
    
    def update_difficulty_display(self):
        """난이도 표시 업데이트"""
        difficulty = self.img_data.get("difficulty", 1)
        
        # 색상 설정
        colors = ["#FFD700", "#FFA500", "#FF8C00", "#FF4500", "#FF0000"]
        color = colors[difficulty - 1] if 1 <= difficulty <= 5 else "#FFD700"
        
        # 난이도 위젯 생성
        diff_widget = DifficultyWidget(difficulty)
        diff_widget.resize(diff_widget.sizeHint())
        
        # 난이도 위젯을 픽스맵으로 렌더링
        diff_pixmap = QPixmap(diff_widget.size())
        diff_pixmap.fill(Qt.GlobalColor.transparent)
        diff_widget.render(diff_pixmap)
        
        # 버튼에 아이콘으로 설정
        self.difficulty_btn.setIcon(QIcon(diff_pixmap))
        self.difficulty_btn.setIconSize(diff_pixmap.size())
        self.difficulty_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
        """)
        
        # 버튼 위치 (우측 하단)
        btn_size = diff_pixmap.size()
        self.difficulty_btn.setFixedSize(btn_size)
        self.difficulty_btn.move(100 - btn_size.width() - 5, 120 - btn_size.height() - 5)
    
    def cycle_difficulty(self):
        """난이도 순환 (1→2→3→4→5→1)"""
        current = self.img_data.get("difficulty", 1)
        new_difficulty = (current % 5) + 1
        
        self.img_data["difficulty"] = new_difficulty
        logger.info(f"난이도 변경: {self.img_data['filename']} -> {new_difficulty}")
        
        # 부모 윈도우의 deck_images 업데이트
        filename = self.img_data["filename"]
        for i, deck_img in enumerate(self.parent_window.deck_images):
            if deck_img.get("filename") == filename:
                self.parent_window.deck_images[i]["difficulty"] = new_difficulty
                break
        
        # UI 업데이트
        self.update_difficulty_display()
        
        # 파일명 라벨도 업데이트
        self.filename_label.setText(f"{self.img_data['filename']})")
        
        self.parent_window.save_temp_file()
        self.parent_window.mark_modified()


# ============== 크로키 덱 편집기 ==============
class DeckEditorWindow(QMainWindow):
    """크로키 덱 편집 윈도우"""
    
    def __init__(self, lang: str = "ko", dark_mode: bool = False, parent=None):
        super().__init__(parent)
        self.lang = lang
        self.dark_mode = dark_mode
        self.deck_images: List[Dict[str, Any]] = []  # 이미지 정보 딕셔너리 리스트로 변경
        self.current_deck_path = None
        self.temp_file_path = None  # 임시 파일 경로
        self.is_modified = False  # 수정 상태
        self.setup_temp_file()
        self.setup_ui()
        self.apply_dark_mode()
        self.update_title()
    
    def setup_temp_file(self):
        """임시 파일 초기화"""
        temp_dir = Path(__file__).parent / "temp"
        temp_dir.mkdir(exist_ok=True)
        
        # 고유한 임시 파일명 생성
        import uuid
        temp_id = str(uuid.uuid4())[:8]
        self.temp_file_path = temp_dir / f"deck_{temp_id}.temp"
        
        # 빈 임시 파일 생성
        self.save_temp_file()
    
    def save_temp_file(self):
        """임시 파일에 현재 덱 상태 저장 (비동기)"""
        if not self.temp_file_path:
            return
        
        # QTimer를 사용하여 비동기 저장
        QTimer.singleShot(0, self._save_temp_file_async)
    
    def _save_temp_file_async(self):
        """임시 파일 비동기 저장"""
        try:
            data = {
                "images": self.deck_images,
                "current_path": self.current_deck_path
            }
            
            encrypted = encrypt_data(data)
            
            with open(self.temp_file_path, "wb") as f:
                f.write(encrypted)
        except Exception as e:
            print(f"임시 파일 저장 실패: {e}")
    
    def load_temp_file(self, source_path: str = None):
        """임시 파일 로드 (덱 파일에서 복사하거나 새로 시작)"""
        try:
            if source_path and os.path.exists(source_path):
                # 기존 덱에서 복사
                with open(source_path, "rb") as f:
                    encrypted = f.read()
                data = decrypt_data(encrypted)
                self.deck_images = data.get("images", [])
            else:
                # 새로 시작
                self.deck_images = []
            
            self.save_temp_file()
            self.update_image_list()
        except Exception as e:
            print(f"임시 파일 로드 실패: {e}")
            self.deck_images = []
    
    def cleanup_temp_file(self):
        """임시 파일 삭제"""
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            try:
                os.unlink(self.temp_file_path)
            except Exception as e:
                print(f"임시 파일 삭제 실패: {e}")
        
    def setup_ui(self):
        self.setWindowTitle(tr("edit_deck", self.lang))
        self.resize(1000, 600)
        
        # 메뉴바
        menubar = self.menuBar()
        file_menu = menubar.addMenu(tr("file", self.lang))
        
        new_action = QAction(tr("new", self.lang), self)
        new_action.triggered.connect(self.new_deck)
        file_menu.addAction(new_action)
        
        open_action = QAction(tr("open", self.lang), self)
        open_action.triggered.connect(self.open_deck)
        file_menu.addAction(open_action)
        
        save_action = QAction(tr("save", self.lang), self)
        save_action.triggered.connect(self.save_deck)
        file_menu.addAction(save_action)
        
        self.save_as_action = QAction(tr("save_as", self.lang), self)
        self.save_as_action.triggered.connect(self.save_deck_as)
        file_menu.addAction(self.save_as_action)
        
        # 중앙 위젯
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # 왼쪽: 덱 이미지 영역
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # 상단 버튼들
        button_layout = QHBoxLayout()
        import_btn = QPushButton(tr("import_images", self.lang))
        import_btn.clicked.connect(self.import_images)
        button_layout.addWidget(import_btn)
        
        delete_btn = QPushButton("선택 삭제")
        delete_btn.clicked.connect(self.delete_selected_images)
        button_layout.addWidget(delete_btn)
        
        self.checkbox_btn = QCheckBox("체크박스 표시")
        self.checkbox_btn.stateChanged.connect(self.toggle_checkboxes)
        button_layout.addWidget(self.checkbox_btn)
        button_layout.addStretch()
        
        left_layout.addLayout(button_layout)
        
        self.image_list = QListWidget()
        self.image_list.setIconSize(QSize(100, 120))
        self.image_list.setGridSize(QSize(120, 160))  # 아이콘 + 텍스트 공간
        self.image_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.image_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.image_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.image_list.setSpacing(3)
        self.image_list.setWordWrap(True)
        self.image_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.image_list.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.image_list.setStyleSheet("""
            QListWidget::item {
                text-align: center;
                padding: 3px;
            }
            QListWidget::item:selected {
                background-color: rgba(0, 120, 212, 0.2);
            }
            QListWidget::item:hover {
                background-color: rgba(0, 120, 212, 0.1);
            }
            QListWidget {
                outline: none;
            }
        """)
        # 드래그로 순서 변경 활성화
        self.image_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.image_list.model().rowsMoved.connect(self.on_items_reordered)
        # 클릭 이벤트 (크로키 목록 표시)
        self.image_list.itemClicked.connect(self.on_deck_item_clicked)
        left_layout.addWidget(self.image_list)
        
        # 드래그 앤 드롭 활성화
        self.image_list.setDragEnabled(True)
        self.setAcceptDrops(True)
        
        layout.addWidget(left_widget, 2)
        
        # 오른쪽: 크로키 목록
        right_widget = QGroupBox("크로키 목록")
        right_layout = QVBoxLayout(right_widget)
        
        # 안내 라벨
        self.croquis_info_label = QLabel("이미지를 선택하면 해당 이미지로 그린 크로키 목록이 표시됩니다.")
        self.croquis_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.croquis_info_label.setWordWrap(True)
        self.croquis_info_label.setStyleSheet("color: gray; padding: 20px;")
        right_layout.addWidget(self.croquis_info_label)
        
        # 크로키 목록 리스트
        self.croquis_list = QListWidget()
        self.croquis_list.setIconSize(QSize(100, 120))
        self.croquis_list.setGridSize(QSize(120, 160))
        self.croquis_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.croquis_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.croquis_list.setSpacing(5)
        self.croquis_list.setStyleSheet("""
            QListWidget::item {
                text-align: center;
                padding: 3px;
            }
            QListWidget::item:selected {
                background-color: rgba(0, 120, 212, 0.2);
            }
        """)
        self.croquis_list.itemClicked.connect(self.show_croquis_large_view)
        self.croquis_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.croquis_list.customContextMenuRequested.connect(self.show_croquis_context_menu)
        self.croquis_list.hide()  # 처음에는 숨김
        right_layout.addWidget(self.croquis_list)
        
        layout.addWidget(right_widget, 1)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() or event.mimeData().hasText() or event.mimeData().hasHtml():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        # URL 드롭 처리
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                path = url.toLocalFile()
                if path and path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    self.add_image_to_deck(path)
                elif not path:  # URL이지만 로컬 파일이 아닌 경우
                    url_str = url.toString()
                    if url_str.startswith('http://') or url_str.startswith('https://'):
                        self.download_image_from_url(url_str)
        
        # 텍스트/URL 드롭 처리 (핀터레스트 등)
        elif event.mimeData().hasText():
            text = event.mimeData().text().strip()
            # URL 패턴 감지
            if text.startswith('http://') or text.startswith('https://'):
                self.download_image_from_url(text)
        
        # HTML 드롭 처리 (핀터레스트가 HTML로 데이터를 전달할 수 있음)
        elif event.mimeData().hasHtml():
            html = event.mimeData().html()
            # HTML에서 URL 추출
            import re
            # img src 패턴 찾기
            img_patterns = [
                r'<img[^>]+src=["\']([^"\' ]+)["\']',
                r'https?://[^\s<>"\']+(\.(jpg|jpeg|png|gif|bmp|webp))',
            ]
            for pattern in img_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    for match in matches:
                        url = match if isinstance(match, str) else match[0]
                        if url.startswith('http://') or url.startswith('https://'):
                            self.download_image_from_url(url)
                            break
                    break
    
    def download_image_from_url(self, url: str):
        """URL에서 이미지 다운로드"""
        try:
            import urllib.request
            import tempfile
            import re
            from urllib.parse import urlparse, unquote
            
            # 핀터레스트 URL인 경우 이미지 URL 추출
            if 'pinterest.com' in url:
                # 핀터레스트 페이지에서 이미지 추출 시도
                try:
                    import ssl
                    import json
                    
                    # SSL 컨텍스트 생성
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                    # User-Agent 헤더 추가
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    req = urllib.request.Request(url, headers=headers)
                    
                    with urllib.request.urlopen(req, context=context, timeout=10) as response:
                        html = response.read().decode('utf-8')
                        
                        # 이미지 URL 패턴 찾기 (핀터레스트 originals)
                        patterns = [
                            r'"url":"(https://i\.pinimg\.com/originals/[^"]+)"',
                            r'"url":"(https://i\.pinimg\.com/[0-9]+x/[^"]+)"',
                            r'<meta property="og:image" content="([^"]+)"'
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, html)
                            if matches:
                                # 가장 큰 이미지 URL 사용
                                image_url = matches[0].replace('\\/', '/')
                                url = image_url
                                break
                except Exception as e:
                    print(f"핀터레스트 이미지 추출 실패: {e}")
                    QMessageBox.warning(self, "경고", "핀터레스트 이미지를 추출할 수 없습니다. 이미지를 우클릭하여 '이미지 주소 복사'로 직접 이미지 URL을 드래그해주세요.")
                    return
            
            # 이미지 다운로드
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                image_data = response.read()
                
                # 임시 파일로 저장
                parsed_url = urlparse(url)
                filename = os.path.basename(unquote(parsed_url.path))
                
                # 파일명이 없거나 확장자가 없으면 기본 이름 사용
                if not filename or '.' not in filename:
                    filename = f"downloaded_{hash(url) % 100000}.jpg"
                
                # 덱 폴더에 저장
                deck_folder = Path(__file__).parent / "deck_images"
                deck_folder.mkdir(exist_ok=True)
                
                save_path = deck_folder / filename
                counter = 1
                while save_path.exists():
                    name, ext = os.path.splitext(filename)
                    save_path = deck_folder / f"{name}_{counter}{ext}"
                    counter += 1
                
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                
                # 덱에 추가
                self.add_image_to_deck(str(save_path))
                # 팝업 제거 - 자동으로 추가됨
                
        except Exception as e:
            QMessageBox.warning(self, "오류", f"이미지를 다운로드하는 중 오류가 발생했습니다:\n{str(e)}")
                
    def add_image_to_deck(self, path: str, difficulty: int = 1):
        """이미지를 덱에 추가 (이미지 정보 저장)"""
        # 이미 추가된 이미지인지 확인 (filename 기반)
        filename = os.path.basename(path)
        logger.info(f"덱에 이미지 추가: {filename}")
        for img_data in self.deck_images:
            if img_data.get("filename") == filename:
                return  # 이미 추가됨
        
        try:
            # 이미지 검증 및 정보 추출
            pixmap = QPixmap(path)
            if pixmap.isNull():
                QMessageBox.warning(self, "경고", f"올바른 이미지 파일이 아닙니다: {filename}")
                return
            
            # 이미지를 바이트로 변환 (QBuffer 사용)
            from PyQt6.QtCore import QBuffer, QIODevice
            buffer = QBuffer()
            buffer.open(QIODevice.OpenModeFlag.WriteOnly)
            pixmap.save(buffer, "PNG")
            image_bytes = buffer.data().data()
            
            # 이미지 정보 딕셔너리 생성
            image_data = {
                "filename": filename,
                "original_path": path,
                "width": pixmap.width(),
                "height": pixmap.height(),
                "size": len(image_bytes),
                "image_data": base64.b64encode(image_bytes).decode(),
                "difficulty": difficulty
            }
            
            self.deck_images.append(image_data)
            self.save_temp_file()  # 임시 파일 업데이트
            self.update_image_list()  # UI 업데이트
            self.mark_modified()
            
        except Exception as e:
            QMessageBox.warning(self, "오류", f"이미지 추가 실패: {str(e)}")
    
    def update_image_list(self):
        """이미지 리스트 UI 업데이트"""
        self.image_list.clear()
        
        for idx, img_data in enumerate(self.deck_images):
            try:
                # 이미지 데이터에서 픽스맵 생성
                image_bytes = base64.b64decode(img_data["image_data"])
                pixmap = QPixmap()
                pixmap.loadFromData(image_bytes)
                
                # 100x120 범위 내에서 가로 또는 세로 중 하나가 꽉 차도록 스케일링
                img_ratio = pixmap.width() / pixmap.height()
                box_ratio = 100 / 120
                
                if img_ratio > box_ratio:
                    # 이미지가 더 넓음 → 가로를 100으로 고정
                    scaled_pixmap = pixmap.scaledToWidth(100, Qt.TransformationMode.SmoothTransformation)
                else:
                    # 이미지가 더 높음 → 세로를 120으로 고정
                    scaled_pixmap = pixmap.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation)
                
                # 100x120 캔버스에 중앙 정렬 (잘라내기)
                canvas = QPixmap(100, 120)
                canvas.fill(Qt.GlobalColor.transparent)
                
                painter = QPainter(canvas)
                x = (100 - scaled_pixmap.width()) // 2
                y = (120 - scaled_pixmap.height()) // 2
                
                # 클리핑 영역 설정
                from PyQt6.QtCore import QRect
                source_x = max(0, -x)
                source_y = max(0, -y)
                source_w = min(scaled_pixmap.width() - source_x, 100)
                source_h = min(scaled_pixmap.height() - source_y, 120)
                
                target_x = max(0, x)
                target_y = max(0, y)
                
                painter.drawPixmap(target_x, target_y, scaled_pixmap, source_x, source_y, source_w, source_h)
                painter.end()
                
                # 리스트 아이템 생성
                item = QListWidgetItem()
                item.setSizeHint(QSize(120, 160))  # 아이콘 + 텍스트 + 여백
                
                # 이미지 데이터를 UserRole에 저장
                item.setData(Qt.ItemDataRole.UserRole, img_data)
                
                self.image_list.addItem(item)
                
                # 커스텀 위젯 생성 및 설정
                widget = DeckItemWidget(canvas, img_data, self)
                self.image_list.setItemWidget(item, widget)
                
            except Exception as e:
                print(f"이미지 로드 실패: {e}")
            
    def import_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            tr("import_images", self.lang),
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp *.webp)"
        )
        for f in files:
            self.add_image_to_deck(f)
        
        # Save As 메뉴 상태 업데이트
        if files:
            self.update_title()
            
    def on_image_selected(self, item: QListWidgetItem):
        """이미지 선택 시 해당 이미지로 그린 크로키 목록 표시"""
        img_data = item.data(Qt.ItemDataRole.UserRole)
        if not img_data:
            return
        
        # 안내 라벨 숨기고 크로키 목록 표시
        self.croquis_info_label.hide()
        self.croquis_list.show()
        
        # 크로키 목록 로드 (비동기로 처리) - filename 기반
        filename = img_data.get("filename", "")
        if filename:
            self.load_croquis_for_image(filename)
            
    def new_deck(self):
        """새 덱 생성"""
        logger.info("새 덱 만들기")
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "저장 확인",
                "현재 파일이 수정되었습니다. 저장하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.save_deck()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
        
        # 기존 임시 파일 삭제
        self.cleanup_temp_file()
        
        # 새 임시 파일 생성
        self.setup_temp_file()
        
        self.deck_images.clear()
        self.current_deck_path = None
        self.is_modified = False
        
        # UI 초기화
        self.update_image_list()
        self.croquis_list.clear()
        self.croquis_list.hide()
        self.croquis_info_label.show()
        
        self.update_title()
        
    def open_deck(self):
        """덱 불러오기"""
        logger.info("덱 불러오기")
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "저장 확인",
                "현재 파일이 수정되었습니다. 저장하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.save_deck()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
        
        path, _ = QFileDialog.getOpenFileName(
            self,
            tr("open", self.lang),
            "",
            "Croquis Deck Files (*.crdk)"
        )
        if path:
            try:
                # 기존 임시 파일 삭제
                self.cleanup_temp_file()
                
                # 덱 파일에서 임시 파일로 복사
                self.load_temp_file(path)
                
                self.current_deck_path = path
                self.is_modified = False
                self.update_title()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"파일을 불러오는 중 오류가 발생했습니다: {str(e)}")
                
    def save_deck(self):
        """덱 저장 - 임시 파일을 덱 파일로 복사"""
        logger.info("덱 저장")
        if self.current_deck_path:
            self._save_to_path(self.current_deck_path)
        else:
            self.save_deck_as()
            
    def save_deck_as(self):
        """다른 이름으로 저장"""
        path, _ = QFileDialog.getSaveFileName(
            self,
            tr("save_as", self.lang),
            "",
            "Croquis Deck Files (*.crdk)"
        )
        if path:
            if not path.endswith('.crdk'):
                path += '.crdk'
            self._save_to_path(path)
            
    def _save_to_path(self, path: str):
        """파일에 저장 - temp 파일을 target 경로로 복사"""
        try:
            # temp 파일이 존재하는지 확인
            if not self.temp_file_path or not os.path.exists(self.temp_file_path):
                QMessageBox.warning(self, "저장 오류", "임시 파일을 찾을 수 없습니다.")
                return
            
            # temp 파일을 target 경로로 복사
            import shutil
            shutil.copy2(self.temp_file_path, path)
            
            self.current_deck_path = path
            self.is_modified = False
            self.update_title()
            
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", f"파일 저장 중 오류가 발생했습니다:\n{str(e)}")
    
    def delete_selected_images(self):
        """선택된 이미지 삭제"""
        selected_items = self.image_list.selectedItems()
        if not selected_items:
            return
        
        logger.info(f"이미지 삭제: {len(selected_items)}개")
        
        # 선택된 아이템들의 filename 수집
        filenames_to_delete = []
        for item in selected_items:
            img_data = item.data(Qt.ItemDataRole.UserRole)
            if img_data and isinstance(img_data, dict):
                filenames_to_delete.append(img_data["filename"])
        
        # deck_images에서 해당 파일들 제거
        self.deck_images = [img for img in self.deck_images if img["filename"] not in filenames_to_delete]
        
        # UI 업데이트
        self.update_image_list()
        
        # 크로키 목록 초기화
        self.croquis_list.clear()
        self.croquis_list.hide()
        self.croquis_info_label.show()
        
        # temp 파일 저장
        self.save_temp_file()
        self.mark_modified()
    
    def toggle_checkboxes(self, state: int):
        """체크박스 표시/숨김"""
        # PyQt6의 QListWidget은 기본적으로 체크박스를 지원하지 않으므로
        # 선택 모드를 활용합니다
        if state == Qt.CheckState.Checked.value:
            self.image_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        else:
            self.image_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
    
    def on_items_reordered(self):
        """아이템 순서 변경 시"""
        logger.info("이미지 순서 변경")
        # deck_images 리스트를 새로운 순서로 업데이트
        new_order = []
        for i in range(self.image_list.count()):
            item = self.image_list.item(i)
            img_data = item.data(Qt.ItemDataRole.UserRole)
            if img_data and isinstance(img_data, dict):
                new_order.append(img_data)
        
        self.deck_images = new_order
        
        # temp 파일 저장
        self.save_temp_file()
        self.mark_modified()
    
    def on_deck_item_clicked(self, item: QListWidgetItem):
        """덱 아이템 클릭 시 크로키 목록 표시"""
        img_data = item.data(Qt.ItemDataRole.UserRole)
        if not img_data:
            return
        
        # 안내 라벨 숨기고 크로키 목록 표시
        self.croquis_info_label.hide()
        self.croquis_list.show()
        
        # 크로키 목록 로드
        filename = img_data.get("filename", "")
        if filename:
            self.load_croquis_for_image(filename)
    
    def update_title(self):
        """창 제목 업데이트"""
        title = tr("edit_deck", self.lang)
        
        if self.current_deck_path:
            filename = os.path.basename(self.current_deck_path)
            title += f" - {filename}"
        else:
            title += " - 제목 없음"
        
        if self.is_modified:
            title += " *"
        
        self.setWindowTitle(title)
        
        # Save As 메뉴 활성화 상태 관리
        # 파일이 없어도 이미지가 있으면 Save As 가능
        self.save_as_action.setEnabled(len(self.deck_images) > 0)
    
    def mark_modified(self):
        """수정 상태로 표시"""
        if not self.is_modified:
            self.is_modified = True
            self.update_title()
    
    def load_croquis_for_image(self, image_path: str):
        """선택한 이미지로 그린 크로키 목록 로드"""
        self.croquis_list.clear()
        
        # 로딩 메시지 표시
        loading_item = QListWidgetItem("로딩 중...")
        self.croquis_list.addItem(loading_item)
        
        # QTimer를 사용하여 비동기식으로 처리
        QTimer.singleShot(0, lambda: self._load_croquis_async(image_path))
    
    def _load_croquis_async(self, image_path: str):
        """크로키 목록을 실제로 로드하는 내부 메서드"""
        self.croquis_list.clear()
        
        pairs_dir = Path(__file__).parent / "croquis_pairs"
        if not pairs_dir.exists():
            no_data_item = QListWidgetItem("저장된 크로키가 없습니다.")
            self.croquis_list.addItem(no_data_item)
            return
        
        image_filename = os.path.basename(image_path)
        found_count = 0
        
        try:
            # 모든 .croq 파일 검색
            for file in sorted(pairs_dir.glob("*.croq"), reverse=True):
                try:
                    with open(file, "rb") as f:
                        encrypted = f.read()
                    
                    key = base64.urlsafe_b64encode(hashlib.sha256(b"croquis_secret_key").digest())
                    fernet = Fernet(key)
                    decrypted = fernet.decrypt(encrypted)
                    data = json.loads(decrypted.decode())
                    
                    # 메타데이터 확인
                    metadata = data.get("image_metadata", {})
                    file_metadata_name = metadata.get("filename", "")
                    
                    # 메타데이터가 없는 구버전 파일은 건너뛰기
                    if not file_metadata_name:
                        continue
                    
                    # 파일명 매칭
                    if file_metadata_name == image_filename:
                        found_count += 1
                        
                        # 크로키 이미지 로드
                        screenshot_bytes = base64.b64decode(data["screenshot"])
                        screenshot_pixmap = QPixmap()
                        screenshot_pixmap.loadFromData(screenshot_bytes)
                        
                        # 썸네일 생성 (100x120 고정 크기)
                        scaled_thumb = screenshot_pixmap.scaled(100, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        
                        # 100x120 캔버스에 중앙 정렬
                        thumbnail = QPixmap(100, 120)
                        thumbnail.fill(Qt.GlobalColor.transparent)
                        thumb_painter = QPainter(thumbnail)
                        thumb_x = (100 - scaled_thumb.width()) // 2
                        thumb_y = (120 - scaled_thumb.height()) // 2
                        thumb_painter.drawPixmap(thumb_x, thumb_y, scaled_thumb)
                        thumb_painter.end()
                        
                        # 리스트 아이템 생성
                        list_item = QListWidgetItem()
                        list_item.setIcon(QIcon(thumbnail))
                        
                        # 타임스탬프와 시간 정보
                        timestamp = data.get("timestamp", "")
                        croquis_time = data.get("croquis_time", 0)
                        time_str = f"{croquis_time // 60}:{croquis_time % 60:02d}" if croquis_time > 0 else "N/A"
                        
                        # 날짜 포맷팅
                        if len(timestamp) >= 13:
                            date_str = f"{timestamp[4:6]}/{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}"
                        else:
                            date_str = timestamp
                        
                        list_item.setText(f"{date_str}\\n{time_str}")
                        
                        # 원본 이미지 로드
                        original_bytes = base64.b64decode(data["original"])
                        original_pixmap = QPixmap()
                        original_pixmap.loadFromData(original_bytes)
                        
                        # 데이터를 아이템에 저장
                        croquis_item_data = {
                            "original": original_pixmap,
                            "screenshot": screenshot_pixmap,
                            "timestamp": timestamp,
                            "time": croquis_time,
                            "date": f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]}",
                            "file_path": str(file)  # 파일 경로 추가
                        }
                        list_item.setData(Qt.ItemDataRole.UserRole, croquis_item_data)
                        
                        # 메모가 있으면 툴팁에 표시
                        memo_text = CroquisMemoDialog.get_memo(str(file))
                        if memo_text:
                            list_item.setToolTip(f"📝 {memo_text}")
                        
                        self.croquis_list.addItem(list_item)
                        
                except Exception as e:
                    continue  # 개별 파일 에러는 무시
            
            if found_count == 0:
                no_data_item = QListWidgetItem("이 이미지로 그린 크로키가 없습니다.")
                self.croquis_list.addItem(no_data_item)
                
        except Exception as e:
            error_item = QListWidgetItem(f"에러: {str(e)}")
            self.croquis_list.addItem(error_item)
    
    def show_croquis_large_view(self, item: QListWidgetItem):
        """크로키 목록에서 선택한 크로키를 크게 보기"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        logger.info("크로키 크게 보기 선택")
        croquis_file_path = data.get("file_path")
        dialog = CroquisLargeViewDialog(data, self.lang, croquis_file_path, self)
        dialog.exec()
    
    def show_croquis_context_menu(self, position):
        """크로키 리스트 우클릭 메뉴"""
        item = self.croquis_list.itemAt(position)
        if not item:
            return
        
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        croquis_file_path = data.get("file_path")
        if not croquis_file_path:
            return
        
        menu = QMenu(self)
        memo_action = QAction(tr("add_memo", self.lang), self)
        memo_action.triggered.connect(lambda: self.open_croquis_memo(croquis_file_path))
        menu.addAction(memo_action)
        
        menu.exec(self.croquis_list.mapToGlobal(position))
    
    def open_croquis_memo(self, croquis_file_path: str):
        """크로키 메모 다이얼로그 열기"""
        dialog = CroquisMemoDialog(croquis_file_path, self.lang, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 메모 저장 후 크로키 리스트 새로고침 (툴팁 업데이트)
            current_item = self.croquis_list.currentItem()
            if current_item:
                self.on_image_selected(current_item)
    
    def closeEvent(self, event):
        """창 닫기 이벤트 - 수정사항이 있으면 저장 확인"""
        logger.info("덱 편집창 닫기")
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "저장 확인",
                "현재 파일이 수정되었습니다. 저장하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.save_deck()
                self.cleanup_temp_file()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                self.cleanup_temp_file()
                event.accept()
            else:  # Cancel
                event.ignore()
        else:
            self.cleanup_temp_file()
            event.accept()
    
    def apply_dark_mode(self):
        """다크 모드 적용"""
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QGroupBox {
                    border: 1px solid #555;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QPushButton {
                    background-color: #3a3a3a;
                    border: 1px solid #555;
                    border-radius: 5px;
                    padding: 8px;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
                QListWidget {
                    background-color: #3a3a3a;
                    border: 1px solid #555;
                    color: #ffffff;
                }
                QListWidget::item {
                    color: #ffffff;
                }
                QListWidget::item:selected {
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                }
                QCheckBox {
                    color: #ffffff;
                }
                QMenuBar {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMenuBar::item:selected {
                    background-color: #3a3a3a;
                }
                QMenu {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    border: 1px solid #555;
                }
                QMenu::item:selected {
                    background-color: #3a3a3a;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QGroupBox {
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    padding: 8px;
                    color: #000000;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QListWidget {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    color: #000000;
                }
                QListWidget::item {
                    color: #000000;
                }
                QListWidget::item:selected {
                    color: #000000;
                }
                QLabel {
                    color: #000000;
                }
                QCheckBox {
                    color: #000000;
                }
                QMenuBar {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QMenuBar::item:selected {
                    background-color: #e0e0e0;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                }
                QMenu::item:selected {
                    background-color: #e0e0e0;
                }
            """)


# ============== 히스토리 윈도우 ==============
class HistoryWindow(QDialog):
    """크로키 히스토리 윈도우"""
    
    def __init__(self, lang: str = "ko", parent=None, dark_mode: bool = False):
        super().__init__(parent)
        self.lang = lang
        self.dark_mode = dark_mode
        self.setup_ui()
        self.load_history()
        
    def setup_ui(self):
        self.setWindowTitle(tr("croquis_history", self.lang))
        self.resize(1000, 600)
        
        layout = QVBoxLayout(self)
        
        # 날짜 필터
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("날짜 필터:"))
        
        self.date_filter = QComboBox()
        self.date_filter.addItem("전체", None)
        self.date_filter.currentIndexChanged.connect(self.filter_by_date)
        filter_layout.addWidget(self.date_filter)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # 히스토리 리스트 (덱 편집창과 동일한 스타일)
        self.history_list = QListWidget()
        self.history_list.setIconSize(QSize(300, 150))
        self.history_list.setGridSize(QSize(320, 185))  # 아이콘 + 텍스트 공간
        self.history_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.history_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.history_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.history_list.setWordWrap(True)
        self.history_list.setSpacing(5)
        
        # 다크/라이트 모드에 따른 텍스트 색상 설정
        text_color = "#ffffff" if self.dark_mode else "#000000"
        self.history_list.setStyleSheet(f"""
            QListWidget::item {{
                text-align: center;
                padding: 3px;
                color: {text_color};
            }}
            QListWidget::item:selected {{
                background-color: rgba(0, 120, 212, 0.2);
                color: {text_color};
            }}
            QListWidget::item:hover {{
                background-color: rgba(0, 120, 212, 0.1);
            }}
            QListWidget {{
                outline: none;
            }}
        """)
        self.history_list.itemClicked.connect(self.show_large_view)
        self.history_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self.show_history_context_menu)
        
        layout.addWidget(self.history_list)
        
    def load_history(self):
        """저장된 크로키 페어 불러오기"""
        history_dir = Path(__file__).parent / "croquis_pairs"
        if not history_dir.exists():
            return
        
        self.history_data = []
        dates_set = set()
        
        # 파일 로드 및 복호화
        for file in sorted(history_dir.glob("*.croq"), reverse=True):
            try:
                with open(file, "rb") as f:
                    encrypted = f.read()
                
                key = base64.urlsafe_b64encode(hashlib.sha256(b"croquis_secret_key").digest())
                fernet = Fernet(key)
                decrypted = fernet.decrypt(encrypted)
                data = json.loads(decrypted.decode())
                
                # 날짜 추출
                timestamp = data.get("timestamp", file.stem)
                date_str = timestamp[:8]  # YYYYMMDD
                formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                dates_set.add(formatted_date)
                
                # 원본 및 스크린샷 이미지 생성
                original_bytes = base64.b64decode(data["original"])
                original_pixmap = QPixmap()
                original_pixmap.loadFromData(original_bytes)
                
                screenshot_bytes = base64.b64decode(data["screenshot"])
                screenshot_pixmap = QPixmap()
                screenshot_pixmap.loadFromData(screenshot_bytes)
                
                # 크로키 시간
                croquis_time = data.get("croquis_time", 0)
                
                # 이미지 메타데이터 (신버전만 있음)
                image_metadata = data.get("image_metadata", {})
                
                self.history_data.append({
                    "date": formatted_date,
                    "timestamp": timestamp,
                    "original": original_pixmap,
                    "screenshot": screenshot_pixmap,
                    "time": croquis_time,
                    "file": file,
                    "image_metadata": image_metadata
                })
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        # 날짜 필터 콤보박스 채우기
        for date_str in sorted(dates_set, reverse=True):
            self.date_filter.addItem(date_str, date_str)
        
        self.display_history()
    
    def filter_by_date(self, index):
        """날짜별 필터링"""
        self.display_history()
    
    def display_history(self):
        """히스토리 표시"""
        # 기존 아이템 제거
        self.history_list.clear()
        
        # 필터링된 날짜
        selected_date = self.date_filter.currentData()
        
        for item in self.history_data:
            if selected_date and item["date"] != selected_date:
                continue
            
            # 원본과 크로키를 합친 썸네일 생성 (왼쪽: 크로키, 오른쪽: 원본)
            combined_width = 300
            combined_height = 150
            combined_pixmap = QPixmap(combined_width, combined_height)
            combined_pixmap.fill(Qt.GlobalColor.white)
            
            painter = QPainter(combined_pixmap)
            
            # 크로키 이미지 (왼쪽)
            screenshot_scaled = item["screenshot"].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            screenshot_x = (150 - screenshot_scaled.width()) // 2
            screenshot_y = (150 - screenshot_scaled.height()) // 2
            painter.drawPixmap(screenshot_x, screenshot_y, screenshot_scaled)
            
            # 원본 이미지 (오른쪽)
            original_scaled = item["original"].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            original_x = 150 + (150 - original_scaled.width()) // 2
            original_y = (150 - original_scaled.height()) // 2
            painter.drawPixmap(original_x, original_y, original_scaled)
            
            painter.end()
            
            # QListWidgetItem 생성
            list_item = QListWidgetItem()
            list_item.setIcon(QIcon(combined_pixmap))
            
            # 정보 텍스트
            time_str = f"{item['time'] // 60}:{item['time'] % 60:02d}" if item['time'] > 0 else "N/A"
            text = f"{item['date']} {item['timestamp'][9:11]}:{item['timestamp'][11:13]} | {time_str}"
            list_item.setText(text)
            
            # 데이터 저장 (file_path 포함)
            item_data_with_path = item.copy()
            item_data_with_path["file_path"] = str(item["file"])
            list_item.setData(Qt.ItemDataRole.UserRole, item_data_with_path)
            
            # 메모가 있으면 툴팁에 표시
            memo_text = CroquisMemoDialog.get_memo(str(item["file"]))
            if memo_text:
                list_item.setToolTip(f"📝 {memo_text}")
            
            self.history_list.addItem(list_item)
    
    def show_large_view(self, item: QListWidgetItem):
        """크로키 크게 보기"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        # 파일 경로 가져오기
        croquis_file_path = data.get("file_path")
        dialog = CroquisLargeViewDialog(data, self.lang, croquis_file_path, self)
        dialog.exec()
    
    def show_history_context_menu(self, position):
        """히스토리 리스트 우클릭 메뉴"""
        item = self.history_list.itemAt(position)
        if not item:
            return
        
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        croquis_file_path = data.get("file_path")
        if not croquis_file_path:
            return
        
        menu = QMenu(self)
        memo_action = QAction(tr("add_memo", self.lang), self)
        memo_action.triggered.connect(lambda: self.open_history_memo(croquis_file_path))
        menu.addAction(memo_action)
        
        menu.exec(self.history_list.mapToGlobal(position))
    
    def open_history_memo(self, croquis_file_path: str):
        """히스토리 메모 다이얼로그 열기"""
        dialog = CroquisMemoDialog(croquis_file_path, self.lang, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 메모 저장 후 히스토리 리스트 새로고침
            self.display_history()
    
    def show_croquis_detail(self, item: QListWidgetItem):
        """크로키 상세 보기 (동일 이미지로 그린 다른 크로키들 표시)"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        # 메타데이터가 있는 경우 해당 이미지로 그린 다른 크로키들 찾기
        dialog = CroquisDetailDialog(data, self.history_data, self.lang, self)
        dialog.exec()


# ============== 크로키 크게 보기 다이얼로그 ==============
class CroquisLargeViewDialog(QDialog):
    """크로키를 크게 보는 다이얼로그"""
    
    def __init__(self, croquis_data: dict, lang: str = "ko", croquis_file_path: str = None, parent=None):
        super().__init__(parent)
        self.croquis_data = croquis_data
        self.lang = lang
        self.croquis_file_path = croquis_file_path
        self.setup_ui()
        logger.info("크로키 큰 보기 열기")
    
    def setup_ui(self):
        self.setWindowTitle("크로키 상세 보기")
        self.resize(950, 550)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # 정보 표시 (상단)
        info_text = f"📅 {self.croquis_data['date']} {self.croquis_data['timestamp'][9:11]}:{self.croquis_data['timestamp'][11:13]}"
        time_str = f"{self.croquis_data['time'] // 60}:{self.croquis_data['time'] % 60:02d}" if self.croquis_data['time'] > 0 else "N/A"
        info_text += f"  ⏱️ {time_str}"
        
        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 13px; font-weight: bold; padding: 8px; background-color: rgba(0, 120, 212, 0.1); border-radius: 5px;")
        main_layout.addWidget(info_label)
        
        # 이미지 레이아웃
        images_layout = QHBoxLayout()
        images_layout.setSpacing(15)
        
        # 원본 이미지
        left_container = QVBoxLayout()
        left_container.setSpacing(5)
        
        orig_label = QLabel("원본")
        orig_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        orig_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #0078d4;")
        left_container.addWidget(orig_label)
        
        # 고정 크기 컨테이너 (440x440)
        orig_img_container = QLabel()
        orig_img_container.setFixedSize(440, 440)
        orig_img_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        orig_img_container.setStyleSheet("border: 2px solid #e0e0e0; border-radius: 5px; background-color: white;")
        
        # 이미지 스케일링 (440x440 범위 내에서 비율 유지)
        orig_pixmap = self.croquis_data["original"].scaled(440, 440, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        orig_img_container.setPixmap(orig_pixmap)
        left_container.addWidget(orig_img_container)
        
        images_layout.addLayout(left_container)
        
        # 크로키 이미지
        right_container = QVBoxLayout()
        right_container.setSpacing(5)
        
        shot_label = QLabel("크로키")
        shot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shot_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #0078d4;")
        right_container.addWidget(shot_label)
        
        # 고정 크기 컨테이너 (440x440)
        shot_img_container = QLabel()
        shot_img_container.setFixedSize(440, 440)
        shot_img_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shot_img_container.setStyleSheet("border: 2px solid #e0e0e0; border-radius: 5px; background-color: white;")
        
        # 이미지 스케일링 (440x440 범위 내에서 비율 유지)
        shot_pixmap = self.croquis_data["screenshot"].scaled(440, 440, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        shot_img_container.setPixmap(shot_pixmap)
        right_container.addWidget(shot_img_container)
        
        images_layout.addLayout(right_container)
        
        main_layout.addLayout(images_layout)
        
        # 메모 버튼 추가
        if self.croquis_file_path:
            memo_btn = QPushButton(tr("add_memo", self.lang))
            memo_btn.clicked.connect(self.open_memo_dialog)
            main_layout.addWidget(memo_btn)
    
    def open_memo_dialog(self):
        """메모 다이얼로그 열기"""
        if self.croquis_file_path:
            dialog = CroquisMemoDialog(self.croquis_file_path, self.lang, self)
            dialog.exec()


# ============== 크로키 메모 다이얼로그 ==============
class CroquisMemoDialog(QDialog):
    """크로키 메모 다이얼로그"""
    
    def __init__(self, croquis_file_path: str, lang: str = "ko", parent=None):
        super().__init__(parent)
        self.croquis_file_path = croquis_file_path
        self.memo_file_path = croquis_file_path.replace(".croq", "_memo.txt")
        self.lang = lang
        self.setup_ui()
        self.load_memo()
        logger.info(f"크로키 메모 다이얼로그 열기: {os.path.basename(croquis_file_path)}")
    
    def setup_ui(self):
        self.setWindowTitle(tr("memo", self.lang))
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 메모 입력 영역
        from PyQt6.QtWidgets import QTextEdit
        self.memo_edit = QTextEdit()
        self.memo_edit.setPlaceholderText("여기에 메모를 입력하세요...")
        layout.addWidget(self.memo_edit)
        
        # 닫기 버튼
        close_btn = QPushButton(tr("close", self.lang))
        close_btn.clicked.connect(self.save_and_close)
        layout.addWidget(close_btn)
    
    def load_memo(self):
        """메모 불러오기"""
        if os.path.exists(self.memo_file_path):
            try:
                with open(self.memo_file_path, 'r', encoding='utf-8') as f:
                    memo_text = f.read()
                    self.memo_edit.setPlainText(memo_text)
            except Exception as e:
                logger.error(f"메모 불러오기 실패: {e}")
    
    def save_and_close(self):
        """메모 저장 후 닫기"""
        try:
            memo_text = self.memo_edit.toPlainText()
            with open(self.memo_file_path, 'w', encoding='utf-8') as f:
                f.write(memo_text)
            logger.info(f"크로키 메모 저장: {os.path.basename(self.croquis_file_path)}")
            self.accept()
        except Exception as e:
            logger.error(f"메모 저장 실패: {e}")
            QMessageBox.warning(self, "오류", f"메모 저장 중 오류가 발생했습니다:\n{str(e)}")
    
    @staticmethod
    def get_memo(croquis_file_path: str) -> str:
        """메모 텍스트 가져오기 (툴팁용)"""
        memo_file_path = croquis_file_path.replace(".croq", "_memo.txt")
        if os.path.exists(memo_file_path):
            try:
                with open(memo_file_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except:
                return ""
        return ""


# ============== 크로키 상세 보기 다이얼로그 ==============
class CroquisDetailDialog(QDialog):
    """특정 이미지로 그린 모든 크로키 목록을 보여주는 다이얼로그"""
    
    def __init__(self, selected_data: dict, all_history: list, lang: str = "ko", parent=None):
        super().__init__(parent)
        self.selected_data = selected_data
        self.all_history = all_history
        self.lang = lang
        self.setup_ui()
        self.load_related_croquis()
        
    def setup_ui(self):
        self.setWindowTitle("크로키 상세 보기")
        self.resize(1200, 700)
        
        layout = QHBoxLayout(self)
        
        # 왼쪽: 선택한 크로키
        left_layout = QVBoxLayout()
        left_label = QLabel("선택한 크로키")
        left_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        left_layout.addWidget(left_label)
        
        # 선택한 크로키 표시
        self.selected_widget = QWidget()
        selected_layout = QVBoxLayout(self.selected_widget)
        
        # 원본과 크로키 이미지
        images_layout = QHBoxLayout()
        
        # 원본 이미지
        orig_container = QVBoxLayout()
        orig_label = QLabel("원본")
        orig_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        orig_container.addWidget(orig_label)
        
        orig_img_label = QLabel()
        orig_pixmap = self.selected_data["original"].scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        orig_img_label.setPixmap(orig_pixmap)
        orig_img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        orig_container.addWidget(orig_img_label)
        images_layout.addLayout(orig_container)
        
        # 크로키 이미지
        shot_container = QVBoxLayout()
        shot_label = QLabel("크로키")
        shot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shot_container.addWidget(shot_label)
        
        shot_img_label = QLabel()
        shot_pixmap = self.selected_data["screenshot"].scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        shot_img_label.setPixmap(shot_pixmap)
        shot_img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shot_container.addWidget(shot_img_label)
        images_layout.addLayout(shot_container)
        
        selected_layout.addLayout(images_layout)
        
        # 선택한 크로키 정보
        info_text = f"날짜: {self.selected_data['date']} {self.selected_data['timestamp'][9:11]}:{self.selected_data['timestamp'][11:13]}\n"
        time_str = f"{self.selected_data['time'] // 60}:{self.selected_data['time'] % 60:02d}" if self.selected_data['time'] > 0 else "N/A"
        info_text += f"크로키 시간: {time_str}"
        
        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 12px; margin-top: 10px;")
        selected_layout.addWidget(info_label)
        
        left_layout.addWidget(self.selected_widget)
        layout.addLayout(left_layout, 1)
        
        # 오른쪽: 동일 이미지로 그린 다른 크로키들
        right_layout = QVBoxLayout()
        right_label = QLabel("이 이미지로 그린 다른 크로키들")
        right_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        right_layout.addWidget(right_label)
        
        self.related_list = QListWidget()
        self.related_list.setIconSize(QSize(200, 100))
        self.related_list.setGridSize(QSize(220, 135))
        self.related_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.related_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.related_list.setSpacing(5)
        self.related_list.setStyleSheet("""
            QListWidget::item {
                text-align: center;
                padding: 3px;
            }
            QListWidget::item:selected {
                background-color: rgba(0, 120, 212, 0.2);
            }
        """)
        right_layout.addWidget(self.related_list)
        
        layout.addLayout(right_layout, 1)
    
    def load_related_croquis(self):
        """동일 이미지로 그린 다른 크로키들 로드"""
        self.related_list.clear()
        
        # 선택한 크로키의 이미지 메타데이터가 없는 경우 (구버전 파일)
        if "image_metadata" not in self.selected_data:
            info_item = QListWidgetItem("구버전 파일로 관련 크로키를 찾을 수 없습니다.")
            self.related_list.addItem(info_item)
            return
        
        selected_metadata = self.selected_data.get("image_metadata", {})
        selected_filename = selected_metadata.get("filename", "")
        
        # 동일한 파일명을 가진 크로키들 찾기
        related_count = 0
        for item in self.all_history:
            # 자기 자신은 제외
            if item["timestamp"] == self.selected_data["timestamp"]:
                continue
            
            # 메타데이터 확인
            item_metadata = item.get("image_metadata", {})
            item_filename = item_metadata.get("filename", "")
            
            if item_filename == selected_filename and selected_filename:
                related_count += 1
                
                # 크로키 이미지만 표시
                screenshot_scaled = item["screenshot"].scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                
                list_item = QListWidgetItem()
                list_item.setIcon(QIcon(screenshot_scaled))
                
                time_str = f"{item['time'] // 60}:{item['time'] % 60:02d}" if item['time'] > 0 else "N/A"
                text = f"{item['date']} {item['timestamp'][9:11]}:{item['timestamp'][11:13]}\n{time_str}"
                list_item.setText(text)
                
                self.related_list.addItem(list_item)
        
        if related_count == 0:
            info_item = QListWidgetItem("이 이미지로 그린 다른 크로키가 없습니다.")
            self.related_list.addItem(info_item)


# ============== 알람 윈도우 ==============
class AlarmWindow(QDialog):
    """크로키 알람 윈도우"""
    
    def __init__(self, lang: str = "ko", parent=None):
        super().__init__(parent)
        self.lang = lang
        self.alarms = []
        self.timers = []
        self.load_alarms()
        self.setup_ui()
        self.start_alarm_timers()
        
    def setup_ui(self):
        self.setWindowTitle(tr("croquis_alarm", self.lang))
        self.resize(690, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 15, 15, 15)
        
        # 알람 리스트
        list_label = QLabel("설정된 알람 목록:")
        layout.addWidget(list_label)
        
        self.alarm_list = QListWidget()
        self.alarm_list.itemDoubleClicked.connect(self.edit_alarm)
        layout.addWidget(self.alarm_list)
        
        # 버튼
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("알람 추가")
        add_btn.clicked.connect(self.add_alarm)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("알람 수정")
        edit_btn.clicked.connect(self.edit_alarm)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("알람 삭제")
        delete_btn.clicked.connect(self.delete_alarm)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.refresh_alarm_list()
        
    def add_alarm(self):
        """알람 추가"""
        dialog = AlarmEditDialog(self.lang, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            alarm_data = dialog.get_alarm_data()
            self.alarms.append(alarm_data)
            self.save_alarms()
            self.refresh_alarm_list()
            self.start_alarm_timers()
            
    def edit_alarm(self):
        """알람 수정"""
        current_item = self.alarm_list.currentItem()
        if not current_item:
            return
        
        index = self.alarm_list.row(current_item)
        alarm_data = self.alarms[index]
        
        dialog = AlarmEditDialog(self.lang, self, alarm_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.alarms[index] = dialog.get_alarm_data()
            self.save_alarms()
            self.refresh_alarm_list()
            self.start_alarm_timers()
            
    def delete_alarm(self):
        """알람 삭제"""
        current_item = self.alarm_list.currentItem()
        if not current_item:
            return
        
        index = self.alarm_list.row(current_item)
        del self.alarms[index]
        self.save_alarms()
        self.refresh_alarm_list()
        self.start_alarm_timers()
        
    def refresh_alarm_list(self):
        """알람 리스트 새로고침"""
        self.alarm_list.clear()
        for alarm in self.alarms:
            if alarm.get("type") == "weekday":
                days = ", ".join([["월", "화", "수", "목", "금", "토", "일"][d] for d in alarm["weekdays"]])
                text = f"{alarm['title']} - 매주 {days} {alarm['time']}"
            else:
                text = f"{alarm['title']} - {alarm['date']} {alarm['time']}"
            
            item = QListWidgetItem(text)
            self.alarm_list.addItem(item)
    
    def save_alarms(self):
        """알람 저장"""
        dat_dir = Path(__file__).parent / "dat"
        dat_dir.mkdir(exist_ok=True)
        alarms_path = dat_dir / "alarms.dat"
        encrypted = encrypt_data({"alarms": self.alarms})
        with open(alarms_path, "wb") as f:
            f.write(encrypted)
    
    def load_alarms(self):
        """알람 로드"""
        dat_dir = Path(__file__).parent / "dat"
        alarms_path = dat_dir / "alarms.dat"
        if alarms_path.exists():
            try:
                with open(alarms_path, "rb") as f:
                    encrypted = f.read()
                decrypted = decrypt_data(encrypted)
                self.alarms = decrypted.get("alarms", [])
            except Exception:
                self.alarms = []
        else:
            self.alarms = []
    
    def start_alarm_timers(self):
        """알람 타이머 시작"""
        # 기존 타이머 중지
        for timer in self.timers:
            timer.stop()
        self.timers.clear()
        
        # 새 타이머 시작
        for alarm in self.alarms:
            timer = QTimer()
            timer.timeout.connect(lambda a=alarm: self.check_alarm(a))
            timer.start(30000)  # 30초마다 체크
            self.timers.append(timer)
            
            # 즉시 한 번 체크
            self.check_alarm(alarm)
    
    def check_alarm(self, alarm):
        """알람 체크"""
        now = QDateTime.currentDateTime()
        current_time = now.time().toString("HH:mm")
        current_date = now.date().toString("yyyy-MM-dd")
        current_weekday = now.date().dayOfWeek() - 1  # 0=월요일
        
        should_alarm = False
        
        if alarm.get("type") == "weekday":
            if current_weekday in alarm["weekdays"] and current_time == alarm["time"]:
                should_alarm = True
        else:
            if current_date == alarm["date"] and current_time == alarm["time"]:
                should_alarm = True
        
        if should_alarm:
            self.show_toast(alarm["title"], alarm.get("message", ""))
    
    def show_toast(self, title: str, message: str):
        """토스트 알람 표시"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


class AlarmEditDialog(QDialog):
    """알람 편집 다이얼로그"""
    
    def __init__(self, lang: str, parent=None, alarm_data=None):
        super().__init__(parent)
        self.lang = lang
        self.alarm_data = alarm_data or {}
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("알람 설정")
        self.resize(490, 400)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 15, 15, 15)
        
        # 제목
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("제목:"))
        self.title_input = QLineEdit()
        self.title_input.setText(self.alarm_data.get("title", ""))
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)
        
        # 메시지
        layout.addWidget(QLabel("메시지:"))
        from PyQt6.QtWidgets import QTextEdit
        self.message_input = QTextEdit()
        self.message_input.setPlainText(self.alarm_data.get("message", ""))
        self.message_input.setMinimumHeight(150)
        # 커서를 최상단으로
        cursor = self.message_input.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.message_input.setTextCursor(cursor)
        layout.addWidget(self.message_input)
        
        # 시간
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("시간:"))
        self.time_edit = QTimeEdit()
        if self.alarm_data.get("time"):
            self.time_edit.setTime(QTime.fromString(self.alarm_data["time"], "HH:mm"))
        else:
            self.time_edit.setTime(QTime.currentTime())
        time_layout.addWidget(self.time_edit)
        layout.addLayout(time_layout)
        
        # 타입 선택
        self.type_combo = QComboBox()
        self.type_combo.addItem("요일 반복", "weekday")
        self.type_combo.addItem("특정 날짜", "date")
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        layout.addWidget(self.type_combo)
        
        # 요일 선택
        self.weekday_group = QGroupBox("반복 요일 선택")
        self.weekday_group.setMaximumHeight(80)
        weekday_layout = QHBoxLayout(self.weekday_group)
        weekday_layout.setContentsMargins(10, 5, 10, 5)
        self.weekday_checks = []
        for day in ["월", "화", "수", "목", "금", "토", "일"]:
            check = QCheckBox(day)
            self.weekday_checks.append(check)
            weekday_layout.addWidget(check)
        layout.addWidget(self.weekday_group)
        
        # 날짜 선택
        self.date_group = QGroupBox("날짜 선택")
        self.date_group.setMaximumHeight(80)
        date_layout = QVBoxLayout(self.date_group)
        date_layout.setContentsMargins(10, 5, 10, 5)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if self.alarm_data.get("date"):
            self.date_edit.setDate(QDate.fromString(self.alarm_data["date"], "yyyy-MM-dd"))
        else:
            self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_edit)
        layout.addWidget(self.date_group)
        
        # 기존 데이터 로드
        if self.alarm_data.get("type") == "weekday":
            self.type_combo.setCurrentIndex(0)
            for i, checked in enumerate(self.alarm_data.get("weekdays", [])):
                if i < len(self.weekday_checks):
                    self.weekday_checks[checked].setChecked(True)
        else:
            self.type_combo.setCurrentIndex(1)
        
        self.on_type_changed()
        
        # 버튼
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def on_type_changed(self):
        """타입 변경 시"""
        alarm_type = self.type_combo.currentData()
        self.weekday_group.setVisible(alarm_type == "weekday")
        self.date_group.setVisible(alarm_type == "date")
    
    def get_alarm_data(self):
        """알람 데이터 반환"""
        alarm_type = self.type_combo.currentData()
        data = {
            "title": self.title_input.text(),
            "message": self.message_input.toPlainText(),  # QTextEdit 사용
            "time": self.time_edit.time().toString("HH:mm"),
            "type": alarm_type
        }
        
        if alarm_type == "weekday":
            data["weekdays"] = [i for i, check in enumerate(self.weekday_checks) if check.isChecked()]
        else:
            data["date"] = self.date_edit.date().toString("yyyy-MM-dd")
        
        return data


# ============== 메인 윈도우 ==============
class MainWindow(QMainWindow):
    """크로키 연습 앱 메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.settings = CroquisSettings()
        self.load_settings()
        self.image_files: List[str] = []
        self.setup_ui()
        self.apply_language()
        self.apply_dark_mode()
        
    def setup_ui(self):
        self.setWindowTitle(tr("app_title", self.settings.language))
        self.setFixedSize(750, 750)
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 20, 10, 10)
        
        # 히트맵 영역
        heatmap_group = QGroupBox()
        heatmap_group.setMinimumHeight(150)  # 툴팁이 잘리지 않도록 높이 증가
        self.heatmap_group = heatmap_group
        heatmap_layout = QVBoxLayout(heatmap_group)
        heatmap_layout.setContentsMargins(10, 20, 10, 5)  # 상하 여백 최소화
        heatmap_layout.setSpacing(0)
        
        # 히트맵을 오른쪽 정렬로 표시
        heatmap_container = QHBoxLayout()
        heatmap_container.setContentsMargins(0, 0, 0, 0)
        heatmap_container.setSpacing(0)
        heatmap_container.addStretch(1)
        self.heatmap_widget = HeatmapWidget(lang=self.settings.language)
        self.heatmap_widget.setMinimumSize(600, 120)
        self.heatmap_widget.setContentsMargins(0, 0, 0, 0)
        heatmap_container.addWidget(self.heatmap_widget)
        heatmap_container.addStretch(1)
        heatmap_layout.addLayout(heatmap_container)
        
        main_layout.addWidget(heatmap_group)
        
        # 설정 영역 (2열 레이아웃)
        settings_layout = QHBoxLayout()
        
        # 왼쪽 열
        left_column = QVBoxLayout()
        
        # 기본 설정
        basic_group = QGroupBox()
        self.basic_group = basic_group
        basic_layout = QVBoxLayout(basic_group)
        
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel()
        self.folder_value = QLineEdit()
        self.folder_value.setReadOnly(True)
        self.folder_value.setPlaceholderText("deck")
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_value, 1)
        basic_layout.addLayout(folder_layout)
        
        self.select_folder_btn = QPushButton()
        self.select_folder_btn.clicked.connect(self.select_folder)
        basic_layout.addWidget(self.select_folder_btn)
        
        left_column.addWidget(basic_group)
        
        # 이미지 설정
        image_group = QGroupBox()
        self.image_group = image_group
        image_layout = QVBoxLayout(image_group)
        image_layout.setSpacing(8)  # 간격 늘림
        
        width_layout = QHBoxLayout()
        self.width_label = QLabel()
        self.width_input = QSpinBox()
        self.width_input.setRange(100, 3000)
        self.width_input.setValue(self.settings.image_width)
        self.width_input.setMinimumWidth(80)
        self.width_input.setMinimumHeight(28)
        self.width_input.valueChanged.connect(self.on_width_changed)
        width_layout.addWidget(self.width_label)
        width_layout.addWidget(self.width_input)
        image_layout.addLayout(width_layout)
        
        height_layout = QHBoxLayout()
        self.height_label = QLabel()
        self.height_input = QSpinBox()
        self.height_input.setRange(100, 3000)
        self.height_input.setValue(self.settings.image_height)
        self.height_input.setMinimumWidth(80)
        self.height_input.setMinimumHeight(28)
        self.height_input.valueChanged.connect(self.on_height_changed)
        height_layout.addWidget(self.height_label)
        height_layout.addWidget(self.height_input)
        image_layout.addLayout(height_layout)
        
        self.random_check = QCheckBox()
        self.random_check.setChecked(self.settings.random_order)
        self.random_check.setMinimumHeight(25)
        self.random_check.stateChanged.connect(self.on_random_changed)
        image_layout.addWidget(self.random_check)
        
        self.grayscale_check = QCheckBox()
        self.grayscale_check.setChecked(self.settings.grayscale)
        self.grayscale_check.setMinimumHeight(25)
        self.grayscale_check.stateChanged.connect(self.on_grayscale_changed)
        image_layout.addWidget(self.grayscale_check)
        
        self.flip_check = QCheckBox()
        self.flip_check.setChecked(self.settings.flip_horizontal)
        self.flip_check.setMinimumHeight(25)
        self.flip_check.stateChanged.connect(self.on_flip_changed)
        image_layout.addWidget(self.flip_check)
        
        left_column.addWidget(image_group)
        left_column.addStretch()
        
        settings_layout.addLayout(left_column)
        
        # 오른쪽 열
        right_column = QVBoxLayout()
        
        # 타이머 설정
        timer_group = QGroupBox()
        self.timer_group = timer_group
        timer_layout = QVBoxLayout(timer_group)
        
        pos_layout = QHBoxLayout()
        self.timer_pos_label = QLabel()
        self.timer_pos_combo = QComboBox()
        self.timer_pos_combo.addItems([
            "bottom_right", "bottom_center", "bottom_left",
            "top_right", "top_center", "top_left"
        ])
        self.timer_pos_combo.setCurrentText(self.settings.timer_position)
        self.timer_pos_combo.currentTextChanged.connect(self.on_timer_pos_changed)
        pos_layout.addWidget(self.timer_pos_label)
        pos_layout.addWidget(self.timer_pos_combo, 1)
        timer_layout.addLayout(pos_layout)
        
        font_layout = QHBoxLayout()
        self.timer_font_label = QLabel()
        self.timer_font_combo = QComboBox()
        self.timer_font_combo.currentTextChanged.connect(self.on_timer_font_changed)
        font_layout.addWidget(self.timer_font_label)
        font_layout.addWidget(self.timer_font_combo, 1)
        timer_layout.addLayout(font_layout)
        
        time_layout = QHBoxLayout()
        self.time_label = QLabel()
        self.time_input = QSpinBox()
        self.time_input.setRange(1, 3600)
        self.time_input.setValue(self.settings.time_seconds)
        self.time_input.setMinimumWidth(80)
        self.time_input.setMinimumHeight(28)
        self.time_input.valueChanged.connect(self.on_time_changed)
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_input)
        timer_layout.addLayout(time_layout)
        
        # 학습 모드
        self.study_mode_check = QCheckBox()
        self.study_mode_check.setChecked(self.settings.study_mode)
        self.study_mode_check.setMinimumHeight(25)
        self.study_mode_check.stateChanged.connect(self.on_study_mode_changed)
        timer_layout.addWidget(self.study_mode_check)
        
        right_column.addWidget(timer_group)
        
        # 기타 설정
        other_group = QGroupBox()
        self.other_group = other_group
        other_layout = QVBoxLayout(other_group)
        
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["한국어", "English"])
        self.lang_combo.setCurrentText("한국어" if self.settings.language == "ko" else "English")
        self.lang_combo.currentTextChanged.connect(self.on_language_changed)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo, 1)
        other_layout.addLayout(lang_layout)
        
        self.dark_mode_check = QCheckBox()
        self.dark_mode_check.setChecked(self.settings.dark_mode)
        self.dark_mode_check.setMinimumHeight(25)
        self.dark_mode_check.stateChanged.connect(self.on_dark_mode_changed)
        other_layout.addWidget(self.dark_mode_check)
        
        right_column.addWidget(other_group)
        right_column.addStretch()
        
        settings_layout.addLayout(right_column)
        main_layout.addLayout(settings_layout)
        
        # 버튼 영역
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        self.start_btn = QPushButton()
        self.start_btn.setEnabled(False)
        self.start_btn.setMinimumHeight(40)
        self.start_btn.clicked.connect(self.start_croquis)
        button_layout.addWidget(self.start_btn)
        
        self.edit_deck_btn = QPushButton()
        self.edit_deck_btn.setMinimumHeight(40)
        self.edit_deck_btn.clicked.connect(self.open_deck_editor)
        button_layout.addWidget(self.edit_deck_btn)
        
        self.history_btn = QPushButton()
        self.history_btn.setMinimumHeight(40)
        self.history_btn.clicked.connect(self.open_history)
        button_layout.addWidget(self.history_btn)
        
        self.alarm_btn = QPushButton()
        self.alarm_btn.setMinimumHeight(40)
        self.alarm_btn.clicked.connect(self.open_alarm)
        button_layout.addWidget(self.alarm_btn)
        
        main_layout.addLayout(button_layout)
        
        # 학습 모드에 따라 시간 입력 활성화/비활성화
        self.time_input.setEnabled(not self.settings.study_mode)
        
    def apply_language(self):
        """언어 적용"""
        lang = self.settings.language
        
        self.setWindowTitle(tr("app_title", lang))
        
        # 히트맵
        count = self.heatmap_widget.total_count
        self.heatmap_group.setTitle(f"{tr('heatmap_title', lang)} - {tr('croquis_count', lang)}: {count}회")
        self.heatmap_widget.lang = lang
        
        # 기본 설정
        self.basic_group.setTitle(tr("basic_settings", lang))
        self.folder_label.setText(tr("image_folder", lang))
        self.select_folder_btn.setText(tr("select_folder", lang))
        
        # 이미지 설정
        self.image_group.setTitle(tr("image_settings", lang))
        self.width_label.setText(tr("image_width", lang))
        self.height_label.setText(tr("image_height", lang))
        self.random_check.setText(tr("random_order", lang))
        self.grayscale_check.setText(tr("grayscale", lang))
        self.flip_check.setText(tr("flip_horizontal", lang))
        
        # 타이머 설정
        self.timer_group.setTitle(tr("timer_settings", lang))
        self.timer_pos_label.setText(tr("timer_position", lang))
        self.timer_font_label.setText(tr("timer_font_size", lang))
        self.time_label.setText(tr("time_setting", lang))
        self.study_mode_check.setText("학습 모드" if lang == "ko" else "Study Mode")
        
        # 폰트 크기 콤보박스 갱신
        self.timer_font_combo.clear()
        self.timer_font_combo.addItems([
            tr("large", lang),
            tr("medium", lang),
            tr("small", lang)
        ])
        font_map = {"large": 0, "medium": 1, "small": 2}
        self.timer_font_combo.setCurrentIndex(font_map.get(self.settings.timer_font_size, 0))
        
        # 기타 설정
        self.other_group.setTitle(tr("other_settings", lang))
        self.lang_label.setText(tr("language", lang))
        self.dark_mode_check.setText(tr("dark_mode", lang))
        
        # 버튼
        self.start_btn.setText(tr("start_croquis", lang))
        self.edit_deck_btn.setText(tr("edit_deck", lang))
        self.history_btn.setText(tr("croquis_history", lang))
        self.alarm_btn.setText(tr("croquis_alarm", lang))
        
    def apply_dark_mode(self):
        """다크 모드 적용"""
        if self.settings.dark_mode:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QGroupBox {
                    border: 1px solid #555;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QPushButton {
                    background-color: #3a3a3a;
                    border: 1px solid #555;
                    border-radius: 5px;
                    padding: 8px;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
                QPushButton:disabled {
                    background-color: #2a2a2a;
                    color: #666;
                }
                QLineEdit, QSpinBox, QComboBox {
                    background-color: #3a3a3a;
                    border: 1px solid #555;
                    border-radius: 4px;
                    padding: 5px;
                    color: #ffffff;
                }
                QCheckBox {
                    color: #ffffff;
                }
                QCheckBox::indicator {
                    background-color: #252525;
                }
                QCheckBox::indicator:checked {
                    background-color: #0078d4;
                    border-color: #0078d4;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QGroupBox {
                    border: 1px solid #555;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QPushButton {
                    background-color: #eeeeee;
                    border: 1px solid #555;
                    border-radius: 5px;
                    padding: 8px;
                    color: #000000;
                }
                QPushButton:hover {
                    background-color: #eeeeee;
                }
                QPushButton:disabled {
                    background-color: #dddddd;
                    color: #666;
                }
                QLineEdit, QSpinBox, QComboBox {
                    background-color: #dddddd;
                    border: 1px solid #555;
                    border-radius: 4px;
                    padding: 5px;
                    color: #000000;
                }
                QCheckBox {
                    color: #000000;
                }
                QCheckBox::indicator {
                    background-color: #dddddd;
                }
                QCheckBox::indicator:checked {
                    background-color: #0078d4;
                    border-color: #0078d4;
                }
            """)
            
    def select_folder(self):
        """크로키 덱 파일 선택"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "크로키 덱 파일 선택",
            "",
            "크로키 덱 파일 (*.crdk)"
        )
        if file_path:
            logger.info(f"덱 선택: {os.path.basename(file_path)}")
            self.load_deck_file(file_path)
            
    def load_deck_file(self, file_path: str):
        """크로키 덱 파일에서 이미지 로드"""
        try:
            with open(file_path, "rb") as f:
                encrypted = f.read()
            
            data = decrypt_data(encrypted)
            self.image_files = []
            
            images_data = data.get("images", [])
            
            # 새로운 형식 (dict) 또는 구버전 형식 (str) 처리
            for img in images_data:
                if isinstance(img, dict):
                    # 새로운 형식: dict에서 image_data 추출
                    try:
                        image_data_b64 = img.get("image_data", "")
                        if image_data_b64:
                            # base64 디코딩하여 메모리 이미지로 저장
                            image_bytes = base64.b64decode(image_data_b64)
                            # 임시로 dict 자체를 저장 (ImageViewerWindow에서 처리)
                            self.image_files.append(img)
                    except Exception as e:
                        print(f"이미지 로드 실패: {e}")
                        continue
                elif isinstance(img, str):
                    # 구버전 형식: 파일 경로
                    if os.path.exists(img):
                        self.image_files.append(img)
            
            if self.image_files:
                self.settings.image_folder = file_path
                self.folder_value.setText(f"{os.path.basename(file_path)} ({len(self.image_files)}개 이미지)")
                self.start_btn.setEnabled(True)
                self.save_settings()
            else:
                QMessageBox.warning(self, "경고", "덱 파일에 유효한 이미지가 없습니다.")
        except Exception as e:
            QMessageBox.warning(self, "오류", f"덱 파일을 불러오는 중 오류가 발생했습니다: {str(e)}")
            
    def load_images_from_folder(self, folder: str):
        """폴더에서 이미지 로드 (구버전 호환)"""
        if folder.endswith('.crdk'):
            self.load_deck_file(folder)
            return
            
        self.image_files.clear()
        extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(extensions):
                    self.image_files.append(os.path.join(root, file))
        
        self.start_btn.setEnabled(len(self.image_files) > 0)
        
    def on_width_changed(self, value: int):
        self.settings.image_width = value
        logger.info(f"이미지 너비 변경: {value}")
        self.save_settings()
        
    def on_height_changed(self, value: int):
        self.settings.image_height = value
        logger.info(f"이미지 높이 변경: {value}")
        self.save_settings()
        
    def on_random_changed(self, state: int):
        self.settings.random_order = state == Qt.CheckState.Checked.value
        logger.info(f"랜덤 모드: {self.settings.random_order}")
        self.save_settings()
        
    def on_grayscale_changed(self, state: int):
        self.settings.grayscale = state == Qt.CheckState.Checked.value
        logger.info(f"흑백 모드: {self.settings.grayscale}")
        self.save_settings()
        
    def on_flip_changed(self, state: int):
        self.settings.flip_horizontal = state == Qt.CheckState.Checked.value
        logger.info(f"좌우 반전: {self.settings.flip_horizontal}")
        self.save_settings()
        
    def on_timer_pos_changed(self, text: str):
        self.settings.timer_position = text
        logger.info(f"타이머 위치: {text}")
        self.save_settings()
        
    def on_timer_font_changed(self, text: str):
        font_map = {
            tr("large", self.settings.language): "large",
            tr("medium", self.settings.language): "medium",
            tr("small", self.settings.language): "small",
            "크게": "large", "보통": "medium", "작게": "small",
            "Large": "large", "Medium": "medium", "Small": "small"
        }
        self.settings.timer_font_size = font_map.get(text, "large")
        logger.info(f"타이머 폰트 크기: {self.settings.timer_font_size}")
        self.save_settings()
        
    def on_time_changed(self, value: int):
        self.settings.time_seconds = value
        logger.info(f"타이머 시간 변경: {value}초")
        self.save_settings()
        
    def on_language_changed(self, text: str):
        self.settings.language = "ko" if text == "한국어" else "en"
        logger.info(f"언어 변경: {self.settings.language}")
        self.apply_language()
        self.save_settings()
        
    def on_dark_mode_changed(self, state: int):
        self.settings.dark_mode = state == Qt.CheckState.Checked.value
        logger.info(f"다크 모드: {self.settings.dark_mode}")
        self.apply_dark_mode()
        self.save_settings()
        
    def on_study_mode_changed(self, state: int):
        """학습 모드 변경"""
        self.settings.study_mode = state == Qt.CheckState.Checked.value
        self.time_input.setEnabled(not self.settings.study_mode)
        self.save_settings()
        
    def start_croquis(self):
        """크로키 시작"""
        if not self.image_files:
            return
        
        logger.info(f"크로키 시작 - 이미지 {len(self.image_files)}개")
        self.viewer = ImageViewerWindow(
            self.settings,
            self.image_files.copy(),
            self.settings.language
        )
        self.viewer.croquis_completed.connect(self.on_croquis_completed)
        self.viewer.croquis_saved.connect(self.on_croquis_saved)
        self.viewer.show()
        
    def on_croquis_completed(self):
        """크로키 완료 시"""
        self.heatmap_widget.add_croquis(1)
        count = self.heatmap_widget.total_count
        self.heatmap_group.setTitle(
            f"{tr('heatmap_title', self.settings.language)} - "
            f"{tr('croquis_count', self.settings.language)}: {count}회"
        )
        
    def on_croquis_saved(self, original: QPixmap, screenshot: QPixmap, croquis_time: int, image_filename: str, image_metadata: dict):
        """크로키 저장 시"""
        # 암호화된 파일로 저장
        pairs_dir = Path(__file__).parent / "croquis_pairs"
        pairs_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # QImage를 통해 바이트로 변환
        import tempfile
        import time
        
        # 임시 파일 생성
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_orig:
            orig_path = tmp_orig.name
        
        original.save(orig_path, "PNG")
        time.sleep(0.1)  # 파일 시스템 동기화 대기
        with open(orig_path, "rb") as f:
            orig_bytes = f.read()
        time.sleep(0.1)
        try:
            os.unlink(orig_path)
        except PermissionError:
            pass  # Windows에서 가끔 발생하는 문제 무시
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_shot:
            shot_path = tmp_shot.name
        
        screenshot.save(shot_path, "PNG")
        time.sleep(0.1)
        with open(shot_path, "rb") as f:
            shot_bytes = f.read()
        time.sleep(0.1)
        try:
            os.unlink(shot_path)
        except PermissionError:
            pass
        
        # 간단한 암호화 (Fernet 사용)
        key = base64.urlsafe_b64encode(hashlib.sha256(b"croquis_secret_key").digest())
        fernet = Fernet(key)
        
        data = {
            "original": base64.b64encode(orig_bytes).decode(),
            "screenshot": base64.b64encode(shot_bytes).decode(),
            "timestamp": timestamp,
            "croquis_time": croquis_time,
            "image_metadata": image_metadata
        }
        
        encrypted = fernet.encrypt(json.dumps(data).encode())
        
        # 파일명에 원본 이미지 이름 포함
        filename = f"{timestamp}_{image_filename}.croq"
        with open(pairs_dir / filename, "wb") as f:
            f.write(encrypted)
            
        self.heatmap_widget.add_croquis(1)
        
    def open_deck_editor(self):
        """덱 편집기 열기"""
        logger.info("덱 편집창 열기")
        self.deck_editor = DeckEditorWindow(self.settings.language, self.settings.dark_mode)
        self.deck_editor.show()
        
    def open_history(self):
        """히스토리 열기"""
        logger.info("크로키 히스토리 열기")
        dialog = HistoryWindow(self.settings.language, self, self.settings.dark_mode)
        dialog.exec()
        logger.info("크로키 히스토리 닫기")
        
    def open_alarm(self):
        """알람 설정 열기"""
        logger.info("알람 설정창 열기")
        dialog = AlarmWindow(self.settings.language, self)
        dialog.exec()
        logger.info("알람 설정창 닫기")
        
    def load_settings(self):
        """설정 로드"""
        dat_dir = Path(__file__).parent / "dat"
        dat_dir.mkdir(exist_ok=True)
        settings_path = dat_dir / "settings.dat"
        if settings_path.exists():
            try:
                with open(settings_path, "rb") as f:
                    encrypted = f.read()
                decrypted = decrypt_data(encrypted)
                self.settings = CroquisSettings(**decrypted)
            except Exception:
                self.settings = CroquisSettings()
                self.save_settings()  # 오류 시 기본 설정으로 저장
        else:
            # 설정 파일이 없으면 기본 설정 생성
            self.settings = CroquisSettings()
            self.save_settings()
                
    def save_settings(self):
        """설정 저장"""
        dat_dir = Path(__file__).parent / "dat"
        dat_dir.mkdir(exist_ok=True)
        settings_path = dat_dir / "settings.dat"
        encrypted = encrypt_data(asdict(self.settings))
        with open(settings_path, "wb") as f:
            f.write(encrypted)
            
    def closeEvent(self, event):
        logger.info("프로그램 종료")
        self.save_settings()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
