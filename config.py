WIDTH, HEIGHT = 1000, 600
FPS = 60

TABLE_MARGIN = 60
GOAL_ZONE = 18

PADDLE_WIDTH = 13
PADDLE_HEIGHT = 90
PADDLE_SPEED = 7

BALL_SIZE = 14
BALL_MAX_SPEED = 15


BALL_ACCELERATION = {
    "easy": 0.15,
    "normal": 0.25,
    "hard": 0.40,
    "hardcore": 0.70
}

SERVE_SPEED = 3

ROUND_TIMES = {
    "15 секунд": 15,
    "30 секунд": 30,"1 минута": 60, "1.5 минуты": 90, "2 минуты": 120,
    "3 минуты": 180, "5 минут": 300, "10 минут": 600,
    "Бесконечно": 99999
}

TARGET_SCORES = {
    "До 2": 2, "До 5": 5, "До 10": 10,
    "До 20": 20, "До 30": 30, "До 50": 50,"До 80": 80,
    "До 100": 100,
    "Бесконечно": 999
}

DIFFICULTY_SETTINGS = {
    "easy": {
        "name_ru": "Лёгкая",
        "name_en": "Easy",
        "speed": 4,
        "error_chance": 0.2,
        "predict": False
    },
    "normal": {
        "name_ru": "Нормальная",
        "name_en": "Normal",
        "speed": 6,
        "error_chance": 0.1,
        "predict": False
    },
    "hard": {
        "name_ru": "Сложная",
        "name_en": "Hard",
        "speed": 9,
        "error_chance": 0.0,
        "predict": True
    },
    "hardcore": {
        "name_ru": "Хардкор",
        "name_en": "Hardcore",
        "speed": 11,
        "error_chance": 0.0,
        "predict": True
    }
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
    "green": {
        "name": "Зелёный",
        "table": (34, 139, 34),
        "table_dark": (25, 100, 25),
        "paddle_player": (0, 255, 0),
        "paddle_computer": (180, 255, 180),
        "paddle_player2": (180, 255, 180)
    },
    "blue": {
        "name": "Синий",
        "table": (30, 60, 120),
        "table_dark": (20, 40, 80),
        "paddle_player": (50, 150, 255),
        "paddle_computer": (150, 200, 255),
        "paddle_player2": (150, 200, 255)
    },
    "red": {
        "name": "Красный",
        "table": (139, 0, 0),
        "table_dark": (100, 0, 0),
        "paddle_player": (255, 80, 80),
        "paddle_computer": (255, 150, 150),
        "paddle_player2": (255, 150, 150)
    },
    "purple": {
        "name": "Фиолетовый",
        "table": (75, 0, 130),
        "table_dark": (50, 0, 90),
        "paddle_player": (180, 100, 255),
        "paddle_computer": (200, 150, 255),
        "paddle_player2": (200, 150, 255)
    },
    "gold": {
        "name": "Золотой",
        "table": (139, 119, 0),
        "table_dark": (100, 80, 0),
        "paddle_player": (255, 215, 0),
        "paddle_computer": (255, 230, 100),
        "paddle_player2": (255, 230, 100)
    }
}

ACHIEVEMENTS_LIST = {
    # ЛЁГКИЕ
    "first_goal": {"name_ru": "Первая кровь!", "name_en": "First Blood!", "desc_ru": "Забить первый гол",
                   "desc_en": "Score first goal", "hint_ru": "Просто начни играть!", "hint_en": "Just start playing!"},
    "first_win": {"name_ru": "Первая победа", "name_en": "First Win", "desc_ru": "Выиграть первый матч",
                  "desc_en": "Win first match", "hint_ru": "Победи кого-нибудь!", "hint_en": "Beat someone!"},
    "hattrick": {"name_ru": "Хет-трик", "name_en": "Hat-trick", "desc_ru": "3 гола подряд",
                 "desc_en": "3 goals in a row", "hint_ru": "Не пропускай между голами",
                 "hint_en": "Don't concede between goals"},
    "draw_master": {"name_ru": "Миротворец", "name_en": "Peacemaker", "desc_ru": "Сыграть в ничью",
                    "desc_en": "Play a draw", "hint_ru": "Сложнее чем кажется!", "hint_en": "Harder than it seems!"},

    # СРЕДНИЕ
    "clean_sheet": {"name_ru": "Сухарь", "name_en": "Clean Sheet", "desc_ru": "Победить 5:0", "desc_en": "Win 5:0",
                    "hint_ru": "Не дай забить ни разу", "hint_en": "Don't let them score"},
    "comeback": {"name_ru": "Камбэк", "name_en": "Comeback", "desc_ru": "Отыграться с 0:3",
                 "desc_en": "Comeback from 0:3", "hint_ru": "Никогда не сдавайся!", "hint_en": "Never give up!"},
    "streak_5": {"name_ru": "На раскате", "name_en": "On Fire", "desc_ru": "5 голов подряд",
                 "desc_en": "5 goals in a row", "hint_ru": "Тренируйся на лёгком ИИ", "hint_en": "Practice vs Easy AI"},
    "fast_goal": {"name_ru": "Молниеносный", "name_en": "Lightning Fast", "desc_ru": "Гол за 3 секунды после подачи",
                  "desc_en": "Goal in 3 seconds", "hint_ru": "Сразу после подачи — удар!",
                  "hint_en": "Right after serve — hit!"},
    "pvp_win": {"name_ru": "Дуэлянт", "name_en": "Duelist", "desc_ru": "Победить в режиме PvP", "desc_en": "Win in PvP",
                "hint_ru": "Позови друга!", "hint_en": "Call a friend!"},
    "speed_demon": {"name_ru": "Реактивный", "name_en": "Speed Demon", "desc_ru": "Мяч разогнался до 12",
                    "desc_en": "Ball reached speed 12", "hint_ru": "Долгий матч без голов",
                    "hint_en": "Long match without goals"},
    "marathon": {"name_ru": "Марафонец", "name_en": "Marathon Runner", "desc_ru": "Матч 10+ минут",
                 "desc_en": "10+ min match", "hint_ru": "Включи бесконечное время", "hint_en": "Enable infinite time"},

    # СЛОЖНЫЕ
    "ten_goals": {"name_ru": "Бомбардир", "name_en": "Bomber", "desc_ru": "Забить 10 голов за матч",
                  "desc_en": "Score 10 goals in a match", "hint_ru": "Играй против лёгкого ИИ",
                  "hint_en": "Play vs Easy AI"},
    "domination": {"name_ru": "Доминация", "name_en": "Domination", "desc_ru": "Победить с разницей 10+",
                   "desc_en": "Win by 10+ goals", "hint_ru": "Разгроми соперника!", "hint_en": "Crush your opponent!"},
    "pve_hard": {"name_ru": "Ветеран", "name_en": "Veteran", "desc_ru": "Победить на сложной", "desc_en": "Win on Hard",
                 "hint_ru": "Тренируй реакцию!", "hint_en": "Train your reaction!"},
    "hardcore_win": {"name_ru": "Хардкор пройден", "name_en": "Hardcore Complete", "desc_ru": "Победить на Хардкоре",
                     "desc_en": "Win on Hardcore", "hint_ru": "Это испытание для лучших!",
                     "hint_en": "A challenge for the best!"},
    "no_death_win": {"name_ru": "Бессмертный", "name_en": "Immortal", "desc_ru": "Победить не пропустив ни гола",
                     "desc_en": "Win without conceding", "hint_ru": "Идеальный матч!", "hint_en": "Perfect match!"},
    "comeback_5": {"name_ru": "Феникс", "name_en": "Phoenix", "desc_ru": "Отыграться с 0:5",
                   "desc_en": "Comeback from 0:5", "hint_ru": "Никогда не сдавайся!", "hint_en": "Never surrender!"},

    # ЛЕГЕНДАРНЫЕ
"longest_game":     {"name_ru": "Долгожитель","name_en": "Long Liver","desc_ru": "Матч 20+ минут",
                     "desc_en": "20+ min match", "hint_ru": "Включи бесконечное время!", "hint_en": "Enable infinite time!"},
    "speedrun": {"name_ru": "Спидран", "name_en": "Speedrun", "desc_ru": "Победить до 5 за 20 секунд",
                 "desc_en": "Win to 5 in 20 sec", "hint_ru": "Каждая секунда на счету!",
                 "hint_en": "Every second counts!"},
    "god_mode": {"name_ru": "Бог понга", "name_en": "Pong God", "desc_ru": "Открыть 15 достижений",
                 "desc_en": "Unlock 15 achievements", "hint_ru": "Продолжай играть!", "hint_en": "Keep playing!"},
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