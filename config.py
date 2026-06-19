WIDTH, HEIGHT = 1000, 600
FPS = 60

TABLE_MARGIN = 60
GOAL_ZONE = 30

PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
PADDLE_SPEED = 6

BALL_SIZE = 14
BALL_MAX_SPEED = 14

BALL_ACCELERATION = {
    "easy": 0.15,
    "normal": 0.25,
    "hard": 0.40,
    "hardcore": 0.90
}

SERVE_SPEED = 3.0

ROUND_TIMES = {
    "1 минута": 60, "1.5 минуты": 90, "2 минуты": 120,
    "3 минуты": 180, "5 минут": 300, "10 минут": 600,
    "Бесконечно": 99999
}

TARGET_SCORES = {
    "До 2": 2, "До 5": 5, "До 10": 10,
    "До 20": 20, "До 30": 30, "До 50": 50,
    "Бесконечно": 999
}

DIFFICULTY_SETTINGS = {
    "easy":    {"name_ru": "Лёгкая",    "name_en": "Easy",    "speed": 3, "error_chance": 0.4, "predict": False},
    "normal":  {"name_ru": "Нормальная","name_en": "Normal",  "speed": 5, "error_chance": 0.15,"predict": False},
    "hard":    {"name_ru": "Сложная",   "name_en": "Hard",    "speed": 7, "error_chance": 0.0, "predict": True},
    "hardcore":{"name_ru": "Хардкор",   "name_en": "Hardcore","speed": 10,"error_chance": 0.0, "predict": True}
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
RED = (255, 50, 50)
DARK_BG = (25, 25, 35)

BALL_COLORS = {
    "Белый": WHITE,
    "Жёлтый": YELLOW,
    "Оранжевый": ORANGE
}

THEMES = {
    "green":  {"name": "Зелёный",    "table": (34, 139, 34), "table_dark": (25, 100, 25),
               "paddle_player": (0, 255, 0), "paddle_computer": (0, 180, 0), "paddle_player2": (180, 255, 180)},
    "blue":   {"name": "Синий",      "table": (30, 60, 120), "table_dark": (20, 40, 80),
               "paddle_player": (50, 150, 255), "paddle_computer": (30, 100, 200), "paddle_player2": (150, 200, 255)},
    "red":    {"name": "Красный",    "table": (139, 0, 0), "table_dark": (100, 0, 0),
               "paddle_player": (255, 80, 80), "paddle_computer": (200, 50, 50), "paddle_player2": (255, 150, 150)},
    "purple": {"name": "Фиолетовый", "table": (75, 0, 130), "table_dark": (50, 0, 90),
               "paddle_player": (180, 100, 255), "paddle_computer": (130, 50, 200), "paddle_player2": (200, 150, 255)},
    "gold":   {"name": "Золотой",    "table": (139, 119, 0), "table_dark": (100, 80, 0),
               "paddle_player": (255, 215, 0), "paddle_computer": (200, 170, 0), "paddle_player2": (255, 230, 100)}
}

ACHIEVEMENTS_LIST = {
    "first_goal":       {"name_ru": "Первая кровь!",        "name_en": "First Blood!",        "desc_ru": "Забить первый гол", "desc_en": "Score first goal", "hint_ru": "Просто начни играть!", "hint_en": "Just start playing!"},
    "first_win":        {"name_ru": "Первая победа",        "name_en": "First Win",            "desc_ru": "Выиграть первый матч", "desc_en": "Win first match", "hint_ru": "Победи кого-нибудь!", "hint_en": "Beat someone!"},
    "hattrick":         {"name_ru": "Хет-трик",             "name_en": "Hat-trick",            "desc_ru": "3 гола подряд", "desc_en": "3 goals in a row", "hint_ru": "Не пропускай между голами", "hint_en": "Don't concede between goals"},
    "draw_master":      {"name_ru": "Миротворец",           "name_en": "Peacemaker",           "desc_ru": "Сыграть в ничью", "desc_en": "Play a draw", "hint_ru": "Сложнее чем кажется!", "hint_en": "Harder than it seems!"},
    "close_call":       {"name_ru": "На волоске",           "name_en": "Close Call",           "desc_ru": "Победить с разницей в 1 гол", "desc_en": "Win by 1 goal", "hint_ru": "Держи интригу до конца!", "hint_en": "Keep it close!"},
    "corner_goal":      {"name_ru": "В девятку",            "name_en": "Top Corner",           "desc_ru": "Забить гол от края стены", "desc_en": "Score from wall edge", "hint_ru": "Целься в углы!", "hint_en": "Aim for corners!"},
    "self_goal":        {"name_ru": "Автогол",              "name_en": "Own Goal",             "desc_ru": "Забить в свои ворота", "desc_en": "Score in own goal", "hint_ru": "Эм... зачем?", "hint_en": "Um... why?"},
    "streak_5":         {"name_ru": "На раскате",           "name_en": "On Fire",              "desc_ru": "5 голов подряд", "desc_en": "5 goals in a row", "hint_ru": "Тренируйся на лёгком ИИ", "hint_en": "Practice vs Easy AI"},
    "fast_goal":        {"name_ru": "Молниеносный",         "name_en": "Lightning Fast",       "desc_ru": "Гол за 3 секунды", "desc_en": "Goal in 3 seconds", "hint_ru": "Сразу после подачи — удар!", "hint_en": "Right after serve — hit!"},
    "clean_sheet":      {"name_ru": "Сухарь",               "name_en": "Clean Sheet",          "desc_ru": "Победить 5:0", "desc_en": "Win 5:0", "hint_ru": "Не дай забить ни разу", "hint_en": "Don't let them score"},
    "comeback":         {"name_ru": "Камбэк",               "name_en": "Comeback",             "desc_ru": "Отыграться с 0:3", "desc_en": "Comeback from 0:3", "hint_ru": "Никогда не сдавайся!", "hint_en": "Never give up!"},
    "pvp_win":          {"name_ru": "Дуэлянт",              "name_en": "Duelist",              "desc_ru": "Победить в PvP", "desc_en": "Win in PvP", "hint_ru": "Позови друга!", "hint_en": "Call a friend!"},
    "overtime_win":     {"name_ru": "Овертайм",             "name_en": "Overtime",             "desc_ru": "Победить по времени", "desc_en": "Win by timeout", "hint_ru": "Тяни время если ведёшь!", "hint_en": "Stall if you lead!"},
    "double_goal":      {"name_ru": "Дубль",                "name_en": "Double",               "desc_ru": "2 гола за 5 секунд", "desc_en": "2 goals in 5 seconds", "hint_ru": "Быстрая атака!", "hint_en": "Fast attack!"},
    "speed_demon":      {"name_ru": "Реактивный",           "name_en": "Speed Demon",          "desc_ru": "Мяч разогнался до 12", "desc_en": "Ball reached speed 12", "hint_ru": "Долгий матч без голов", "hint_en": "Long match without goals"},
    "marathon":         {"name_ru": "Марафонец",            "name_en": "Marathon Runner",      "desc_ru": "Матч 10+ минут", "desc_en": "10+ min match", "hint_ru": "Включи бесконечное время", "hint_en": "Enable infinite time"},
    "longest_game":     {"name_ru": "Долгожитель",          "name_en": "Long Liver",           "desc_ru": "Матч дольше 20 минут", "desc_en": "20+ min match", "hint_ru": "Это требует терпения!", "hint_en": "This requires patience!"},
    "ten_goals":        {"name_ru": "Бомбардир",            "name_en": "Bomber",               "desc_ru": "Забить 10 голов за матч", "desc_en": "Score 10 goals in a match", "hint_ru": "Играй против лёгкого ИИ", "hint_en": "Play vs Easy AI"},
    "domination":       {"name_ru": "Доминация",            "name_en": "Domination",           "desc_ru": "Победить с разницей 10+", "desc_en": "Win by 10+ goals", "hint_ru": "Разгроми соперника!", "hint_en": "Crush your opponent!"},
    "pve_hard":         {"name_ru": "Ветеран",              "name_en": "Veteran",              "desc_ru": "Победить на сложной", "desc_en": "Win on Hard", "hint_ru": "Тренируй реакцию!", "hint_en": "Train your reaction!"},
    "hardcore_win":     {"name_ru": "Хардкор пройден",      "name_en": "Hardcore Complete",    "desc_ru": "Победить на Хардкоре", "desc_en": "Win on Hardcore", "hint_ru": "Это испытание для лучших!", "hint_en": "A challenge for the best!"},
    "perfect_round":    {"name_ru": "Идеальный раунд",      "name_en": "Perfect Round",        "desc_ru": "Выиграть раунд не пропустив", "desc_en": "Win round without conceding", "hint_ru": "Безупречная защита", "hint_en": "Flawless defense"},
    "no_death_win":     {"name_ru": "Бессмертный",          "name_en": "Immortal",             "desc_ru": "Победить не пропустив ни гола", "desc_en": "Win without conceding", "hint_ru": "Идеальный матч!", "hint_en": "Perfect match!"},
    "comeback_5":       {"name_ru": "Феникс",               "name_en": "Phoenix",              "desc_ru": "Отыграться с 0:5", "desc_en": "Comeback from 0:5", "hint_ru": "Никогда не сдавайся!", "hint_en": "Never surrender!"},
    "fast_match":       {"name_ru": "Блицкриг",             "name_en": "Blitzkrieg",           "desc_ru": "Победить за 30 секунд", "desc_en": "Win in 30 seconds", "hint_ru": "Атакуй с первой секунды!", "hint_en": "Attack from second one!"},
    "speedrun":         {"name_ru": "Спидран",              "name_en": "Speedrun",             "desc_ru": "Победить до 5 за 20 секунд", "desc_en": "Win to 5 in 20 sec", "hint_ru": "Каждая секунда на счету!", "hint_en": "Every second counts!"},
    "ten_wins":         {"name_ru": "Чемпион",              "name_en": "Champion",             "desc_ru": "Выиграть 10 матчей", "desc_en": "Win 10 matches", "hint_ru": "Играй регулярно!", "hint_en": "Play regularly!"},
    "all_themes":       {"name_ru": "Коллекционер",         "name_en": "Collector",            "desc_ru": "Попробовать все 5 тем", "desc_en": "Try all 5 themes", "hint_ru": "Меняй тему в настройках", "hint_en": "Change theme in settings"},
    "long_rally":       {"name_ru": "Теннисист",            "name_en": "Tennis Player",        "desc_ru": "10 ударов подряд без гола", "desc_en": "10 hits without goal", "hint_ru": "Держи мяч в игре!", "hint_en": "Keep the ball in play!"},
    "god_mode":         {"name_ru": "Бог понга",            "name_en": "Pong God",             "desc_ru": "Открыть 20 достижений", "desc_en": "Unlock 20 achievements", "hint_ru": "Продолжай играть!", "hint_en": "Keep playing!"},
}

ACHIEVEMENTS_FILE = "achievements.txt"

DEFAULT_DIFFICULTY = "normal"
DEFAULT_THEME = "green"
DEFAULT_MUSIC_VOLUME = 0.5
DEFAULT_SFX_VOLUME = 0.7
DEFAULT_ROUND_TIME = "1.5 минуты"
DEFAULT_TARGET_SCORE = "До 5"
DEFAULT_BALL_COLOR = "Белый"
DEFAULT_LANGUAGE = "ru"

SETTINGS_FILE = "settings.txt"