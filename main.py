from time import sleep
import subprocess
import pyperclip
import pyautogui
import defines

from set_up import osu_path, map_name_correct, screen_width_center, screen_height_center, hit_objects, template
from funcs import press_ctrl_v, press_enter, monitor_screen_with_raw_template, play_map

def start_map():
    """Выбор и заход на карту"""
    sleep(8)
    pyautogui.moveTo(screen_width_center, screen_height_center, duration=0.1)
    sleep(0.3)
    pyautogui.click()
    sleep(0.5)
    pyautogui.moveTo(1230, 320)
    sleep(0.3)
    pyautogui.click()
    sleep(0.5)
    pyautogui.moveTo(1250, 395)
    sleep(0.3)
    pyautogui.click()
    sleep(0.5)
    press_ctrl_v()
    sleep(1)
    press_enter()
    match_time = monitor_screen_with_raw_template(template, region=None, template_size=(60, 60))
    play_map(match_time, hit_objects)
    
    
def main():
    pyperclip.copy(map_name_correct) #Копируем в буффер название трека чтобы попасть только на одну карту
    osu_process = subprocess.Popen(osu_path)

    start_map()
    
    osu_process.wait()
    
if __name__ == "__main__":
    pass
    main()