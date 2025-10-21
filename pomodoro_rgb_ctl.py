#!/usr/bin/env python3
import time
import subprocess
from pathlib import Path

ZONE_PATH = Path("/sys/devices/platform/hp-wmi/rgb_zones/zone00")

FLAG_PATHS = {
    "work": Path("/tmp/pomodoro_work_flag"),
    "break": Path("/tmp/pomodoro_break_flag"),
    "pause": Path("/tmp/pomodoro_pause_flag"),
}

COLORS = {
    "default": "ffc800",  
    "work": "ff0000",     
    "break": "00ff00",    
    "pause": "404040",    
}

def sudo_write(col_hex):
    """Записывает HEX-код в системный файл с помощью sudo tee."""
    try:
        subprocess.run(["sudo", "tee", str(ZONE_PATH)], input=col_hex.encode(),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print(f"Ошибка записи цвета: проверьте права sudoers для {ZONE_PATH}")
        exit(1)

def set_color(color_key):
    """Применяет цвет из словаря COLORS."""
    col_hex = COLORS.get(color_key, COLORS["default"])
    sudo_write(col_hex)

def get_pomodoro_state():
    """Проверяет наличие файлов-флагов."""
    if FLAG_PATHS["work"].exists():
        return "work"
    if FLAG_PATHS["break"].exists():
        return "break"
    if FLAG_PATHS["pause"].exists():
        return "pause"
    
    return "default"


if __name__ == "__main__":
    current_state = ""
    for p in FLAG_PATHS.values():
        if p.exists():
            p.unlink()

    print("Контроллер RGB запущен. Мониторинг файлов-флагов...")
    
    while True:
        try:
            new_state = get_pomodoro_state()
            
            if new_state != current_state:
                set_color(new_state)
                current_state = new_state
                
            time.sleep(1) 
            
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            break
