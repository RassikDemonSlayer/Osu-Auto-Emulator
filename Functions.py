from mss import mss
import subprocess
from OsuParsing import osu_exe_path, hit_objects
import time
from time import sleep
from MovementFuncs import click
from Defines import SCREEN_HEIGHT_CENTER, SCREEN_WIDTH_CENTER
import ctypes
import cv2
import numpy as np


region = region={'left': 1714, 'top': 60, 'width': 50, 'height':50}
template_path = 'Templates\\screenshot_130.raw'



VK_CONTROL = 0x11  # Код клавиши Ctrl
VK_V = 0x56        # Код клавиши V

VK_RETURN = 0x0D  # Код клавиши Enter
KEYEVENTF_KEYDOWN = 0x0000  # Нажатие клавиши
KEYEVENTF_KEYUP = 0x0002  # Отпускание клавиши

def press_ctrl_v():
    """Функция для эмуляции нажатия CTRL+V(Через pyautogui раз через раз почему то срабатывает)"""

    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_V, 0, 0, 0)
    sleep(0.05)  
    ctypes.windll.user32.keybd_event(VK_V, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
    
def press_enter():
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYDOWN, 0)
    sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)
    


def find_object(template_path, region=None, template_size=(50, 50), threshold=0.95):
    """Мониторит экрана или области экрана на наличие сырого шаблона.
    
    template_path - Путь да файла с сырым шаблоном (.raw).
    region - Область экрана для анализа: Принимает словарь {top, left, width, height}) или None для всего экрана(default).
    template_size -  Размер шаблона (ширина, высота).
    threshold - Пороговое значение для совпадения (от 0 до 1).
    """

    with open(template_path, "rb") as f:
        raw_data = f.read()
    template = np.frombuffer(raw_data, dtype=np.uint8).reshape((template_size[1], template_size[0], 3))


    with mss() as sct:

        if region is None:
            monitor = sct.monitors[0]
            region = {
                "top": monitor["top"],
                "left": monitor["left"],
                "width": monitor["width"],
                "height": monitor["height"]
            }

        while True:
            screenshot = sct.grab(region)
            screen_data = np.frombuffer(screenshot.rgb, dtype=np.uint8).reshape((screenshot.height, screenshot.width, 3))
            res = cv2.matchTemplate(screen_data, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val >= threshold:
                return True
                # match_time = time.time()/1000
                # return match_time

def play_map():
    previous_time = hit_objects[0].time
    sleep(0.15)
    for ho in hit_objects:
        delay = ho.time-previous_time
        sleep(delay)
        click(ho.x, ho.y)
        sleep(0.001)
        previous_time=ho.time
        
        
def start_game():
    osu_process = subprocess.Popen(osu_exe_path)
    """Выбор и заход на карту"""
    sleep(10)
    click(SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER)

    sleep(0.5)
    click(1230, 320)

    sleep(0.5)
    click(1250, 395)
    
    sleep(0.5)
    press_ctrl_v()
    sleep(1)
    press_enter()
    find_object('Templates\\screenshot_139.raw', region=region)
    play_map()
    osu_process.wait()
    
# if __name__=="__main__":
#     find_object(template_path=template_path, region=region)

