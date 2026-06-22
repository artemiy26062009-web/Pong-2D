import pygame
import random
import sys
from config import (WIDTH, HEIGHT, FPS, WHITE, BLACK, YELLOW, RED, GRAY,
                    DARK_BG, THEMES, BALL_COLORS, TABLE_MARGIN, GOAL_ZONE,
                    ROUND_TIMES, TARGET_SCORES, PADDLE_SPEED, DIFFICULTY_SETTINGS,
                    SERVE_SPEED)
from player import Paddle
from ball import Ball
from achievements import Achievements
from stats import Stats


class Game:
    def __init__(self, screen, difficulty="normal", theme="green",
                 music_volume=0.5, sfx_volume=0.7, game_mode="pve",
                 round_time="1.5 минуты", target_score="До 5", ball_color="Белый",
                 language="ru"):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.difficulty = difficulty
        self.theme = theme
        self.music_volume = music_volume
        self.sfx_volume = sfx_volume
        self.game_mode = game_mode
        self.language = language
        self.margin = TABLE_MARGIN
        self.paused = False
        self.quit_game = False

        self.round_time_total = ROUND_TIMES.get(round_time, 90)
        self.target_score = TARGET_SCORES.get(target_score, 5)
        self.infinite_mode = (target_score == "Бесконечно")
        self.infinite_time = (round_time == "Бесконечно")
        self.ball_color = BALL_COLORS.get(ball_color, WHITE)

        theme_data = THEMES.get(theme, THEMES["green"])
        self.table_color = theme_data["table"]
        self.table_dark = theme_data["table_dark"]

        paddle_x_left = self.margin + GOAL_ZONE
        paddle_x_right = WIDTH - self.margin - GOAL_ZONE - 12

        self.player1 = Paddle(paddle_x_left, HEIGHT // 2 - 45, theme_data["paddle_player"], PADDLE_SPEED, True)
        if game_mode == "pvp":
            self.player2 = Paddle(paddle_x_right, HEIGHT // 2 - 45, theme_data["paddle_player2"], PADDLE_SPEED, True)
        else:
            self.player2 = Paddle(paddle_x_right, HEIGHT // 2 - 45, theme_data["paddle_computer"], PADDLE_SPEED, False)

        self.ball = Ball(difficulty)
        self.score_left = 0
        self.score_right = 0
        self.round_time = self.round_time_total

        self.font_score = pygame.font.SysFont("Arial", 44)
        self.font_timer = pygame.font.SysFont("Arial", 36)
        self.font_info = pygame.font.SysFont("Arial", 20)
        self.font_pause = pygame.font.SysFont("Arial", 64)
        self.font_pause_small = pygame.font.SysFont("Arial", 28)
        self.font_achieve = pygame.font.SysFont("Arial", 36)
        self.font_result = pygame.font.SysFont("Arial", 56)
        self.font_result_big = pygame.font.SysFont("Arial", 72, bold=True)
        self.font_result_mid = pygame.font.SysFont("Arial", 46, bold=True)
        self.font_stats = pygame.font.SysFont("Arial", 30)
        self.font_countdown = pygame.font.SysFont("Arial", 120, bold=True)

        self.achievements = Achievements()
        self.stats = Stats()
        self.goal_timer = 0
        self.match_time = 0

        self._load_sounds()

    def _load_sounds(self):
        try:
            self.hit_sound = pygame.mixer.Sound("sounds/hit.wav");
            self.hit_sound.set_volume(self.sfx_volume)
        except:
            self.hit_sound = None
        try:
            self.wall_sound = pygame.mixer.Sound("sounds/wall.wav");
            self.wall_sound.set_volume(self.sfx_volume * 0.5)
        except:
            self.wall_sound = None
        try:
            self.score_sound = pygame.mixer.Sound("sounds/score.wav");
            self.score_sound.set_volume(self.sfx_volume)
        except:
            self.score_sound = None
        try:
            self.win_sound = pygame.mixer.Sound("sounds/win.wav");
            self.win_sound.set_volume(self.sfx_volume)
        except:
            self.win_sound = None
        try:
            self.lose_sound = pygame.mixer.Sound("sounds/lose.wav");
            self.lose_sound.set_volume(self.sfx_volume)
        except:
            self.lose_sound = None

    def t(self, key):
        if self.language == "ru":
            return {
                "pause": "ПАУЗА", "continue": "ESC - Продолжить", "menu": "M - Выйти в меню",
                "achievement": "Достижение получено!", "speed": "Скорость",
                "win": "ВЫ ВЫИГРАЛИ!", "lose": "ВЫ ПРОИГРАЛИ", "draw": "НИЧЬЯ!",
                "left_win": "ЛЕВЫЙ ИГРОК ПОБЕДИЛ!", "right_win": "ПРАВЫЙ ИГРОК ПОБЕДИЛ!",
                "press_key": "Нажмите любую клавишу", "stats_title": "СТАТИСТИКА МАТЧА",
                "hits": "Ударов", "goals": "Счёт", "max_speed": "Макс. скорость",
                "streak": "Лучшая серия", "time": "Время", "inf_text": "Бесконечно",
                "back_to_menu": "ESC - Выйти в главное меню",
                "back_to_settings": "ПРОБЕЛ - Вернуться к настройкам",
                "tab_stats": "TAB - Статистика матча",
            }.get(key, key)
        else:
            return {
                "pause": "PAUSE", "continue": "ESC - Continue", "menu": "M - Menu",
                "achievement": "Achievement!", "speed": "Speed",
                "win": "YOU WIN!", "lose": "YOU LOSE", "draw": "DRAW!",
                "left_win": "LEFT PLAYER WINS!", "right_win": "RIGHT PLAYER WINS!",
                "press_key": "Press any key", "stats_title": "MATCH STATS",
                "hits": "Hits", "goals": "Score", "max_speed": "Max speed",
                "streak": "Best streak", "time": "Time", "inf_text": "Infinity",
                "back_to_menu": "ESC - Return to main menu",
                "back_to_settings": "SPACE - Return to settings",
                "tab_stats": "TAB - Match statistics",
            }.get(key, key)

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.player1.move_up()
        if keys[pygame.K_s]: self.player1.move_down()
        if self.game_mode == "pvp":
            if keys[pygame.K_UP]: self.player2.move_up()
            if keys[pygame.K_DOWN]: self.player2.move_down()

    def _check_goal(self):
        if self.ball.rect.left <= self.margin:
            return "right"
        elif self.ball.rect.right >= WIDTH - self.margin:
            return "left"
        return None

    def _countdown(self):
        for i in range(3, 0, -1):
            self._draw()
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            count_text = self.font_countdown.render(str(i), True, YELLOW)
            self.screen.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2 - 60))
            pygame.display.flip()
            pygame.time.wait(700)
        self.clock.tick(FPS)

    def _goal_flash(self):
        flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash.fill((255, 255, 255, 100))
        self.screen.blit(flash, (0, 0))
        pygame.display.flip()
        pygame.time.wait(120)

    def _reset_after_goal(self, scorer):
        self._goal_flash()
        if scorer == "right":
            self.ball.reset(direction=-1)
        else:
            self.ball.reset(direction=1)
        self.player1.reset_position()
        self.player2.reset_position()
        pygame.time.wait(400)

    def _check_achievements(self):
        s = self.stats

        if self.game_mode == "pve":
            my_score = self.score_left
            my_streak = s.current_streak
            enemy_score = self.score_right
        else:
            my_score = self.score_left if s.current_streak > 0 else self.score_right
            my_streak = s.current_streak if s.current_streak > 0 else 0
            enemy_score = self.score_right if s.current_streak > 0 else self.score_left

        if s.goals_left + s.goals_right >= 1:
            if self.achievements.unlock("first_goal"):
                self._show_achievement("Первая кровь!")
        if my_score >= self.target_score and self.game_mode == "pve":
            if self.achievements.unlock("first_win"):
                self._show_achievement("Первая победа!")
        if my_streak >= 3:
            if self.achievements.unlock("hattrick"):
                self._show_achievement("Хет-трик!")
        if self.round_time <= 0 and self.score_left == self.score_right:
            if self.achievements.unlock("draw_master"):
                self._show_achievement("Миротворец!")
        if my_streak >= 5:
            if self.achievements.unlock("streak_5"):
                self._show_achievement("На раскате!")
        if my_score >= 5 and enemy_score == 0:
            if self.achievements.unlock("clean_sheet"):
                self._show_achievement("Сухарь!")
        if self.goal_timer < 3 and s.goals_left + s.goals_right >= 1:
            if self.achievements.unlock("fast_goal"):
                self._show_achievement("Молниеносный!")
        if self.game_mode == "pvp" and (self.score_left >= self.target_score or self.score_right >= self.target_score):
            if self.achievements.unlock("pvp_win"):
                self._show_achievement("Дуэлянт!")
        if s.max_speed >= 12:
            if self.achievements.unlock("speed_demon"):
                self._show_achievement("Реактивный!")
        if self.match_time >= 600:
            if self.achievements.unlock("marathon"):
                self._show_achievement("Марафонец!")
        if my_score >= 3 and enemy_score == 0 and my_score >= self.target_score:
            if self.achievements.unlock("comeback"):
                self._show_achievement("Камбэк!")
        if my_score >= 10:
            if self.achievements.unlock("ten_goals"):
                self._show_achievement("Бомбардир!")
        if abs(self.score_left - self.score_right) >= 10:
            if self.achievements.unlock("domination"):
                self._show_achievement("Доминация!")
        if self.difficulty == "hard" and self.score_left >= self.target_score:
            if self.achievements.unlock("pve_hard"):
                self._show_achievement("Ветеран!")
        if self.difficulty == "hardcore" and self.score_left >= self.target_score:
            if self.achievements.unlock("hardcore_win"):
                self._show_achievement("Хардкор пройден!")
        if enemy_score == 0 and my_score >= self.target_score:
            if self.achievements.unlock("no_death_win"):
                self._show_achievement("Бессмертный!")
        if self.match_time < 20 and self.score_left >= 5:
            if self.achievements.unlock("speedrun"):
                self._show_achievement("Спидран!")
        if self.match_time >= 1200:
            if self.achievements.unlock("longest_game"):
                self._show_achievement("Долгожитель!")
        if my_score >= 5 and enemy_score >= 5 and my_score >= self.target_score:
            if self.achievements.unlock("comeback_5"):
                self._show_achievement("Феникс!")

        unlocked_count = len(self.achievements.get_unlocked())
        if unlocked_count >= 15:
            if self.achievements.unlock("god_mode"):
                self._show_achievement("Бог понга!")

    def _show_achievement(self, text):
        surf = self.font_achieve.render(f"{self.t('achievement')} ({text})", True, YELLOW)
        bg = pygame.Rect(WIDTH // 2 - surf.get_width() // 2 - 15, 80, surf.get_width() + 30, 50)
        pygame.draw.rect(self.screen, (0, 0, 0, 220), bg, border_radius=10)
        pygame.draw.rect(self.screen, YELLOW, bg, 2, border_radius=10)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, 90))
        pygame.display.flip()
        pygame.time.wait(1500)

    def _show_pause_menu(self):
        while self.paused:
            self._draw()

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            pause_text = self.font_pause.render(self.t("pause"), True, YELLOW)
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 80))

            cont_text = self.font_pause_small.render(self.t("continue"), True, YELLOW)
            self.screen.blit(cont_text, (WIDTH // 2 - cont_text.get_width() // 2, HEIGHT // 2))

            menu_text = self.font_pause_small.render(self.t("menu"), True, YELLOW)
            self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 50))

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: self.quit_game = True; self.paused = False; return "exit"
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.paused = False
                        self._countdown()
                        return "continue"
                    if ev.key == pygame.K_m: self.paused = False; return "menu"

            self.clock.tick(FPS)
        return "continue"

    def _show_result(self):
        # В PvP всегда зелёный и звук победы
        if self.game_mode == "pvp":
            if self.score_left > self.score_right:
                text = self.t("left_win")
            elif self.score_right > self.score_left:
                text = self.t("right_win")
            else:
                text = self.t("draw")
            color = YELLOW
        else:
            if self.score_left > self.score_right:
                text = self.t("win")
                color = YELLOW
            elif self.score_right > self.score_left:
                text = self.t("lose")
                color = RED
            else:
                text = self.t("draw")
                color = GRAY

        # Выбираем шрифт в зависимости от длины текста
        if self.game_mode == "pvp" and self.score_left != self.score_right:
            result_font = self.font_result_mid  # поменьше для PvP победителя
        else:
            result_font = self.font_result_big

        waiting = True
        while waiting:
            mx, my = pygame.mouse.get_pos()

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200);
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            surf = result_font.render(text, True, color)
            self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, HEIGHT // 2 - 140))

            score_text = f"{self.score_left} - {self.score_right}"
            score_surf = self.font_result.render(score_text, True, WHITE)
            self.screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, HEIGHT // 2 - 40))

            # Кнопки без наведения
            space_text = self.font_stats.render(self.t("back_to_settings"), True, (200, 200, 200))
            self.screen.blit(space_text, (WIDTH // 2 - space_text.get_width() // 2, HEIGHT // 2 + 45))

            tab_text = self.font_stats.render(self.t("tab_stats"), True, (200, 200, 200))
            self.screen.blit(tab_text, (WIDTH // 2 - tab_text.get_width() // 2, HEIGHT // 2 + 95))

            esc_text = self.font_stats.render(self.t("back_to_menu"), True, (200, 200, 200))
            self.screen.blit(esc_text, (WIDTH // 2 - esc_text.get_width() // 2, HEIGHT // 2 + 145))

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_SPACE: return "back"
                    if ev.key == pygame.K_TAB: return "stats"
                    if ev.key == pygame.K_ESCAPE: return "menu"

            self.clock.tick(FPS)

    def _show_stats_screen(self):
        s = self.stats
        minutes = int(self.match_time) // 60;
        seconds = int(self.match_time) % 60

        lines = [
            f"{self.t('goals')}: {self.score_left} - {self.score_right}",
            f"{self.t('hits')}: {s.hits}",
            f"{self.t('max_speed')}: {s.max_speed:.1f}",
            f"{self.t('streak')}: {s.max_streak}",
            f"{self.t('time')}: {minutes}:{seconds:02d}",
        ]

        waiting = True
        while waiting:
            mx, my = pygame.mouse.get_pos()

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(230);
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            title = self.font_result.render(self.t("stats_title"), True, YELLOW)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 180))

            y = HEIGHT // 2 - 110
            for line in lines:
                surf = self.font_stats.render(line, True, WHITE)
                self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
                y += 40

            # Кнопки без наведения
            space_text = self.font_stats.render(self.t("back_to_settings"), True, (200, 200, 200))
            self.screen.blit(space_text, (WIDTH // 2 - space_text.get_width() // 2, HEIGHT - 130))

            esc_text = self.font_stats.render(self.t("back_to_menu"), True, (200, 200, 200))
            self.screen.blit(esc_text, (WIDTH // 2 - esc_text.get_width() // 2, HEIGHT - 80))

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_SPACE: return "back"
                    if ev.key == pygame.K_ESCAPE: return "menu"

            self.clock.tick(FPS)

    def run(self):
        self.ball.speed_x = SERVE_SPEED * random.choice((1, -1))
        self.ball.speed_y = SERVE_SPEED * random.choice((0.5, -0.5)) * 0.5

        self._countdown()
        self.clock.tick(FPS)

        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            self.match_time += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
                        result = self._show_pause_menu()
                        if result == "exit":
                            return "exit"
                        elif result == "menu":
                            return "menu"
            if self.paused: continue
            if self.quit_game: return "exit"
            self._handle_input()
            if self.game_mode == "pve":
                self.player2.ai_move(self.ball, self.difficulty)
            self.ball.move(dt)
            self.ball.accelerate(dt)
            if self.ball.bounce_wall():
                self.stats.add_wall_hit()
                if self.wall_sound: self.wall_sound.play()
            if self.ball.bounce_paddle(self.player1):
                self.stats.add_hit()
                if self.hit_sound: self.hit_sound.play()
            if self.ball.bounce_paddle(self.player2):
                self.stats.add_hit()
                if self.hit_sound: self.hit_sound.play()
            scorer = self._check_goal()
            if scorer:
                if self.score_sound: self.score_sound.play()
                if scorer == "right":
                    self.score_right += 1
                    self.stats.add_goal("right", self.goal_timer, abs(self.ball.speed_x))
                else:
                    self.score_left += 1
                    self.stats.add_goal("left", self.goal_timer, abs(self.ball.speed_x))
                self.goal_timer = 0
                self._check_achievements()
                self._reset_after_goal(scorer)
            self.goal_timer += dt
            if not self.infinite_time:
                self.round_time -= dt
                if self.round_time <= 0:
                    # Звук в зависимости от режима
                    if self.game_mode == "pve":
                        if self.score_left > self.score_right:
                            if self.win_sound: self.win_sound.play()
                        elif self.score_right > self.score_left:
                            if self.lose_sound: self.lose_sound.play()
                    else:
                        if self.win_sound: self.win_sound.play()

                    result_action = self._show_result()
                    while result_action == "stats":
                        result_action = self._show_stats_screen()
                    if result_action == "menu":
                        return "menu"
                    elif result_action == "back":
                        return "back"
                    else:
                        return "menu"
            if not self.infinite_mode:
                if self.score_left >= self.target_score:
                    if self.game_mode == "pve":
                        if self.win_sound: self.win_sound.play()
                    else:
                        if self.win_sound: self.win_sound.play()
                    result_action = self._show_result()
                    while result_action == "stats":
                        result_action = self._show_stats_screen()
                    if result_action == "menu":
                        return "menu"
                    elif result_action == "back":
                        return "back"
                    else:
                        return "menu"
                elif self.score_right >= self.target_score:
                    if self.game_mode == "pve":
                        if self.lose_sound: self.lose_sound.play()
                    else:
                        if self.win_sound: self.win_sound.play()
                    result_action = self._show_result()
                    while result_action == "stats":
                        result_action = self._show_stats_screen()
                    if result_action == "menu":
                        return "menu"
                    elif result_action == "back":
                        return "back"
                    else:
                        return "menu"
            self._draw()
            pygame.display.flip()
        return "exit"

    def _draw(self):
        self.screen.fill(DARK_BG)
        goal_surface = pygame.Surface((self.margin, HEIGHT - self.margin * 2), pygame.SRCALPHA)
        goal_surface.fill((40, 40, 60, 180))
        self.screen.blit(goal_surface, (0, self.margin))
        self.screen.blit(goal_surface, (WIDTH - self.margin, self.margin))
        goal_font = pygame.font.Font(None, 24)
        goal_text = "ГОЛ" if self.language == "ru" else "GOAL"
        self.screen.blit(goal_font.render(goal_text, True, (150, 150, 150)), (10, HEIGHT // 2 - 10))
        self.screen.blit(goal_font.render(goal_text, True, (150, 150, 150)),
                         (WIDTH - self.margin + 10, HEIGHT // 2 - 10))
        tx, ty = self.margin, self.margin
        tw, th = WIDTH - self.margin * 2, HEIGHT - self.margin * 2
        pygame.draw.rect(self.screen, (10, 10, 15), pygame.Rect(tx + 4, ty + 4, tw, th), border_radius=6)
        pygame.draw.rect(self.screen, self.table_dark, pygame.Rect(tx, ty, tw, th), border_radius=6)
        pygame.draw.rect(self.screen, self.table_color, pygame.Rect(tx, ty, tw, th).inflate(-8, -8), border_radius=4)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(tx, ty, tw, th), 3, border_radius=6)
        mid_x = WIDTH // 2
        pygame.draw.line(self.screen, WHITE, (mid_x, ty + 4), (mid_x, ty + th - 4), 2)
        pygame.draw.circle(self.screen, WHITE, (mid_x, HEIGHT // 2), 50, 2)
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.ball.draw(self.screen, self.ball_color)
        info_y = 8
        p_text = self.font_score.render(str(self.score_left), True, WHITE)
        c_text = self.font_score.render(str(self.score_right), True, WHITE)
        pw, ph = p_text.get_width(), p_text.get_height()
        cw, ch = c_text.get_width(), c_text.get_height()
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (WIDTH // 4 - pw // 2 - 2, info_y, pw + 4, ph), border_radius=3)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (WIDTH * 3 // 4 - cw // 2 - 2, info_y, cw + 4, ch),
                         border_radius=3)
        self.screen.blit(p_text, (WIDTH // 4 - pw // 2, info_y))
        self.screen.blit(c_text, (WIDTH * 3 // 4 - cw // 2, info_y))
        if not self.infinite_time:
            ttc = YELLOW if self.round_time < 10 else WHITE
            ttx = self.font_timer.render(f"{int(self.round_time)}s", True, ttc)
            self.screen.blit(ttx, (WIDTH // 2 - ttx.get_width() // 2, info_y + 3))
        else:
            ttx = self.font_timer.render(self.t("inf_text"), True, WHITE)
            self.screen.blit(ttx, (WIDTH // 2 - ttx.get_width() // 2, info_y + 3))
        spx = self.font_info.render(f"{self.t('speed')}: {abs(self.ball.speed_x):.1f}", True, (180, 180, 180))
        self.screen.blit(spx, (WIDTH // 2 - spx.get_width() // 2, HEIGHT - 20))
        if self.game_mode == "pve":
            diff_name = DIFFICULTY_SETTINGS[self.difficulty]['name_' + self.language]
            mode_str = f"PvE | {diff_name}"
        else:
            mode_str = "PvP"
        self.screen.blit(self.font_info.render(mode_str, True, (180, 180, 180)), (10, HEIGHT - 20))
        if not self.infinite_mode:
            goal_str = f"До {self.target_score}" if self.language == "ru" else f"To {self.target_score}"
        else:
            goal_str = "∞"
        goal_surf = self.font_info.render(goal_str, True, (180, 180, 180))
        self.screen.blit(goal_surf, (WIDTH - goal_surf.get_width() - 10, HEIGHT - 20))