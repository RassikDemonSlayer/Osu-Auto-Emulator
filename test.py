from mss import mss
import time
from time import sleep
from Functions import region
import threading
import numpy as np
import cv2


def find_object(template_path, region=None, template_size=(50, 50), threshold=0.91):
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
                match_time = time.time()/1000
                return match_time
find_object('Templates\\screenshot_139.raw',region={'left': 1714, 'top': 60, 'width': 50, 'height':50})

