"""
Croquis 프로그램 컴파일 스크립트
PyInstaller를 사용하여 실행 파일 생성
"""
import subprocess
import sys
from pathlib import Path

def compile_croquis():
    """Compile Croquis application"""
    
    # 현재 디렉터리
    current_dir = Path(__file__).parent
    icon_path = current_dir / "icon.ico"
    main_py = current_dir / "main.py"
    
    # PyInstaller 명령어 (최적화됨)
    cmd = [
        "pyinstaller",
        "--name=Croquis",
        "--windowed",  # GUI 애플리케이션 (콘솔 창 숨김)
        "--onefile",  # 단일 실행 파일로 컴파일
        f"--icon={icon_path}",  # 아이콘 설정
        "--add-data=dat;dat",  # dat 폴더 포함
        "--add-data=translations.csv;.",  # 번역 파일 포함
        "--add-data=icon.ico;.",  # 아이콘 파일 포함
        
        # 최적화 옵션
        "--noupx",  # UPX 압축 비활성화 (안정성 향상)
        "--clean",  # 이전 빌드 캐시 제거
        
        # 필수 imports만 포함
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=cryptography.fernet",
        "--hidden-import=PIL.Image",
        "--hidden-import=win11toast",
        "--hidden-import=plyer",
        "--hidden-import=asyncio",
        
        # 불필요한 모듈 제외 (용량 감소)
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        "--exclude-module=scipy",
        "--exclude-module=IPython",
        "--exclude-module=jupyter",
        "--exclude-module=tkinter",
        
        # 로그 레벨
        "--log-level=WARN",
        
        str(main_py)
    ]
    
    print("=" * 60)
    print("Croquis 프로그램 컴파일 시작")
    print("=" * 60)
    print()
    print(f"아이콘: {icon_path}")
    print(f"메인 파일: {main_py}")
    print()
    
    try:
        # PyInstaller 실행
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        print()
        print("=" * 60)
        print("✓ 컴파일 성공!")
        print("=" * 60)
        print()
        print(f"실행 파일 위치: {current_dir / 'dist' / 'Croquis.exe'}")
        print()
        
    except subprocess.CalledProcessError as e:
        print("=" * 60)
        print("✗ 컴파일 실패!")
        print("=" * 60)
        print()
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("=" * 60)
        print("✗ PyInstaller가 설치되어 있지 않습니다!")
        print("=" * 60)
        print()
        print("다음 명령어로 설치하세요:")
        print("pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    compile_croquis()
