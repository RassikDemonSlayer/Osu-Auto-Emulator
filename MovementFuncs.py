import ctypes
from ctypes import wintypes

# Константы для мыши
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x02  # Нажатие ЛКМ
MOUSEEVENTF_LEFTUP = 0x04    # Отпускание ЛКМ
MOUSEEVENTF_MOVE = 0x0001    # Перемещение мыши

# Структуры для использования с ctypes
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [("dx", wintypes.LONG),
                        ("dy", wintypes.LONG),
                        ("mouseData", wintypes.DWORD),
                        ("dwFlags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", ctypes.POINTER(ctypes.c_void_p))]

        _fields_ = [("mi", MOUSEINPUT)]  # Для мыши

    _fields_ = [("type", wintypes.DWORD),
                ("_input", _INPUT)]


SendInput = ctypes.windll.user32.SendInput


def click(x, y):
    screen_width = ctypes.windll.user32.GetSystemMetrics(0) 
    screen_height = ctypes.windll.user32.GetSystemMetrics(1) 
    # Преобразуем в абсолютные координаты
    abs_x = int(x * 65535 / screen_width)  
    abs_y = int(y * 65535 / screen_height)  

    # Перемещаем мышь в точку (abs_x, abs_y)
    input_event = INPUT()
    input_event.type = INPUT_MOUSE
    input_event._input.mi.dx = abs_x
    input_event._input.mi.dy = abs_y
    input_event._input.mi.dwFlags = MOUSEEVENTF_MOVE | 0x8000 
    SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))


    input_event._input.mi.dwFlags = MOUSEEVENTF_LEFTDOWN  # Нажатие ЛКМ
    SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))
    input_event._input.mi.dwFlags = MOUSEEVENTF_LEFTUP  # Отпускание ЛКМ
    SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))


