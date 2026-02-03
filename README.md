# Croquis - 크로키 연습 프로그램

크로키 연습을 위한 데스크톱 애플리케이션입니다. 이미지 덱을 관리하고 타이머를 설정하여 체계적인 드로잉 연습을 할 수 있습니다.

## 주요 기능

- **덱 관리**: 이미지 폴더를 덱으로 등록하고 관리
- **타이머 기능**: 크로키 시간을 설정하고 자동으로 이미지 전환
- **다국어 지원**: 한국어/영어 지원
- **알람 기능**: 설정한 시간에 크로키 연습 알림
- **연습 히스토리**: 크로키 연습 기록 자동 저장 및 통계 제공
- **보안**: 사용자별 암호화된 데이터 저장
- **Qt 리소스 시스템**: `.qrc` 형식으로 버튼 이미지와 번역 파일 관리

## Qt Resource System
## 설치 및 실행

### 요구사항

- Python 3.10 이상
- Windows 10/11 (알림 기능 지원)

### 설치

```bash
# 저장소 클론
git clone <repository-url>
cd Croquis2

# 의존성 설치
pip install -r requirements.txt
```

### 실행

```bash
python run.py
```

### 빌드 (실행 파일 생성)

```bash
python scripts/compile_resources.py  # Qt 리소스 컴파일
pyinstaller Croquis.spec             # 실행 파일 빌드
```

빌드된 실행 파일은 `dist/Croquis/` 폴더에 생성됩니다.

## 프로젝트 구조

```
Croquis2/
├── src/                      # 소스 코드
│   ├── core/                 # 핵심 기능
│   │   └── key_manager.py    # 암호화 키 관리
│   ├── gui/                  # GUI 컴포넌트
│   │   └── image_viewer.py   # 이미지 뷰어 윈도우
│   ├── utils/                # 유틸리티
│   │   ├── language_manager.py    # 다국어 지원
│   │   ├── log_manager.py         # 로깅 시스템
│   │   └── qt_resource_loader.py  # Qt 리소스 로더
│   ├── assets/               # 리소스 파일
│   │   ├── btn/              # 버튼 이미지
│   │   ├── icon.ico          # 앱 아이콘
│   │   ├── resources.qrc     # Qt 리소스 정의
│   │   └── resources_rc.py   # 컴파일된 리소스
│   └── main.py               # 메인 애플리케이션
├── scripts/                  # 빌드 스크립트
│   ├── compile.py            # 전체 빌드 스크립트
│   └── compile_resources.py  # Qt 리소스 컴파일
├── data/                     # 사용자 데이터 (생성됨)
├── logs/                     # 로그 파일 (생성됨)
├── run.py                    # 진입점
├── requirements.txt          # Python 의존성
└── Croquis.spec             # PyInstaller 설정
```

## 보안 기능

- **동적 암호화 키**: 사용자 환경(PC UUID + OS 사용자명)에 기반한 고유 키 생성
- **데이터 암호화**: 덱 정보 및 설정이 암호화되어 저장
- **사용자 격리**: 각 사용자는 자신의 암호화된 데이터에만 접근 가능

## 사용 방법

1. **덱 생성**: 메인 화면에서 '편집' 버튼으로 덱 에디터 열기
2. **이미지 추가**: 폴더 선택 또는 개별 이미지 추가
3. **크로키 시작**: 덱 선택 후 시간 설정, '시작' 버튼 클릭
4. **단축키**:
   - `Space`: 재생/일시정지
   - `N`: 다음 이미지
   - `P`: 이전 이미지
   - `F11`: 전체화면 토글
   - `Esc`: 종료

## Qt 리소스 시스템

### 리소스 컴파일

리소스 파일(버튼 이미지, 번역 파일)을 수정한 경우:

```bash
python scripts/compile_resources.py
```

[resources.qrc](src/assets/resources.qrc)를 읽어 [resources_rc.py](src/assets/resources_rc.py) 모듈을 생성합니다.

### 리소스 사용 예제

```python
from utils.qt_resource_loader import QtResourceLoader

loader = QtResourceLoader()

# 이미지 로드
pixmap = loader.get_pixmap(":/buttons/정지.png")
icon = loader.get_icon(":/buttons/재생.png")

# CSV 파일 읽기
csv_data = loader.read_text_file(":/data/translations.csv")

# 리소스 존재 확인
if loader.resource_exists(":/buttons/정지.png"):
    print("리소스 존재!")
```

### PyInstaller 배포 시 주의사항

다음 파일들은 배포 시 포함되지 않아도 됩니다 (모두 `resources_rc.py`에 임베딩됨):
- `resources.qrc` (소스 정의 파일)
- `compile_resources.py` (빌드 도구)
- `btn/` 폴더의 버튼 이미지들
- `translations.csv`

## 기술 스택

- **GUI Framework**: PyQt6
- **암호화**: cryptography (Fernet)
- **알림**: win11toast, plyer
- **빌드**: PyInstaller

## 문제 해결

### 알림이 작동하지 않는 경우
- Windows 11: '알림' 설정에서 앱 알림 권한 확인
- Windows 10: 'win11toast' 대신 'plyer' 백업 알림 사용

### 실행 파일이 바이러스로 탐지되는 경우
- PyInstaller로 빌드된 실행 파일은 오탐지될 수 있습니다
- 소스 코드를 직접 실행(`python run.py`)하거나 백신 예외 처리 추가

### 이미지가 로드되지 않는 경우
- 덱 경로가 유효한지 확인
- 지원 형식: JPG, PNG, BMP, GIF

### 버튼 아이콘이 표시되지 않는 경우
- `python scripts/compile_resources.py`로 Qt 리소스 재컴파일

## 라이선스

이 프로젝트는 개인 사용 목적으로 제작되었습니다.

## 개발자 정보

버전: 2.0.0
