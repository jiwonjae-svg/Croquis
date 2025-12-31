"""
리소스 로더 모듈
resources.dat에서 이미지 리소스를 로드하거나, 
파일이 없거나 손상된 경우 embedded_resources.py에서 로드
"""

import os
import json
import base64
import hashlib
import logging
from pathlib import Path
from cryptography.fernet import Fernet
from PyQt6.QtGui import QPixmap

# 로거
logger = logging.getLogger('Croquis')

# 로깅 메시지
RESOURCE_LOG_MESSAGES = {
    "loaded_from_dat": "Resources loaded from resources.dat: {} items",
    "failed_to_load_dat": "Failed to load resources.dat: {}",
    "loaded_from_embedded": "Resources loaded from embedded module: {} items",
    "failed_to_load_embedded": "Failed to load embedded resources: {}",
    "dat_rebuilt": "resources.dat rebuilt successfully",
    "failed_to_rebuild_dat": "Failed to rebuild resources.dat: {}",
    "resource_not_found": "Resource not found: {}",
    "failed_to_load_pixmap": "Failed to load pixmap for {}: {}",
}

# 암호화 키
key = base64.urlsafe_b64encode(hashlib.sha256(b"croquis_secret_key").digest())
fernet = Fernet(key)

class ResourceLoader:
    """리소스 로더 클래스"""
    
    def __init__(self):
        self.resources = {}
        self.load_resources()
    
    def load_resources(self):
        """리소스 로드 (resources.dat -> embedded_resources.py 순서)"""
        # 1. resources.dat에서 로드 시도
        resources_file = Path(__file__).parent / "dat" / "resources.dat"
        
        if resources_file.exists():
            try:
                with open(resources_file, "rb") as f:
                    encrypted = f.read()
                
                decrypted = fernet.decrypt(encrypted)
                self.resources = json.loads(decrypted.decode())
                logger.info(RESOURCE_LOG_MESSAGES["loaded_from_dat"].format(len(self.resources)))
                return
            except Exception as e:
                logger.error(RESOURCE_LOG_MESSAGES["failed_to_load_dat"].format(e))
        
        # 2. embedded_resources.py에서 로드
        try:
            from embedded_resources import EMBEDDED_RESOURCES
            # 튜플로 저장된 문자열을 합치기
            self.resources = {
                key: "".join(value) if isinstance(value, tuple) else value
                for key, value in EMBEDDED_RESOURCES.items()
            }
            logger.info(RESOURCE_LOG_MESSAGES["loaded_from_embedded"].format(len(self.resources)))
            
            # resources.dat 재생성
            self._rebuild_resources_dat()
        except Exception as e:
            logger.error(RESOURCE_LOG_MESSAGES["failed_to_load_embedded"].format(e))
            self.resources = {}
    
    def _rebuild_resources_dat(self):
        """resources.dat 파일 재생성"""
        try:
            dat_dir = Path(__file__).parent / "dat"
            dat_dir.mkdir(exist_ok=True)
            
            json_data = json.dumps(self.resources, ensure_ascii=False)
            encrypted = fernet.encrypt(json_data.encode())
            
            resources_file = dat_dir / "resources.dat"
            with open(resources_file, "wb") as f:
                f.write(encrypted)
            
            logger.info(RESOURCE_LOG_MESSAGES["dat_rebuilt"])
        except Exception as e:
            logger.error(RESOURCE_LOG_MESSAGES["failed_to_rebuild_dat"].format(e))
    
    def get_pixmap(self, key: str) -> QPixmap:
        """리소스에서 QPixmap 가져오기"""
        if key not in self.resources:
            logger.warning(RESOURCE_LOG_MESSAGES["resource_not_found"].format(key))
            return QPixmap()
        
        try:
            image_data = base64.b64decode(self.resources[key])
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            return pixmap
        except Exception as e:
            logger.error(RESOURCE_LOG_MESSAGES["failed_to_load_pixmap"].format(key, e))
            return QPixmap()
    
    def get_icon(self, key: str):
        """리소스에서 QIcon 가져오기"""
        from PyQt6.QtGui import QIcon
        pixmap = self.get_pixmap(key)
        return QIcon(pixmap)

# 전역 리소스 로더 인스턴스
_resource_loader = None

def get_resource_loader() -> ResourceLoader:
    """리소스 로더 싱글톤 인스턴스 가져오기"""
    global _resource_loader
    if _resource_loader is None:
        _resource_loader = ResourceLoader()
    return _resource_loader
