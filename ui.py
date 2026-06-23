import pygame
import random
import sys
from config import (WIDTH, HEIGHT, YELLOW, WHITE, ORANGE, RED,
                    THEMES, DIFFICULTY_SETTINGS, ROUND_TIMES, TARGET_SCORES,
                    BALL_COLORS, SETTINGS_FILE)
from game import Game
from achievements import Achievements


class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self._load_settings()
        self.achievements = Achievements()
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 36)
        self.font_btn = pygame.font.SysFont("Arial", 34)
        self.font_small = pygame.font.SysFont("Arial", 26)
        self.font_tiny = pygame.font.SysFont("Arial", 18)
        self.font_rules = pygame.font.SysFont("Arial", 30)
        self.font_rules_small = pygame.font.SysFont("Arial", 24)
        self.font_achieve = pygame.font.SysFont("Arial", 26)
        self.font_arrows = pygame.font.SysFont("Arial", 28)
        self.font_scroll = pygame.font.SysFont("Arial", 40)

        self.bg_balls = []
        for _ in range(25):
            self.bg_balls.append({
                "x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT),
                "vx": random.uniform(0.3, 1.5) * random.choice((1, -1)),
                "vy": random.uniform(0.3, 1.5) * random.choice((1, -1)),
                "size": random.randint(6, 16),
                "color": random.choice([(30, 30, 60), (40, 40, 70), (25, 25, 55), (35, 35, 80)]),
            })

        self.time_trans = {
            "15 секунд": "15 seconds", "30 секунд": "30 seconds",
            "1 минута": "1 minute", "1.5 минуты": "1.5 minutes", "2 минуты": "2 minutes",
            "3 минуты": "3 minutes", "5 минут": "5 minutes", "10 минут": "10 minutes",
            "Бесконечно": "Infinity"
        }
        self.score_trans = {
            "До 2": "To 2", "До 5": "To 5", "До 10": "To 10",
            "До 20": "To 20", "До 30": "To 30", "До 50": "To 50",
            "До 80": "To 80", "До 100": "To 100", "Бесконечно": "Infinity"
        }
        self.theme_trans = {
            "Зелёный": "Green", "Синий": "Blue", "Красный": "Red",
            "Фиолетовый": "Purple", "Золотой": "Gold"
        }
        self.ball_trans = {
            "Белый": "White", "Жёлтый": "Yellow", "Оранжевый": "Orange"
        }
        self.score_info = {
            "До 2": "2 гола", "До 5": "5 голов", "До 10": "10 голов",
            "До 20": "20 голов", "До 30": "30 голов", "До 50": "50 голов",
            "До 80": "80 голов", "До 100": "100 голов", "Бесконечно": "∞"
        }
        self.score_info_en = {
            "До 2": "2 goals", "До 5": "5 goals", "До 10": "10 goals",
            "До 20": "20 goals", "До 30": "30 goals", "До 50": "50 goals",
            "До 80": "80 goals", "До 100": "100 goals", "Бесконечно": "∞"
        }

    def _update_bg(self):
        for b in self.bg_balls:
            b["x"] += b["vx"];
            b["y"] += b["vy"]
            if b["x"] < 0 or b["x"] > WIDTH: b["vx"] = -b["vx"]
            if b["y"] < 0 or b["y"] > HEIGHT: b["vy"] = -b["vy"]

    def _draw_bg(self):
        self._update_bg()
        self.screen.fill((10, 10, 25))
        for b in self.bg_balls:
            pygame.draw.circle(self.screen, b["color"], (int(b["x"]), int(b["y"])), b["size"])

    def _refresh_achievements(self):
        self.achievements.load()

    def _load_settings(self):
        self.difficulty = "normal";
        self.theme = "green"
        self.music_volume = 0.5;
        self.sfx_volume = 0.7
        self.round_time = "1.5 минуты";
        self.target_score = "До 5"
        self.ball_color = "Белый";
        self.language = "ru"
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    k, v = line.strip().split("=")
                    if k == "difficulty":
                        self.difficulty = v
                    elif k == "theme":
                        self.theme = v
                    elif k == "music_volume":
                        self.music_volume = float(v)
                    elif k == "sfx_volume":
                        self.sfx_volume = float(v)
                    elif k == "round_time":
                        self.round_time = v
                    elif k == "target_score":
                        self.target_score = v
                    elif k == "ball_color":
                        self.ball_color = v
                    elif k == "language":
                        self.language = v
        except:
            pass

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                f.write(f"difficulty={self.difficulty}\n");
                f.write(f"theme={self.theme}\n")
                f.write(f"music_volume={self.music_volume}\n");
                f.write(f"sfx_volume={self.sfx_volume}\n")
                f.write(f"round_time={self.round_time}\n");
                f.write(f"target_score={self.target_score}\n")
                f.write(f"ball_color={self.ball_color}\n");
                f.write(f"language={self.language}\n")
        except:
            pass

    def L(self, ru, en):
        return ru if self.language == "ru" else en

    def TV(self, value, trans_dict):
        if self.language == "ru": return value
        return trans_dict.get(value, value)

    def _draw_button(self, text, rect, hover=False, color=WHITE, small=False):
        font = self.font_small if small else self.font_btn
        if hover:
            pygame.draw.rect(self.screen, (35, 35, 65), rect, border_radius=12)
            pygame.draw.rect(self.screen, YELLOW, rect, 3, border_radius=12)
            c = YELLOW
        else:
            pygame.draw.rect(self.screen, (18, 18, 38), rect, border_radius=12)
            pygame.draw.rect(self.screen, (55, 55, 95), rect, 2, border_radius=12)
            c = color
        surf = font.render(text, True, c)
        self.screen.blit(surf, (rect.centerx - surf.get_width() // 2, rect.centery - surf.get_height() // 2))

    def _draw_setting_box(self, rect, text, value, mx, my, color=YELLOW):
        pygame.draw.rect(self.screen, (25, 25, 45), rect, border_radius=8)
        pygame.draw.rect(self.screen, (60, 60, 100), rect, 2, border_radius=8)

        l_rect = pygame.Rect(rect.left + 5, rect.centery - 14, 28, 28)
        l_hover = l_rect.collidepoint(mx, my)
        lc = YELLOW if l_hover else (120, 120, 160)
        ls = self.font_arrows.render("◄", True, lc)
        self.screen.blit(ls, (l_rect.centerx - ls.get_width() // 2, l_rect.centery - ls.get_height() // 2))

        s = self.font_small.render(f"{text}  {value}", True, color)
        self.screen.blit(s, (rect.centerx - s.get_width() // 2, rect.centery - s.get_height() // 2))

        r_rect = pygame.Rect(rect.right - 33, rect.centery - 14, 28, 28)
        r_hover = r_rect.collidepoint(mx, my)
        rc = YELLOW if r_hover else (120, 120, 160)
        rs = self.font_arrows.render("►", True, rc)
        self.screen.blit(rs, (r_rect.centerx - rs.get_width() // 2, r_rect.centery - rs.get_height() // 2))

        if l_hover: return "left"
        if r_hover: return "right"
        return None

    def _draw_scroll_buttons(self, up_btn, down_btn, mx, my):
        up_hover = up_btn.collidepoint(mx, my)
        uc = YELLOW if up_hover else (120, 120, 160)
        us = self.font_scroll.render("▲", True, uc)
        self.screen.blit(us, (up_btn.centerx - us.get_width() // 2, up_btn.centery - us.get_height() // 2))

        down_hover = down_btn.collidepoint(mx, my)
        dc = YELLOW if down_hover else (120, 120, 160)
        ds = self.font_scroll.render("▼", True, dc)
        self.screen.blit(ds, (down_btn.centerx - ds.get_width() // 2, down_btn.centery - ds.get_height() // 2))

        if up_hover: return "up"
        if down_hover: return "down"
        return None

    def _draw_title(self, text, y=40):
        surf = self.font_title.render(text, True, YELLOW)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

    def _draw_subtitle(self, text, y, color=(255, 100, 100)):
        surf = self.font_subtitle.render(text, True, color)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

    def show_main_menu(self):
        btns = [
            ("play", pygame.Rect(WIDTH // 2 - 180, 170, 360, 60), self.L("ИГРАТЬ", "PLAY"), WHITE),
            ("ach", pygame.Rect(WIDTH // 2 - 180, 250, 360, 60), self.L("ДОСТИЖЕНИЯ", "ACHIEVEMENTS"), WHITE),
            ("rules", pygame.Rect(WIDTH // 2 - 180, 330, 360, 60), self.L("ПРАВИЛА", "RULES"), WHITE),
            ("sett", pygame.Rect(WIDTH // 2 - 180, 410, 360, 60), self.L("НАСТРОЙКИ", "SETTINGS"), WHITE),
            ("exit", pygame.Rect(WIDTH // 2 - 180, 490, 360, 60), self.L("ВЫХОД", "EXIT"), (255, 120, 120)),
        ]
        while True:
            mx, my = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    for bid, r, _, _ in btns:
                        if r.collidepoint(mx, my):
                            if bid == "play":
                                self.show_mode_select()
                            elif bid == "ach":
                                self.show_achievements()
                            elif bid == "rules":
                                self.show_rules()
                            elif bid == "sett":
                                self.show_settings()
                            elif bid == "exit":
                                pygame.quit(); sys.exit()
            self._draw_bg();
            self._draw_title("PONG 2D")
            for bid, r, t, c in btns:
                self._draw_button(t, r, r.collidepoint(mx, my), c)
            ver_font = pygame.font.SysFont("Arial", 16, italic=True)
            if self.language == "ru":
                ver_text = ver_font.render("Версия 1.0 | Разработчик: Artox | Платформа: Python | Спасибо, что играете!", True, (180, 180, 200))
            else:
                ver_text = ver_font.render("Version 1.0 | Developer: Artox | Platform: Python | Thanks for playing!", True, (180, 180, 200))
            self.screen.blit(ver_text, (WIDTH // 2 - ver_text.get_width() // 2, HEIGHT - 22))
            pygame.display.flip();
            self.clock.tick(60)

    def show_achievements(self):
        self._refresh_achievements()
        all_a = self.achievements.get_all()
        uc = sum(1 for _, _, u in all_a if u)
        scroll = 0;
        per = 10;
        max_scroll = max(0, len(all_a) - per)

        panel_x = WIDTH - 55;
        btn_size = 50
        up_btn = pygame.Rect(panel_x, 100, btn_size, btn_size)
        down_btn = pygame.Rect(panel_x, HEIGHT - 150, btn_size, btn_size)
        back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 75, 200, 45)

        while True:
            mx, my = pygame.mouse.get_pos()
            scroll_action = self._draw_scroll_buttons(up_btn, down_btn, mx, my)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 4:
                        scroll = max(scroll - 1, 0)
                    elif ev.button == 5:
                        scroll = min(scroll + 1, max_scroll)
                    elif ev.button == 1:
                        if back_btn.collidepoint(mx, my): return
                        if scroll_action == "up":
                            scroll = max(scroll - 1, 0)
                        elif scroll_action == "down":
                            scroll = min(scroll + 1, max_scroll)

            self._draw_bg()
            self._draw_title(self.L("ДОСТИЖЕНИЯ", "ACHIEVEMENTS"))
            txt = self.L(f"Открыто: {uc}/{len(all_a)}", f"Unlocked: {uc}/{len(all_a)}")
            s = self.font_small.render(txt, True, YELLOW)
            self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, 110))

            y = 155
            for i in range(scroll, min(scroll + per, len(all_a))):
                _, info, unlocked = all_a[i]
                if unlocked:
                    t = f"{info['name_' + self.language]} — {info['desc_' + self.language]}"
                    c = WHITE
                else:
                    t = f"??? — {self.L('Подсказка', 'Hint')}: {info['hint_' + self.language]}"
                    c = (120, 120, 120)
                s = self.font_achieve.render(t, True, c)
                self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, y))
                y += 36

            self._draw_scroll_buttons(up_btn, down_btn, mx, my)
            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), color=(255, 100, 100), small=True)
            pygame.display.flip();
            self.clock.tick(60)

    def show_mode_select(self):
        btns = [
            ("pve", pygame.Rect(WIDTH // 2 - 250, 160, 500, 65), self.L("ИГРОК vs КОМПЬЮТЕР", "PLAYER vs COMPUTER"),
             WHITE),
            ("pvp", pygame.Rect(WIDTH // 2 - 250, 260, 500, 65), self.L("ИГРОК vs ИГРОК", "PLAYER vs PLAYER"), WHITE),
            ("back", pygame.Rect(WIDTH // 2 - 250, 420, 500, 65), self.L("НАЗАД", "BACK"), (255, 100, 100)),
        ]
        while True:
            mx, my = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    for bid, r, _, _ in btns:
                        if r.collidepoint(mx, my):
                            if bid == "pve":
                                self.show_pve_setup()
                            elif bid == "pvp":
                                self.show_pvp_setup()
                            elif bid == "back":
                                return
            self._draw_bg();
            self._draw_title(self.L("РЕЖИМ ИГРЫ", "GAME MODE"))
            c1 = self.L("W / S — управление", "W / S — control")
            c2 = self.L("Левый: W/S | Правый: Стрелки ВВЕРХ/ВНИЗ", "Left: W/S | Right: ARROWS UP/DOWN")
            s1 = self.font_tiny.render(c1, True, (180, 180, 200));
            s2 = self.font_tiny.render(c2, True, (180, 180, 200))
            self.screen.blit(s1, (WIDTH // 2 - s1.get_width() // 2, 232));
            self.screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, 332))
            for bid, r, t, c in btns:
                self._draw_button(t, r, r.collidepoint(mx, my), c)
            pygame.display.flip();
            self.clock.tick(60)

    def show_pve_setup(self):
        dnames = list(DIFFICULTY_SETTINGS.keys())
        tnames = list(ROUND_TIMES.keys())
        thnames = list(THEMES.keys())
        bnames = list(BALL_COLORS.keys())
        snames = list(TARGET_SCORES.keys())

        box_w = 300
        col_left_x = WIDTH // 2 - box_w - 20
        col_right_x = WIDTH // 2 + 20

        diff_left = [
            pygame.Rect(col_left_x, 120, box_w, 70),  # Лёгкая
            pygame.Rect(col_left_x, 200, box_w, 70),  # Нормальная
        ]
        diff_right = [
            pygame.Rect(col_right_x, 120, box_w, 70),  # Сложная
            pygame.Rect(col_right_x, 200, box_w, 70),  # Хардкор
        ]

        set_w = 500
        t_rect = pygame.Rect(WIDTH // 2 - set_w // 2, 295, set_w, 38)
        s_rect = pygame.Rect(WIDTH // 2 - set_w // 2, 343, set_w, 38)
        th_rect = pygame.Rect(WIDTH // 2 - set_w // 2, 391, set_w, 38)
        b_rect = pygame.Rect(WIDTH // 2 - set_w // 2, 439, set_w, 38)

        back_btn = pygame.Rect(WIDTH // 2 - 260, 495, 240, 60)
        start_btn = pygame.Rect(WIDTH // 2 + 20, 495, 240, 60)

        desc1 = {
            "easy": self.L("Медленный ИИ, часто ошибается", "Slow AI, often mistakes"),
            "normal": self.L("Средняя скорость, редко ошибается", "Medium speed, rarely mistakes"),
            "hard": self.L("Быстрый, предугадывает траекторию", "Fast, predicts trajectory"),
            "hardcore": self.L("Максимальная скорость, без шансов", "Maximum speed, no chance")
        }
        desc2 = {
            "easy": self.L("Мяч медленно ускоряется", "Ball accelerates slowly"),
            "normal": self.L("Мяч нормально ускоряется", "Ball accelerates normally"),
            "hard": self.L("Мяч быстро ускоряется", "Ball accelerates fast"),
            "hardcore": self.L("Мяч очень быстро ускоряется", "Ball accelerates very fast")
        }
        dcol = {"easy": (100, 255, 100), "normal": (255, 255, 100), "hard": ORANGE, "hardcore": RED}

        while True:
            mx, my = pygame.mouse.get_pos()

            self._draw_bg()
            self._draw_title(self.L("ИГРА С КОМПЬЮТЕРОМ", "PLAYER vs COMPUTER"), 1)
            dn = DIFFICULTY_SETTINGS[self.difficulty]['name_' + self.language].upper()
            self._draw_subtitle(self.L(f"СЛОЖНОСТЬ: {dn}", f"DIFFICULTY: {dn}"), 65, dcol[self.difficulty])

            # Левая колонка (Лёгкая, Нормальная)
            for i, diff in enumerate(dnames[:2]):
                r = diff_left[i]
                selected = (self.difficulty == diff)
                if selected:
                    pygame.draw.rect(self.screen, (25, 25, 45), r, border_radius=8)
                    pygame.draw.rect(self.screen, dcol[diff], r, 3, border_radius=8)
                else:
                    pygame.draw.rect(self.screen, (25, 25, 45), r, border_radius=8)
                    pygame.draw.rect(self.screen, (60, 60, 100), r, 2, border_radius=8)
                name_s = self.font_small.render(DIFFICULTY_SETTINGS[diff]["name_" + self.language], True, dcol[diff])
                d1_s = self.font_tiny.render(desc1[diff], True, (180, 180, 200))
                d2_s = self.font_tiny.render(desc2[diff], True, (150, 150, 170))
                self.screen.blit(name_s, (r.centerx - name_s.get_width() // 2, r.y + 3))
                self.screen.blit(d1_s, (r.centerx - d1_s.get_width() // 2, r.y + 26))
                self.screen.blit(d2_s, (r.centerx - d2_s.get_width() // 2, r.y + 46))

            # Правая колонка (Сложная, Хардкор)
            for i, diff in enumerate(dnames[2:]):
                r = diff_right[i]
                selected = (self.difficulty == diff)
                if selected:
                    pygame.draw.rect(self.screen, (25, 25, 45), r, border_radius=8)
                    pygame.draw.rect(self.screen, dcol[diff], r, 3, border_radius=8)
                else:
                    pygame.draw.rect(self.screen, (25, 25, 45), r, border_radius=8)
                    pygame.draw.rect(self.screen, (60, 60, 100), r, 2, border_radius=8)
                name_s = self.font_small.render(DIFFICULTY_SETTINGS[diff]["name_" + self.language], True, dcol[diff])
                d1_s = self.font_tiny.render(desc1[diff], True, (180, 180, 200))
                d2_s = self.font_tiny.render(desc2[diff], True, (150, 150, 170))
                self.screen.blit(name_s, (r.centerx - name_s.get_width() // 2, r.y + 3))
                self.screen.blit(d1_s, (r.centerx - d1_s.get_width() // 2, r.y + 26))
                self.screen.blit(d2_s, (r.centerx - d2_s.get_width() // 2, r.y + 46))

            time_val = self.TV(self.round_time, self.time_trans)
            score_val = self.TV(self.target_score, self.score_trans)
            theme_val = self.TV(THEMES[self.theme]["name"], self.theme_trans)
            ball_val = self.TV(self.ball_color, self.ball_trans)

            info = self.score_info if self.language == "ru" else self.score_info_en
            s_val = f"{score_val} ({info.get(self.target_score, '')})"

            self._draw_setting_box(t_rect, self.L("Время раунда:", "Round time:"), time_val, mx, my)
            self._draw_setting_box(s_rect, self.L("Игра до:", "Play to:"), s_val, mx, my)
            self._draw_setting_box(th_rect, self.L("Тема стола:", "Table theme:"), theme_val, mx, my)
            self._draw_setting_box(b_rect, self.L("Цвет мяча:", "Ball color:"), ball_val, mx, my)

            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), (255, 100, 100))
            self._draw_button(self.L("СТАРТ", "START"), start_btn, start_btn.collidepoint(mx, my), (100, 255, 100))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE: return
                    if ev.key == pygame.K_SPACE:
                        self._save_settings()
                        result = Game(self.screen, self.difficulty, self.theme, self.music_volume, self.sfx_volume,
                                      "pve", self.round_time, self.target_score, self.ball_color, self.language).run()
                        if result == "exit": pygame.quit(); sys.exit()
                        if result == "back":
                            pass
                        else:
                            self.show_main_menu()
                            return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    for i, r in enumerate(diff_left):
                        if r.collidepoint(mx, my): self.difficulty = dnames[i]
                    for i, r in enumerate(diff_right):
                        if r.collidepoint(mx, my): self.difficulty = dnames[i + 2]

                    for rect, names, attr in [(t_rect, tnames, 'round_time'), (s_rect, snames, 'target_score'),
                                              (th_rect, thnames, 'theme'), (b_rect, bnames, 'ball_color')]:
                        lr = pygame.Rect(rect.left + 5, rect.centery - 14, 28, 28)
                        rr = pygame.Rect(rect.right - 33, rect.centery - 14, 28, 28)
                        cur = getattr(self, attr)
                        if lr.collidepoint(mx, my):
                            idx = (names.index(cur) - 1) % len(names)
                            setattr(self, attr, names[idx])
                        elif rr.collidepoint(mx, my):
                            idx = (names.index(cur) + 1) % len(names)
                            setattr(self, attr, names[idx])

                    if back_btn.collidepoint(mx, my): return
                    if start_btn.collidepoint(mx, my):
                        self._save_settings()
                        result = Game(self.screen, self.difficulty, self.theme, self.music_volume, self.sfx_volume,
                                      "pve", self.round_time, self.target_score, self.ball_color, self.language).run()
                        if result == "exit": pygame.quit(); sys.exit()
                        if result == "back":
                            pass
                        else:
                            self.show_main_menu()
                            return

            pygame.display.flip()
            self.clock.tick(60)

    def show_pvp_setup(self):
        tnames = list(ROUND_TIMES.keys());
        thnames = list(THEMES.keys())
        bnames = list(BALL_COLORS.keys());
        snames = list(TARGET_SCORES.keys())

        box_w = 460;
        arrow_w = 35;
        arrow_gap = 25

        t_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 220, box_w, 38)
        t_left = pygame.Rect(t_rect.centerx - arrow_w - box_w // 2 - arrow_gap, t_rect.centery - 19, arrow_w, 38)
        t_right = pygame.Rect(t_rect.centerx + box_w // 2 + arrow_gap, t_rect.centery - 19, arrow_w, 38)

        s_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 270, box_w, 38)
        s_left = pygame.Rect(s_rect.centerx - arrow_w - box_w // 2 - arrow_gap, s_rect.centery - 19, arrow_w, 38)
        s_right = pygame.Rect(s_rect.centerx + box_w // 2 + arrow_gap, s_rect.centery - 19, arrow_w, 38)

        th_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 320, box_w, 38)
        th_left = pygame.Rect(th_rect.centerx - arrow_w - box_w // 2 - arrow_gap, th_rect.centery - 19, arrow_w, 38)
        th_right = pygame.Rect(th_rect.centerx + box_w // 2 + arrow_gap, th_rect.centery - 19, arrow_w, 38)

        b_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 370, box_w, 38)
        b_left = pygame.Rect(b_rect.centerx - arrow_w - box_w // 2 - arrow_gap, b_rect.centery - 19, arrow_w, 38)
        b_right = pygame.Rect(b_rect.centerx + box_w // 2 + arrow_gap, b_rect.centery - 19, arrow_w, 38)

        start_btn = pygame.Rect(WIDTH // 2 - 180, 450, 360, 55)
        back_btn = pygame.Rect(WIDTH // 2 - 180, 520, 360, 55)

        while True:
            mx, my = pygame.mouse.get_pos()

            self._draw_bg()
            self._draw_title(self.L("ИГРОК ПРОТИВ ИГРОКА", "PLAYER vs PLAYER"))
            c = self.L("Левый: W/S | Правый: Стрелки ВВЕРХ/ВНИЗ", "Left: W/S | Right: ARROWS UP/DOWN")
            s = self.font_small.render(c, True, (180, 180, 200))
            self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, 130))

            time_val = self.TV(self.round_time, self.time_trans)
            score_val = self.TV(self.target_score, self.score_trans)
            theme_val = self.TV(THEMES[self.theme]["name"], self.theme_trans)
            ball_val = self.TV(self.ball_color, self.ball_trans)

            info = self.score_info if self.language == "ru" else self.score_info_en
            s_val = f"{score_val} ({info.get(self.target_score, '')})"

            t_action = self._draw_setting_box(t_rect, self.L("Время раунда:", "Round time:"), time_val, mx, my)
            s_action = self._draw_setting_box(s_rect, self.L("Игра до:", "Play to:"), s_val, mx, my)
            th_action = self._draw_setting_box(th_rect, self.L("Тема стола:", "Table theme:"), theme_val, mx, my)
            b_action = self._draw_setting_box(b_rect, self.L("Цвет мяча:", "Ball color:"), ball_val, mx, my)
            self._draw_button(self.L("СТАРТ", "START"), start_btn, start_btn.collidepoint(mx, my), (100, 255, 100))
            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), (255, 100, 100))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE: return
                    if ev.key == pygame.K_SPACE:
                        self._save_settings()
                        result = Game(self.screen, "normal", self.theme, self.music_volume, self.sfx_volume,
                                      "pvp", self.round_time, self.target_score, self.ball_color, self.language).run()
                        if result == "exit": pygame.quit(); sys.exit()
                        if result == "back":
                            pass
                        else:
                            self.show_main_menu()
                            return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if t_action == "left":
                        idx = (tnames.index(self.round_time) - 1) % len(tnames);
                        self.round_time = tnames[idx]
                    elif t_action == "right":
                        idx = (tnames.index(self.round_time) + 1) % len(tnames);
                        self.round_time = tnames[idx]
                    elif s_action == "left":
                        idx = (snames.index(self.target_score) - 1) % len(snames);
                        self.target_score = snames[idx]
                    elif s_action == "right":
                        idx = (snames.index(self.target_score) + 1) % len(snames);
                        self.target_score = snames[idx]
                    elif th_action == "left":
                        idx = (thnames.index(self.theme) - 1) % len(thnames);
                        self.theme = thnames[idx]
                    elif th_action == "right":
                        idx = (thnames.index(self.theme) + 1) % len(thnames);
                        self.theme = thnames[idx]
                    elif b_action == "left":
                        idx = (bnames.index(self.ball_color) - 1) % len(bnames);
                        self.ball_color = bnames[idx]
                    elif b_action == "right":
                        idx = (bnames.index(self.ball_color) + 1) % len(bnames);
                        self.ball_color = bnames[idx]
                    elif start_btn.collidepoint(mx, my):
                        self._save_settings()
                        result = Game(self.screen, "normal", self.theme, self.music_volume, self.sfx_volume,
                                      "pvp", self.round_time, self.target_score, self.ball_color, self.language).run()
                        if result == "exit": pygame.quit(); sys.exit()
                        if result == "back":
                            pass
                        else:
                            self.show_main_menu()
                            return
                    elif back_btn.collidepoint(mx, my):
                        return

            pygame.display.flip()
            self.clock.tick(60)

    def show_rules(self):
        rules = [
            (self.L("ОБ ИГРЕ", "ABOUT"), True),
            (self.L("ПОНГ — классическая аркадная игра.", "PONG — classic arcade game."), False),
            (self.L("Отбивай мяч ракеткой и забивай голы!", "Hit the ball and score goals!"), False),
            (self.L("Играй против ИИ или с другом.", "Play vs AI or a friend."), False),
            ("", False),
            (self.L("РЕЖИМЫ ИГРЫ", "GAME MODES"), True),
            (self.L("Игрок vs Компьютер — вы против ИИ", "Player vs Computer — you vs AI"), False),
            (self.L("  W / S — движение ракетки вверх/вниз", "  W / S — move paddle up/down"), False),
            (self.L("  Выбор сложности, времени и голов", "  Difficulty, time and score settings"), False),
            ("", False),
            (self.L("Игрок vs Игрок — игра вдвоём", "Player vs Player — local multiplayer"), False),
            (self.L("  Левый: W / S    Правый: Стрелки ВВЕРХ / ВНИЗ", "  Left: W / S    Right: ARROWS UP / DOWN"),
             False),
            ("", False),
            (self.L("ЦЕЛЬ ИГРЫ", "GOAL"), True),
            (self.L("Забить мяч в ворота соперника", "Score in opponent's goal"), False),
            (self.L("Ворота — затемнённые зоны по бокам", "Goals — dark zones on sides"), False),
            ("", False),
            (self.L("МЕХАНИКИ", "MECHANICS"), True),
            (self.L("В начале мяч летит в случайную сторону", "Ball starts in random direction"), False),
            (self.L("Мяч ускоряется, если долго нет гола", "Ball speeds up without goals"), False),
            (self.L("После гола — медленная подача пропустившему", "After goal — slow serve to conceding side"), False),
            (self.L("Угол отскока зависит от места удара", "Bounce angle depends on hit position"), False),
            (self.L("Время вышло + равный счёт = НИЧЬЯ", "Time up + equal score = DRAW"), False),
            ("", False),
            (self.L("УПРАВЛЕНИЕ", "CONTROLS"), True),
            (self.L("ESC — пауза", "ESC — pause"), False),
            (self.L("В паузе: ESC — продолжить, M — меню", "Pause: ESC — continue, M — menu"), False),
            ("", False),
            (self.L("ПОСЛЕ ИГРЫ", "AFTER GAME"), True),
            (self.L("ПРОБЕЛ — вернуться к настройкам", "SPACE — return to settings"), False),
            (self.L("TAB — статистика матча", "TAB — match statistics"), False),
            (self.L("ESC — выйти в главное меню", "ESC — return to main menu"), False),
        ]
        scroll = 0;
        per = 16;
        max_scroll = max(0, len(rules) - per)

        panel_x = WIDTH - 55;
        btn_size = 50
        up_btn = pygame.Rect(panel_x, 100, btn_size, btn_size)
        down_btn = pygame.Rect(panel_x, HEIGHT - 150, btn_size, btn_size)
        back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 75, 200, 45)

        while True:
            mx, my = pygame.mouse.get_pos()
            scroll_action = self._draw_scroll_buttons(up_btn, down_btn, mx, my)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 4:
                        scroll = max(scroll - 1, 0)
                    elif ev.button == 5:
                        scroll = min(scroll + 1, max_scroll)
                    elif ev.button == 1:
                        if back_btn.collidepoint(mx, my): return
                        if scroll_action == "up":
                            scroll = max(scroll - 1, 0)
                        elif scroll_action == "down":
                            scroll = min(scroll + 1, max_scroll)

            self._draw_bg();
            self._draw_title(self.L("ПРАВИЛА", "RULES"))
            y = 115
            for i in range(scroll, min(scroll + per, len(rules))):
                text, is_title = rules[i]
                if text:
                    s = (self.font_rules if is_title else self.font_rules_small).render(text, True,
                                                                                        YELLOW if is_title else (
                                                                                            WHITE if not text.startswith(
                                                                                                "  ") else (
                                                                                            180, 180, 200)))
                    self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, y))
                    y += 36 if is_title else 26
                else:
                    y += 6

            self._draw_scroll_buttons(up_btn, down_btn, mx, my)
            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), color=(255, 100, 100), small=True)
            pygame.display.flip()
            self.clock.tick(60)

    def show_settings(self):
        lang_label_y = 130
        lang_ru_btn = pygame.Rect(WIDTH // 2 - 260, 180, 240, 50)
        lang_en_btn = pygame.Rect(WIDTH // 2 + 20, 180, 240, 50)

        music_rect = pygame.Rect(WIDTH // 2 - 200, 270, 400, 40)
        sfx_rect = pygame.Rect(WIDTH // 2 - 200, 370, 400, 40)
        back_btn = pygame.Rect(WIDTH // 2 - 100, 470, 200, 50)

        while True:
            mx, my = pygame.mouse.get_pos()
            self._draw_bg();
            self._draw_title(self.L("НАСТРОЙКИ", "SETTINGS"))

            lang_label = self.font_subtitle.render(self.L("Языки:", "Languages:"), True, YELLOW)
            self.screen.blit(lang_label, (WIDTH // 2 - lang_label.get_width() // 2, lang_label_y))

            ru_color = YELLOW if self.language == "ru" else WHITE
            en_color = YELLOW if self.language == "en" else WHITE
            self._draw_button("РУССКИЙ", lang_ru_btn, lang_ru_btn.collidepoint(mx, my), ru_color, small=True)
            self._draw_button("ENGLISH", lang_en_btn, lang_en_btn.collidepoint(mx, my), en_color, small=True)

            ms = self.font_small.render(
                self.L(f"Музыка: {int(self.music_volume * 100)}%", f"Music: {int(self.music_volume * 100)}%"), True, YELLOW)
            self.screen.blit(ms, (WIDTH // 2 - ms.get_width() // 2, 275))
            pygame.draw.rect(self.screen, (60, 60, 100), (WIDTH // 2 - 150, 315, 300, 8), border_radius=4)
            pygame.draw.rect(self.screen, YELLOW, (WIDTH // 2 - 150, 315, int(300 * self.music_volume), 8),
                             border_radius=4)

            sf = self.font_small.render(
                self.L(f"Звуки: {int(self.sfx_volume * 100)}%", f"Sound: {int(self.sfx_volume * 100)}%"), True, YELLOW)
            self.screen.blit(sf, (WIDTH // 2 - sf.get_width() // 2, 375))
            pygame.draw.rect(self.screen, (60, 60, 100), (WIDTH // 2 - 150, 415, 300, 8), border_radius=4)
            pygame.draw.rect(self.screen, YELLOW, (WIDTH // 2 - 150, 415, int(300 * self.sfx_volume), 8),
                             border_radius=4)

            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), color=(255, 100, 100), small=True)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self._save_settings()
                        self.show_main_menu()
                        return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if lang_ru_btn.collidepoint(mx, my):
                        self.language = "ru"
                    elif lang_en_btn.collidepoint(mx, my):
                        self.language = "en"
                    elif back_btn.collidepoint(mx, my):
                        self._save_settings()
                        self.show_main_menu()
                        return

                if pygame.mouse.get_pressed()[0]:
                    if pygame.Rect(WIDTH // 2 - 150, 305, 300, 20).collidepoint(mx, my):
                        self.music_volume = (mx - (WIDTH // 2 - 150)) / 300
                        self.music_volume = max(0, min(1, self.music_volume))
                        try:
                            pygame.mixer.music.set_volume(self.music_volume)
                        except:
                            pass
                    if pygame.Rect(WIDTH // 2 - 150, 405, 300, 20).collidepoint(mx, my):
                        self.sfx_volume = (mx - (WIDTH // 2 - 150)) / 300
                        self.sfx_volume = max(0, min(1, self.sfx_volume))

            pygame.display.flip()
            self.clock.tick(60)