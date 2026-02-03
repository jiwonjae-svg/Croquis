"""
Alarm management functionality for Croquis application
"""

import logging
from datetime import datetime
from core.key_manager import decrypt_data
from utils.common import get_data_path, show_toast_notification, get_icon_path
from utils.log_manager import LOG_MESSAGES

logger = logging.getLogger('Croquis')


def check_and_trigger_alarms():
    """Check and trigger alarms (prevent duplicates)"""
    dat_dir = get_data_path() / "dat"
    alarms_file = dat_dir / "alarms.dat"
    
    if not alarms_file.exists():
        return
    
    try:
        with open(alarms_file, "rb") as f:
            encrypted = f.read()
        data = decrypt_data(encrypted)
        alarms = data.get("alarms", [])
        
        if not alarms:
            return
        
        logger.info(LOG_MESSAGES["alarm_checking"].format(len(alarms)))
        
        # Current time
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")
        current_weekday = now.weekday()
        icon_path = get_icon_path()
        
        # Check alarms
        for i, alarm in enumerate(alarms):
            if not alarm.get("enabled", False):
                continue
            
            alarm_time = alarm.get("time", "")
            alarm_type = alarm.get("type", "")
            
            # Check time match
            if alarm_time != current_time:
                continue
            
            # Check by type
            should_trigger = False
            
            if alarm_type == "weekday":
                weekdays = alarm.get("weekdays", [])
                if current_weekday in weekdays:
                    should_trigger = True
            elif alarm_type == "date":
                alarm_date = alarm.get("date", "")
                if alarm_date == current_date:
                    should_trigger = True
            
            if should_trigger:
                title = alarm.get("title", "Croquis Alarm")
                message = alarm.get("message", "Time to practice croquis!")
                logger.info(LOG_MESSAGES["alarm_triggered"].format(title, current_time))
                show_toast_notification(title, message, icon_path)
                
    except Exception as e:
        logger.error(LOG_MESSAGES["alarm_check_failed"].format(e))
