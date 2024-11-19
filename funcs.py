import ctypes
from time import sleep, time
import cv2
import numpy as np
from datetime import datetime
from mss import mss
import pyautogui
from pynput.mouse import Controller, Button
import defines
VK_CONTROL = 0x11  # Код клавиши Ctrl
VK_V = 0x56        # Код клавиши V

VK_RETURN = 0x0D  # Код клавиши Enter
KEYEVENTF_KEYDOWN = 0x0000  # Нажатие клавиши
KEYEVENTF_KEYUP = 0x0002  # Отпускание клавиши

def press_ctrl_v():
    """Функция для эмуляции нажатия CTRL+V(Через pyautogui раз через раз почему то срабатывает)"""
    # Нажимаем клавишу Ctrl
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    # Нажимаем клавишу V
    ctypes.windll.user32.keybd_event(VK_V, 0, 0, 0)
    sleep(0.05)  # Задержка для эмуляции удержания
    # Отпускаем клавишу V
    ctypes.windll.user32.keybd_event(VK_V, 0, 2, 0)
    # Отпускаем клавишу Ctrl
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
    
def press_enter():
    # Нажимаем клавишу ENTER
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYDOWN, 0)
    sleep(0.05)  # Пауза между нажатием и отпусканием
    # Отпускаем клавишу ENTER
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)
    
def osu_to_screen(x, y):
    """Конвертация координат osu! в координаты экрана."""
    screen_x = (x + 180) * (1920 / (691 + 180))
    screen_y = (y + 82) * (1080 / (407 + 82)) - 40
    return int(screen_x), int(screen_y)
#-------------------------
def play_map(match_time, hit_objects):
    mouse = Controller()
    previous_time = hit_objects[0][2]
    sleep(0.011)
    for x, y, hit_time, hit_type in hit_objects:
        delay = hit_time - previous_time
        sleep(delay)
        if(hit_type == LOCAL_FLAG_DOT):    
            mouse.position = (x, y)
            mouse.click(Button.left, 2)
            previous_time = hit_time
            print(f"{OSU_OBJECT_NAMES[hit_type]} Resolved")
        elif(hit_type == LOCAL_FLAG_SLIDER):
            print(f"{OSU_OBJECT_NAMES[hit_type]} NOT IMPLEMENTED")
        elif(hit_type == LOCAL_FLAG_SPINNER):
            print(f"{OSU_OBJECT_NAMES[hit_type]} NOT IMPLEMENTED")
        else:
            print(f"Unknown type: {OSU_OBJECT_NAMES[hit_type]}")
#-----------------------
def monitor_screen_with_raw_template(template_path, region=None, template_size=(60, 60), threshold=0.91):
    """Мониторит экрана или области экрана на наличие сырого шаблона.
    
    template_path - Путь да файла с сырым шаблоном (.raw).
    region - Область экрана для анализа: Принимает словарь {top, left, width, height}) или None для всего экрана(default).
    template_size -  Размер шаблона (ширина, высота).
    threshold - Пороговое значение для совпадения (от 0 до 1).
    """
    # Загружаем шаблон из файла .raw
    with open(template_path, "rb") as f:
        raw_data = f.read()
    template = np.frombuffer(raw_data, dtype=np.uint8).reshape((template_size[1], template_size[0], 3))


    with mss() as sct:
        # Если region не задан, используем размер всего экрана
        if region is None:
            monitor = sct.monitors[0]  # Первый монитор
            region = {
                "top": monitor["top"],
                "left": monitor["left"],
                "width": monitor["width"],
                "height": monitor["height"]
            }

        while True:
            # Захват экрана или указанной области
            screenshot = sct.grab(region)
            screen_data = np.frombuffer(screenshot.rgb, dtype=np.uint8).reshape((screenshot.height, screenshot.width, 3))

            # Сравнение с шаблоном
            res = cv2.matchTemplate(screen_data, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            if max_val >= threshold:
                match_time = time()/1000
                return match_time
                
                
                

