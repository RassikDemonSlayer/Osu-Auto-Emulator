import re
import pyautogui
from funcs import osu_to_screen
import defines

#========================= Настройки и переменные ====================================================================
screen_width, screen_height = pyautogui.size() #Разрешение экрана
screen_width_center, screen_height_center = (int(screen_width/2), int(screen_height/2)) #Координаты центра экрана

start_config_file = "start_config.txt" #файл с конфигом

region = {"top": 60, "left": 1700, "width": 77, "height": 60} #Область поиска совпадения на экране
template = "objects\\end_timer.raw"
#=====================================================================================================================



#============================ Парсинг конфига ========================================================================
config = []
with open(start_config_file, 'r', encoding='utf-8') as file:
    """Получаем информацию из текстового документа о путях к самой осу, карте и т.д."""
    config_list = list(file)
    for line in config_list:
        line = line.split(": ")
        config.append(line[1])

def correct_map_name(map_name):
    """Получение корректного имени карты"""
    pattern = r"\([^)]*\)|\.osu" #Паттерн для удаления расширения и содержимого круглых скобок
    cleaned_string = re.sub(pattern, "", map_name).strip() # Убираем ненужные части
    
    square_brackets_pattern = r"\[([^\]]+)\]" # Извлечение текста из квадратных скобок
    square_content = re.search(square_brackets_pattern, cleaned_string)
    
    if square_content: #Удаляем квадратные скобки и добавляем содержимое к оставшемуся тексту
        final_string = re.sub(r"\[.*?\]", "", cleaned_string).strip() + " " + square_content.group(1)
    else:
        final_string = cleaned_string
    
    return final_string


osu_path = config[0].strip() #Путь до osu!.exe
map_path = config[1].strip() #Папка с картой
map_name = config[2].strip() #Название карты
map_name_correct = correct_map_name(map_name) #Имя файла без лишних скобок для вставки
map_full_path = map_path + "\\" + map_name #Полный путь до карты
del config
#=======================================================================================================================



#========================== Парсинг Osu! файла =========================================================================

hit_objects = []
with open(map_full_path, 'r', encoding='utf-8') as file:
    osu_data = file.read()

# Извлечение строк с hit objects
hit_objects_section = osu_data.split("[HitObjects]")[1].split("[")[0].strip()

for line in hit_objects_section.split("\n"):
    if line:  # Пропускаем пустые строки
        # Разделяем строку на части и извлекаем x, y, hit_time
        parts = line.split(",")
        x = int(parts[0])
        y = int(parts[1])
        hit_time = int(parts[2])
        flags = int(parts[3])
        hit_type = -1
        index = 0
        for i in OSU_OBJECT_FLAGS:
            if((flags & i) == i and i != OSU_FLAG_NEW_COMBO):
                hit_type = LOCAL_TYPE_FLAGS[index]
            index += 1
        hit_objects.append([x, y, hit_time, hit_type])
for hit_obj in hit_objects: 
    hit_obj[2] /= 1000

#=======================================================================================================================
def prepare_hit_objects(hit_objects):
    """Подготовка данных: конвертация osu-координат в экранные."""
    prepared_objects = []
    for hit_obj in hit_objects:
        x, y, time, hit_type = hit_obj
        screen_x, screen_y = osu_to_screen(x, y)  # Конвертируем координаты
        prepared_objects.append((screen_x, screen_y, time, hit_type))
    return prepared_objects

hit_objects = prepare_hit_objects(hit_objects)

