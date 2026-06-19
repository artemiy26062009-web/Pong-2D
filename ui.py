import pygame
import random
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

        self.bg_balls = []
        for _ in range(20):
            self.bg_balls.append({
                "x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT),
                "vx": random.uniform(-1.5, 1.5), "vy": random.uniform(-1.5, 1.5),
                "size": random.randint(6, 16),
                "color": random.choice([(30, 30, 60), (40, 40, 70), (25, 25, 55), (35, 35, 80)]),
            })

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
        """
        Рисует оболочку настройки со стрелками ◄ ► внутри.
        Возвращает: "left" если мышь над левой стрелкой, "right" если над правой, иначе None
        """
        pygame.draw.rect(self.screen, (25, 25, 45), rect, border_radius=8)
        pygame.draw.rect(self.screen, (60, 60, 100), rect, 2, border_radius=8)

        # Левая стрелка ◄
        l_rect = pygame.Rect(rect.left + 5, rect.centery - 14, 28, 28)
        l_hover = l_rect.collidepoint(mx, my)
        l_color = YELLOW if l_hover else (120, 120, 160)
        l_surf = self.font_arrows.render("◄", True, l_color)
        self.screen.blit(l_surf, (l_rect.centerx - l_surf.get_width() // 2, l_rect.centery - l_surf.get_height() // 2))

        # Текст по центру
        s = self.font_small.render(f"{text}  {value}", True, color)
        self.screen.blit(s, (rect.centerx - s.get_width() // 2, rect.centery - s.get_height() // 2))

        # Правая стрелка ►
        r_rect = pygame.Rect(rect.right - 33, rect.centery - 14, 28, 28)
        r_hover = r_rect.collidepoint(mx, my)
        r_color = YELLOW if r_hover else (120, 120, 160)
        r_surf = self.font_arrows.render("►", True, r_color)
        self.screen.blit(r_surf, (r_rect.centerx - r_surf.get_width() // 2, r_rect.centery - r_surf.get_height() // 2))

        # Возвращаем что нажато
        if l_hover: return "left"
        if r_hover: return "right"
        return None

    def _draw_scroll_arrows(self, up_rect, down_rect, mx, my):
        self._draw_button("▲", up_rect, up_rect.collidepoint(mx, my), YELLOW, True)
        self._draw_button("▼", down_rect, down_rect.collidepoint(mx, my), YELLOW, True)

    def _draw_title(self, text, y=40):
        surf = self.font_title.render(text, True, YELLOW)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

    def _draw_subtitle(self, text, y, color=(255, 100, 100)):
        surf = self.font_subtitle.render(text, True, color)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

    # ========================= ГЛАВНОЕ МЕНЮ =========================
    def show_main_menu(self):
        btns = [
            ("play", pygame.Rect(WIDTH // 2 - 180, 170, 360, 60), self.L("ИГРАТЬ", "PLAY"), WHITE),
            ("ach", pygame.Rect(WIDTH // 2 - 180, 250, 360, 60), self.L("ДОСТИЖЕНИЯ", "ACHIEVEMENTS"), WHITE),
            ("rules", pygame.Rect(WIDTH // 2 - 180, 330, 360, 60), self.L("ПРАВИЛА", "RULES"), WHITE),
            ("sett", pygame.Rect(WIDTH // 2 - 180, 410, 360, 60), self.L("НАСТРОЙКИ", "SETTINGS"), WHITE),
            ("exit", pygame.Rect(WIDTH // 2 - 180, 490, 360, 60), self.L("ВЫХОД", "EXIT"), (255, 120, 120)),
        ]

        def draw():
            self._draw_title("PONG 2D")

        while True:
            mx, my = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
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
                                return
            self._draw_bg();
            draw()
            for bid, r, t, c in btns:
                self._draw_button(t, r, r.collidepoint(mx, my), c)
            pygame.display.flip();
            self.clock.tick(60)

    # ========================= ДОСТИЖЕНИЯ =========================
    def show_achievements(self):
        self._refresh_achievements()
        all_a = self.achievements.get_all()
        uc = sum(1 for _, _, u in all_a if u)
        scroll = 0;
        per = 8;
        max_scroll = max(0, len(all_a) - per)
        margin = 80
        up_btn = pygame.Rect(WIDTH - 60, margin, 40, 40)
        down_btn = pygame.Rect(WIDTH - 60, HEIGHT - margin - 40, 40, 40)
        back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 45)

        while True:
            mx, my = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 4:
                        scroll = max(scroll - 1, 0)
                    elif ev.button == 5:
                        scroll = min(scroll + 1, max_scroll)
                    elif ev.button == 1:
                        if back_btn.collidepoint(mx, my): return
                        if up_btn.collidepoint(mx, my):
                            scroll = max(scroll - 1, 0)
                        elif down_btn.collidepoint(mx, my):
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

            self._draw_scroll_arrows(up_btn, down_btn, mx, my)
            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), small=True)
            pygame.display.flip();
            self.clock.tick(60)

    # ========================= ВЫБОР РЕЖИМА =========================
    def show_mode_select(self):
        btns = [
            ("pve", pygame.Rect(WIDTH // 2 - 250, 160, 500, 65), self.L("ИГРОК vs КОМПЬЮТЕР", "PLAYER vs COMPUTER"),
             WHITE),
            ("pvp", pygame.Rect(WIDTH // 2 - 250, 260, 500, 65), self.L("ИГРОК vs ИГРОК", "PLAYER vs PLAYER"), WHITE),
            ("back", pygame.Rect(WIDTH // 2 - 250, 420, 500, 65), self.L("НАЗАД", "BACK"), WHITE),
        ]

        def draw():
            self._draw_title(self.L("РЕЖИМ ИГРЫ", "GAME MODE"))
            c1 = self.L("W / S — управление", "W / S — control")
            c2 = self.L("Левый: W/S | Правый: Стрелки ВВЕРХ/ВНИЗ", "Left: W/S | Right: ARROWS UP/DOWN")
            s1 = self.font_tiny.render(c1, True, (180, 180, 200));
            s2 = self.font_tiny.render(c2, True, (180, 180, 200))
            self.screen.blit(s1, (WIDTH // 2 - s1.get_width() // 2, 232));
            self.screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, 332))

        while True:
            mx, my = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
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
            draw()
            for bid, r, t, c in btns:
                self._draw_button(t, r, r.collidepoint(mx, my), c)
            pygame.display.flip();
            self.clock.tick(60)

    # ========================= НАСТРОЙКА PvE =========================
    def show_pve_setup(self):
        dnames = list(DIFFICULTY_SETTINGS.keys())
        tnames = list(ROUND_TIMES.keys())
        thnames = list(THEMES.keys())
        bnames = list(BALL_COLORS.keys())
        snames = list(TARGET_SCORES.keys())

        scroll = 0;
        per = 4;
        max_scroll = max(0, len(dnames) - per)
        margin = 80
        up_btn = pygame.Rect(WIDTH - 60, margin, 40, 40)
        down_btn = pygame.Rect(WIDTH - 60, HEIGHT - margin - 40, 40, 40)

        box_w = 480

        diff_rects = [pygame.Rect(WIDTH // 2 - box_w // 2, 108 + i * 60, box_w, 50) for i in range(4)]

        # Оболочки настроек (без отдельных треугольников)
        t_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 368, box_w, 40)
        s_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 418, box_w, 40)
        th_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 468, box_w, 40)
        b_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 518, box_w, 40)

        start_btn = pygame.Rect(WIDTH // 2 - 180, 580, 360, 55)
        back_btn = pygame.Rect(WIDTH // 2 - 180, 645, 360, 55)

        desc = {
            "easy": self.L("Медленный ИИ, часто ошибается (мяч медленно ускоряется)", "Slow AI, often mistakes"),
            "normal": self.L("Средняя скорость, редко ошибается (мяч нормально ускоряется)",
                             "Medium speed, rarely mistakes"),
            "hard": self.L("Быстрый, предугадывает траекторию (мяч быстро ускоряется)", "Fast, predicts trajectory"),
            "hardcore": self.L("Максимальная скорость, без шансов (мяч очень быстро ускоряется)",
                               "Maximum speed, no chance")
        }
        dcol = {"easy": (100, 255, 100), "normal": (255, 255, 100), "hard": ORANGE, "hardcore": RED}

        def draw():
            self._draw_title(self.L("ИГРА С КОМПЬЮТЕРОМ", "PLAYER vs COMPUTER"), 1)
            dn = DIFFICULTY_SETTINGS[self.difficulty]['name_' + self.language].upper()
            self._draw_subtitle(self.L(f"СЛОЖНОСТЬ: {dn}", f"DIFFICULTY: {dn}"), 5, (255, 100, 100))

            for i in range(scroll, min(scroll + per, len(dnames))):
                diff = dnames[i]
                r = diff_rects[i - scroll]
                pygame.draw.rect(self.screen, (25, 25, 45), r, border_radius=8)
                pygame.draw.rect(self.screen, dcol[diff], r, 2, border_radius=8)
                name_s = self.font_small.render(DIFFICULTY_SETTINGS[diff]["name_" + self.language], True, dcol[diff])
                desc_s = self.font_tiny.render(desc[diff], True, (180, 180, 200))
                self.screen.blit(name_s, (r.centerx - name_s.get_width() // 2, r.y + 2))
                self.screen.blit(desc_s, (r.centerx - desc_s.get_width() // 2, r.y + 25))

        while True:
            mx, my = pygame.mouse.get_pos()

            # Отрисовка оболочек со стрелками (получаем что нажато)
            t_action = self._draw_setting_box(t_rect, self.L("Время раунда:", "Round time:"), self.round_time, mx, my)
            s_action = self._draw_setting_box(s_rect, self.L("Игра до:", "Play to:"), self.target_score, mx, my)
            th_action = self._draw_setting_box(th_rect, self.L("Тема стола:", "Table theme:"),
                                               THEMES[self.theme]["name"], mx, my)
            b_action = self._draw_setting_box(b_rect, self.L("Цвет мяча:", "Ball color:"), self.ball_color, mx, my)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE: return
                    if ev.key == pygame.K_SPACE:
                        self._save_settings()
                        Game(self.screen, self.difficulty, self.theme, self.music_volume, self.sfx_volume,
                             "pve", self.round_time, self.target_score, self.ball_color, self.language).run()
                        return

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 4:
                        scroll = max(scroll - 1, 0)
                    elif ev.button == 5:
                        scroll = min(scroll + 1, max_scroll)
                    elif ev.button == 1:
                        if up_btn.collidepoint(mx, my):
                            scroll = max(scroll - 1, 0)
                        elif down_btn.collidepoint(mx, my):
                            scroll = min(scroll + 1, max_scroll)
                        # Сложности
                        for i in range(scroll, min(scroll + per, len(dnames))):
                            if diff_rects[i - scroll].collidepoint(mx, my): self.difficulty = dnames[i]
                        # Настройки через стрелки
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
                            Game(self.screen, self.difficulty, self.theme, self.music_volume, self.sfx_volume,
                                 "pve", self.round_time, self.target_score, self.ball_color, self.language).run()
                            return
                        elif back_btn.collidepoint(mx, my):
                            return

            # Дорисовываем всё остальное
            self._draw_bg()
            self._draw_title(self.L("ИГРА С КОМПЬЮТЕРОМ", "PLAYER vs COMPUTER"), 10)
            dn = DIFFICULTY_SETTINGS[self.difficulty]['name_' + self.language].upper()
            self._draw_subtitle(self.L(f"СЛОЖНОСТЬ: {dn}", f"DIFFICULTY: {dn}"), 60, (255, 100, 100))

            for i in range(scroll, min(scroll + per, len(dnames))):
                diff = dnames[i]
                r = diff_rects[i - scroll]
                pygame.draw.rect(self.screen, (25, 25, 45), r, border_radius=8)
                pygame.draw.rect(self.screen, dcol[diff], r, 2, border_radius=8)
                name_s = self.font_small.render(DIFFICULTY_SETTINGS[diff]["name_" + self.language], True, dcol[diff])
                desc_s = self.font_tiny.render(desc[diff], True, (180, 180, 200))
                self.screen.blit(name_s, (r.centerx - name_s.get_width() // 2, r.y + 2))
                self.screen.blit(desc_s, (r.centerx - desc_s.get_width() // 2, r.y + 25))

            self._draw_setting_box(t_rect, self.L("Время раунда:", "Round time:"), self.round_time, mx, my)
            self._draw_setting_box(s_rect, self.L("Игра до:", "Play to:"), self.target_score, mx, my)
            self._draw_setting_box(th_rect, self.L("Тема стола:", "Table theme:"), THEMES[self.theme]["name"], mx, my)
            self._draw_setting_box(b_rect, self.L("Цвет мяча:", "Ball color:"), self.ball_color, mx, my)

            self._draw_scroll_arrows(up_btn, down_btn, mx, my)
            self._draw_button(self.L("СТАРТ", "START"), start_btn, start_btn.collidepoint(mx, my), (100, 255, 100))
            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), (255, 100, 100))
            pygame.display.flip();
            self.clock.tick(60)

    # ========================= НАСТРОЙКА PvP =========================
    def show_pvp_setup(self):
        tnames = list(ROUND_TIMES.keys());
        thnames = list(THEMES.keys())
        bnames = list(BALL_COLORS.keys());
        snames = list(TARGET_SCORES.keys())

        box_w = 480

        t_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 220, box_w, 40)
        s_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 270, box_w, 40)
        th_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 320, box_w, 40)
        b_rect = pygame.Rect(WIDTH // 2 - box_w // 2, 370, box_w, 40)

        start_btn = pygame.Rect(WIDTH // 2 - 180, 450, 360, 55)
        back_btn = pygame.Rect(WIDTH // 2 - 180, 520, 360, 55)

        def draw():
            self._draw_title(self.L("ИГРОК ПРОТИВ ИГРОКА", "PLAYER vs PLAYER"))
            c = self.L("Левый: W/S | Правый: Стрелки ВВЕРХ/ВНИЗ", "Left: W/S | Right: ARROWS UP/DOWN")
            s = self.font_small.render(c, True, (180, 180, 200))
            self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, 130))

        while True:
            mx, my = pygame.mouse.get_pos()

            t_action = self._draw_setting_box(t_rect, self.L("Время раунда:", "Round time:"), self.round_time, mx, my)
            s_action = self._draw_setting_box(s_rect, self.L("Игра до:", "Play to:"), self.target_score, mx, my)
            th_action = self._draw_setting_box(th_rect, self.L("Тема стола:", "Table theme:"),
                                               THEMES[self.theme]["name"], mx, my)
            b_action = self._draw_setting_box(b_rect, self.L("Цвет мяча:", "Ball color:"), self.ball_color, mx, my)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE: return
                    if ev.key == pygame.K_SPACE:
                        self._save_settings()
                        Game(self.screen, "normal", self.theme, self.music_volume, self.sfx_volume,
                             "pvp", self.round_time, self.target_score, self.ball_color, self.language).run()
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
                        Game(self.screen, "normal", self.theme, self.music_volume, self.sfx_volume,
                             "pvp", self.round_time, self.target_score, self.ball_color, self.language).run()
                        return
                    elif back_btn.collidepoint(mx, my):
                        return

            self._draw_bg();
            draw()
            self._draw_setting_box(t_rect, self.L("Время раунда:", "Round time:"), self.round_time, mx, my)
            self._draw_setting_box(s_rect, self.L("Игра до:", "Play to:"), self.target_score, mx, my)
            self._draw_setting_box(th_rect, self.L("Тема стола:", "Table theme:"), THEMES[self.theme]["name"], mx, my)
            self._draw_setting_box(b_rect, self.L("Цвет мяча:", "Ball color:"), self.ball_color, mx, my)
            self._draw_button(self.L("СТАРТ", "START"), start_btn, start_btn.collidepoint(mx, my), (100, 255, 100))
            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), (255, 100, 100))
            pygame.display.flip();
            self.clock.tick(60)

    # ========================= ПРАВИЛА =========================
    def show_rules(self):
        rules = [
            (self.L("РЕЖИМЫ ИГРЫ", "GAME MODES"), True), ("", False),
            (self.L("Игрок vs Компьютер — вы против ИИ", "Player vs Computer — you vs AI"), False),
            (self.L("W (вверх) / S (вниз)", "W (up) / S (down)"), False), ("", False),
            (self.L("Игрок vs Игрок — игра вдвоём", "Player vs Player — local multiplayer"), False),
            (self.L("Левый: W / S     Правый: Стрелки ВВЕРХ / ВНИЗ", "Left: W / S     Right: ARROWS UP / DOWN"), False),
            ("", False), (self.L("ЦЕЛЬ ИГРЫ", "GOAL"), True), ("", False),
            (self.L("Забить мяч в ворота соперника", "Score in opponent's goal"), False),
            (self.L("Ворота — затемнённые зоны по бокам поля", "Goals — dark zones on sides"), False),
            ("", False), (self.L("ПРАВИЛА", "RULES"), True), ("", False),
            (self.L("Мяч ускоряется, если долго нет гола", "Ball speeds up without goals"), False),
            (self.L("После гола — медленная подача пропустившему", "After goal — slow serve"), False),
            (self.L("Время вышло + равный счёт = НИЧЬЯ", "Time up + equal score = DRAW"), False),
            ("", False), (self.L("УПРАВЛЕНИЕ", "CONTROLS"), True), ("", False),
            (self.L("ESC — пауза", "ESC — pause"), False),
            (self.L("В паузе: ESC — продолжить", "Pause: ESC — continue"), False),
            (self.L("В паузе: M — выйти в меню", "Pause: M — menu"), False),
        ]
        scroll = 0;
        per = 14;
        max_scroll = max(0, len(rules) - per)
        margin = 80
        up_btn = pygame.Rect(WIDTH - 60, margin, 40, 40)
        down_btn = pygame.Rect(WIDTH - 60, HEIGHT - margin - 40, 40, 40)
        back_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 45)

        while True:
            mx, my = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 4:
                        scroll = max(scroll - 1, 0)
                    elif ev.button == 5:
                        scroll = min(scroll + 1, max_scroll)
                    elif ev.button == 1:
                        if back_btn.collidepoint(mx, my): return
                        if up_btn.collidepoint(mx, my):
                            scroll = max(scroll - 1, 0)
                        elif down_btn.collidepoint(mx, my):
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
                                                                                                "W") and not text.startswith(
                                                                                                "Л") else (
                                                                                            180, 180, 200)))
                    self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, y))
                y += 36 if is_title else 30

            self._draw_scroll_arrows(up_btn, down_btn, mx, my)
            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), small=True)
            pygame.display.flip();
            self.clock.tick(60)

    # ========================= НАСТРОЙКИ =========================
    def show_settings(self):
        lang_btn = pygame.Rect(WIDTH // 2 - 140, 200, 280, 55)
        music_rect = pygame.Rect(WIDTH // 2 - 200, 300, 400, 40)
        sfx_rect = pygame.Rect(WIDTH // 2 - 200, 400, 400, 40)
        back_btn = pygame.Rect(WIDTH // 2 - 100, 510, 200, 50)

        def draw():
            self._draw_title(self.L("НАСТРОЙКИ", "SETTINGS"))
            ms = self.font_small.render(
                self.L(f"Музыка: {int(self.music_volume * 100)}%", f"Music: {int(self.music_volume * 100)}%"), True,
                YELLOW)
            self.screen.blit(ms, (WIDTH // 2 - ms.get_width() // 2, 305))
            pygame.draw.rect(self.screen, (60, 60, 100), (WIDTH // 2 - 150, 345, 300, 8), border_radius=4)
            pygame.draw.rect(self.screen, YELLOW, (WIDTH // 2 - 150, 345, int(300 * self.music_volume), 8),
                             border_radius=4)
            sf = self.font_small.render(
                self.L(f"Звуки: {int(self.sfx_volume * 100)}%", f"Sound: {int(self.sfx_volume * 100)}%"), True, YELLOW)
            self.screen.blit(sf, (WIDTH // 2 - sf.get_width() // 2, 405))
            pygame.draw.rect(self.screen, (60, 60, 100), (WIDTH // 2 - 150, 445, 300, 8), border_radius=4)
            pygame.draw.rect(self.screen, YELLOW, (WIDTH // 2 - 150, 445, int(300 * self.sfx_volume), 8),
                             border_radius=4)

        while True:
            mx, my = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE: self._save_settings(); return
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if lang_btn.collidepoint(mx, my):
                        self.language = "en" if self.language == "ru" else "ru"
                    elif back_btn.collidepoint(mx, my):
                        self._save_settings(); return

            if pygame.mouse.get_pressed()[0]:
                if pygame.Rect(WIDTH // 2 - 150, 335, 300, 20).collidepoint(mx, my):
                    self.music_volume = (mx - (WIDTH // 2 - 150)) / 300
                    self.music_volume = max(0, min(1, self.music_volume))
                    try:
                        pygame.mixer.music.set_volume(self.music_volume)
                    except:
                        pass
                if pygame.Rect(WIDTH // 2 - 150, 435, 300, 20).collidepoint(mx, my):
                    self.sfx_volume = (mx - (WIDTH // 2 - 150)) / 300
                    self.sfx_volume = max(0, min(1, self.sfx_volume))

            self._draw_bg();
            draw()
            lt = "Русский" if self.language == "ru" else "English"
            self._draw_button(f"{self.L('Язык:', 'Language:')} {lt}", lang_btn, lang_btn.collidepoint(mx, my), YELLOW,
                              small=True)
            self._draw_button(self.L("НАЗАД", "BACK"), back_btn, back_btn.collidepoint(mx, my), small=True)
            pygame.display.flip();
            self.clock.tick(60)