"""
크로키 알람 확인 스크립트 (Windows 토스트 알림)
Windows 작업 스케줄러에서 주기적으로 실행됩니다.
"""
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

# 실행 파일 또는 스크립트 디렉토리 찾기
if getattr(sys, 'frozen', False):
    # 컴파일된 실행 파일
    base_dir = Path(sys.executable).parent
else:
    # 스크립트 실행
    base_dir = Path(__file__).parent

# main.py의 경로를 import path에 추가
sys.path.insert(0, str(base_dir))

from main import decrypt_data

def show_toast_notification(title: str, message: str, icon_path: str = None):
    """Windows 토스트 알림 표시"""
    # 아이콘 경로 설정
    if icon_path is None:
        if getattr(sys, 'frozen', False):
            icon_path = str(Path(sys.executable).parent / "icon.ico")
        else:
            icon_path = str(Path(__file__).parent / "icon.ico")
    
    # 1순위: win11toast (Windows 10/11 네이티브 알림, 가장 안정적)
    try:
        from win11toast import toast_async
        import asyncio
        
        async def show_toast():
            await toast_async(
                title,
                message,
                icon=icon_path if os.path.exists(icon_path) else None,
                app_id="Croquis Practice"
            )
        
        # 비동기 실행
        asyncio.run(show_toast())
        return
        
    except Exception as e:
        pass  # 다음 방법 시도
    
    # 2순위: plyer (크로스 플랫폼)
    try:
        from plyer import notification
        
        notification.notify(
            title=title,
            message=message,
            app_name="Croquis Practice",
            app_icon=icon_path if icon_path and os.path.exists(icon_path) else None,
            timeout=10
        )
        return
        
    except Exception as e:
        pass  # 다음 방법 시도
    
    # 최후의 수단: 콘솔 출력
    print(f"[ALARM] {title}: {message}")

def check_and_trigger_alarms():
    """알람 확인 및 실행"""
    # 알람 데이터 로드
    if getattr(sys, 'frozen', False):
        dat_dir = Path(sys.executable).parent / "dat"
    else:
        dat_dir = Path(__file__).parent / "dat"
    
    alarms_file = dat_dir / "alarms.dat"
    
    if not alarms_file.exists():
        sys.exit(0)
    
    try:
        with open(alarms_file, "rb") as f:
            encrypted = f.read()
        data = decrypt_data(encrypted)
        alarms = data.get("alarms", [])
        
        # 현재 시간
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")
        current_weekday = now.weekday()
        
        if getattr(sys, 'frozen', False):
            icon_path = str(Path(sys.executable).parent / "icon.ico")
        else:
            icon_path = str(Path(__file__).parent / "icon.ico")
        
        # 알람 확인
        for alarm in alarms:
            if not alarm.get("enabled", False):
                continue
            
            alarm_time = alarm.get("time", "")
            alarm_type = alarm.get("type", "")
            
            # 시간 매칭 확인
            if alarm_time != current_time:
                continue
            
            # 타입별 확인
            should_trigger = False
            
            if alarm_type == "weekday":
                # 요일별 반복
                weekdays = alarm.get("weekdays", [])
                if current_weekday in weekdays:
                    should_trigger = True
            elif alarm_type == "date":
                # 특정 날짜
                alarm_date = alarm.get("date", "")
                if alarm_date == current_date:
                    should_trigger = True
            
            if should_trigger:
                # 알람 트리거 - 토스트 알림 표시
                title = alarm.get("title", "크로키 알람")
                message = alarm.get("message", "크로키 연습 시간입니다!")
                
                # Windows 토스트 알림 표시
                show_toast_notification(title, message, icon_path)
                
    except Exception as e:
        print(f"Error checking alarms: {e}")
    
    sys.exit(0)

if __name__ == "__main__":
    check_and_trigger_alarms()
