import re
import configparser

def x_osu_to_screen(x):
    """Конвертация координаты X osu! в координаты X экрана."""
    screen_x = (x + 180) * (1920 / (691 + 180))
    
    return int(screen_x)
def y_osu_to_screen(y):
    """Конвертация координаты Y osu! в координаты Y экрана."""
    screen_y = (y + 82) * (1080 / (407 + 82)) - 40
    return int(screen_y)

class TimingPoint:
    def __init__(self, time, beat_length, meter, sample_set, sample_index, volume, uninherited, effects):
        self.time = time  # Время начала тайминг поинта
        self.beat_length = beat_length  # Длина бита
        self.meter = meter  # Метрика
        self.sample_set = sample_set  # Сет звуков
        self.sample_index = sample_index  # Индекс звука
        self.volume = volume  # Громкость
        self.uninherited = uninherited  # Наследование
        self.effects = effects  # Эффекты

class HitObject:
    def __init__(self, x, y, time, object_type, hit_sound, end_time=0, additional_data=None):
        self.x = x  # Позиция по оси X
        self.y = y  # Позиция по оси Y
        self.time = time  # Время появления объекта
        self.object_type = object_type  # Тип объекта
        self.hit_sound = hit_sound  # Звук при клике
        self.end_time = end_time  # Время окончания (для длинных объектов)
        self.additional_data = additional_data  # Дополнительные данные

class OsuParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.timing_points = []
        self.hit_objects = []

    def parse(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        section = None
        for line in lines:
            line = line.strip()
            if line.startswith('['):
                section = line[1:line.index(']')]  # Определяем секцию
            elif section == 'TimingPoints':
                self._parse_timing_point(line)
            elif section == 'HitObjects':
                self._parse_hit_object(line)

    def _parse_timing_point(self, line):
        # 100,300,0,2,0,0,0
        # Формат: time, beat_length, meter, sample_set, sample_index, volume, uninherited, effects
        parts = line.split(',')
        if len(parts) >= 8:
            time = int(parts[0])
            beat_length = float(parts[1])
            meter = int(parts[2])
            sample_set = int(parts[3])
            sample_index = int(parts[4])
            volume = int(parts[5])
            uninherited = int(parts[6])
            effects = int(parts[7])
            timing_point = TimingPoint(time, beat_length, meter, sample_set, sample_index, volume, uninherited, effects)
            self.timing_points.append(timing_point)

    def _parse_hit_object(self, line):
        # 256,192,158988,1,0,0:0:0:
        # Формат: x, y, time, object_type, hit_sound, additional_data
        parts = line.split(',')
        if len(parts) >= 5:
            x = x_osu_to_screen(int(parts[0]))
            y = y_osu_to_screen(int(parts[1]))
            time = int(parts[2])/1000
            object_type = int(parts[3])
            hit_sound = int(parts[4])
            additional_data = parts[5] if len(parts) > 5 else None
            hit_object = HitObject(x, y, time, object_type, hit_sound, additional_data=additional_data)
            self.hit_objects.append(hit_object)

    def get_timing_points(self):
        return self.timing_points

    def get_hit_objects(self):
        return self.hit_objects
    

config = configparser.ConfigParser()


config.read('config.ini', encoding='utf-8')


osu_file = config['Settings']['file_path']
osu_exe_path = config['Settings']['osu_exe_path']

import re

def get_beatmap_name(file_path):
    match = re.search(r'[^/\\]+\.osu$', file_path)
    if not match:
        return None  
    
    file_name = match.group() 
    file_name = file_name[:-4] 
    

    file_name = re.sub(r'\s*\(.*?\)', '', file_name)
    

    clean_name = re.sub(r'\s*\[.*?\]', '', file_name).strip()
    difficulty = re.search(r'\[.*?\]', file_name) 
    

    result = clean_name
    if difficulty:
        result += f" {difficulty.group()[1:-1]}"
    
    return result

beatmap_name = get_beatmap_name(osu_file)

parser = OsuParser(osu_file)
parser.parse()

timing_points = parser.get_timing_points()
hit_objects = parser.get_hit_objects()


for ho in hit_objects:
    print(ho.x, ho.y, ho.time)

