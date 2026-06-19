import pygame
import random
from config import (WIDTH, HEIGHT, FPS, WHITE, BLACK, YELLOW, RED, GRAY,
                    DARK_BG, THEMES, BALL_COLORS, TABLE_MARGIN, GOAL_ZONE,
                    ROUND_TIMES, TARGET_SCORES, PADDLE_SPEED)
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

        self.font_score = pygame.font.SysFont("Arial", 38)
        self.font_timer = pygame.font.SysFont("Arial", 36)
        self.font_info = pygame.font.SysFont("Arial", 20)
        self.font_pause = pygame.font.SysFont("Arial", 64)
        self.font_pause_small = pygame.font.SysFont("Arial", 28)
        self.font_achieve = pygame.font.SysFont("Arial", 36)
        self.font_result = pygame.font.SysFont("Arial", 56)
        self.font_stats = pygame.font.SysFont("Arial", 30)

        self.achievements = Achievements()
        self.stats = Stats()
        self.goal_timer = 0
        self.match_time = 0

        self._load_sounds()

    def _load_sounds(self):
        try:
            self.hit_sound = pygame.mixer.Sound("sounds/hit.wav"); self.hit_sound.set_volume(self.sfx_volume)
        except:
            self.hit_sound = None
        try:
            self.wall_sound = pygame.mixer.Sound("sounds/wall.wav"); self.wall_sound.set_volume(self.sfx_volume * 0.5)
        except:
            self.wall_sound = None
        try:
            self.score_sound = pygame.mixer.Sound("sounds/score.wav"); self.score_sound.set_volume(self.sfx_volume)
        except:
            self.score_sound = None
        try:
            self.win_sound = pygame.mixer.Sound("sounds/win.wav"); self.win_sound.set_volume(self.sfx_volume)
        except:
            self.win_sound = None
        try:
            self.lose_sound = pygame.mixer.Sound("sounds/lose.wav"); self.lose_sound.set_volume(self.sfx_volume)
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
                "streak": "Лучшая серия", "time": "Время",
            }.get(key, key)
        else:
            return {
                "pause": "PAUSE", "continue": "ESC - Continue", "menu": "M - Menu",
                "achievement": "Achievement!", "speed": "Speed",
                "win": "YOU WIN!", "lose": "YOU LOSE", "draw": "DRAW!",
                "left_win": "LEFT PLAYER WINS!", "right_win": "RIGHT PLAYER WINS!",
                "press_key": "Press any key", "stats_title": "MATCH STATS",
                "hits": "Hits", "goals": "Score", "max_speed": "Max speed",
                "streak": "Best streak", "time": "Time",
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
        if not self.infinite_time: self.round_time = self.round_time_total
        pygame.time.wait(400)

    def _check_achievements(self):
        s = self.stats
        checks = [
            (s.goals_left + s.goals_right >= 1, "first_goal", "Первая кровь!"),
            (s.current_streak >= 3, "hattrick", "Хет-трик!"),
            (s.current_streak >= 5, "streak_5", "На раскате!"),
            (s.goals_left >= 5 and s.goals_right == 0, "clean_sheet", "Сухарь! 5:0"),
            (
            self.difficulty == "hardcore" and self.score_left >= self.target_score, "hardcore_win", "Хардкор пройден!"),
            (s.goals_left >= 10, "ten_goals", "Бомбардир!"),
            (self.goal_timer < 3 and s.goals_left >= 1, "fast_goal", "Молниеносный!"),
            (s.max_speed >= 12, "speed_demon", "Реактивный!"),
            (self.match_time >= 600, "marathon", "Марафонец!"),
            (abs(self.score_left - self.score_right) == 1, "close_call", "На волоске!"),
            (abs(self.score_left - self.score_right) >= 10, "domination", "Доминация!"),
            (self.game_mode == "pvp" and self.score_left >= self.target_score, "pvp_win", "Дуэлянт!"),
            (self.difficulty == "hard" and self.score_left >= self.target_score, "pve_hard", "Ветеран!"),
            (self.round_time <= 0 and self.score_left > self.score_right, "overtime_win", "Овертайм!"),
            (self.round_time <= 0 and self.score_left == self.score_right, "draw_master", "Миротворец!"),
            (self.score_right == 0 and self.score_left >= self.target_score, "perfect_round", "Идеальный раунд!"),
            (self.score_right == 0 and self.score_left >= self.target_score, "no_death_win", "Бессмертный!"),
            (self.match_time < 30 and self.score_left >= self.target_score, "fast_match", "Блицкриг!"),
        ]
        for condition, name, text in checks:
            if condition and self.achievements.unlock(name):
                self._show_achievement(text)

    def _show_achievement(self, text):
        surf = self.font_achieve.render(f"{self.t('achievement')} ({text})", True, YELLOW)
        bg = pygame.Rect(WIDTH // 2 - surf.get_width() // 2 - 15, 80, surf.get_width() + 30, 50)
        pygame.draw.rect(self.screen, (0, 0, 0, 220), bg, border_radius=10)
        pygame.draw.rect(self.screen, YELLOW, bg, 2, border_radius=10)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, 90))
        pygame.display.flip()
        pygame.time.wait(1500)

    def _show_pause_menu(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        pause_text = self.font_pause.render(self.t("pause"), True, YELLOW)
        self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 80))
        buttons = [
            (self.t("continue"), HEIGHT // 2),
            (self.t("menu"), HEIGHT // 2 + 50),
        ]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for text, y in buttons:
            btn_text = self.font_pause_small.render(text, True, YELLOW)
            btn_rect = pygame.Rect(WIDTH // 2 - btn_text.get_width() // 2 - 20, y - 10, btn_text.get_width() + 40, 40)
            if btn_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.screen, (50, 50, 60), btn_rect, border_radius=5)
                pygame.draw.rect(self.screen, YELLOW, btn_rect, 2, border_radius=5)
            self.screen.blit(btn_text, (WIDTH // 2 - btn_text.get_width() // 2, y))
        pygame.display.flip()
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.quit_game = True; self.paused = False; return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.paused = False; return "continue"
                    if event.key == pygame.K_m: self.paused = False; return "menu"
            self.clock.tick(FPS)
        return "continue"

    def _show_result(self):
        if self.score_left > self.score_right:
            text = self.t("win") if self.game_mode == "pve" else self.t("left_win")
            color = YELLOW
        elif self.score_right > self.score_left:
            text = self.t("lose") if self.game_mode == "pve" else self.t("right_win")
            color = RED
        else:
            text = self.t("draw")
            color = GRAY
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        surf = self.font_result.render(text, True, color)
        self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, HEIGHT // 2 - 80))
        hint = self.font_stats.render(self.t("press_key"), True, WHITE)
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN: waiting = False

    def _show_stats_screen(self):
        s = self.stats
        minutes = int(self.match_time) // 60
        seconds = int(self.match_time) % 60
        lines = [
            f"{self.t('goals')}: {self.score_left} - {self.score_right}",
            f"{self.t('hits')}: {s.hits}",
            f"{self.t('max_speed')}: {s.max_speed:.1f}",
            f"{self.t('streak')}: {s.max_streak}",
            f"{self.t('time')}: {minutes}:{seconds:02d}",
            "",
            self.t("press_key"),
        ]
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        title = self.font_result.render(self.t("stats_title"), True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150))
        y = HEIGHT // 2 - 90
        for line in lines:
            if line:
                surf = self.font_stats.render(line, True, WHITE)
                self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
            y += 40
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN: waiting = False

    def run(self):
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
                    if self.score_left > self.score_right:
                        if self.win_sound: self.win_sound.play()
                    elif self.score_right > self.score_left:
                        if self.lose_sound: self.lose_sound.play()
                    self._show_result()
                    self._show_stats_screen()
                    return "menu"
            if not self.infinite_mode:
                if self.score_left >= self.target_score:
                    if self.win_sound: self.win_sound.play()
                    self._show_result()
                    self._show_stats_screen()
                    return "menu"
                elif self.score_right >= self.target_score:
                    if self.lose_sound: self.lose_sound.play()
                    self._show_result()
                    self._show_stats_screen()
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
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (WIDTH // 4 - pw // 2 - 8, info_y, pw + 16, ph + 6),
                         border_radius=4)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (WIDTH * 3 // 4 - cw // 2 - 8, info_y, cw + 16, ch + 6),
                         border_radius=4)
        self.screen.blit(p_text, (WIDTH // 4 - pw // 2, info_y + 3))
        self.screen.blit(c_text, (WIDTH * 3 // 4 - cw // 2, info_y + 3))
        if not self.infinite_time:
            ttc = YELLOW if self.round_time < 10 else WHITE
            ttx = self.font_timer.render(f"{int(self.round_time)}s", True, ttc)
            self.screen.blit(ttx, (WIDTH // 2 - ttx.get_width() // 2, info_y + 3))
        else:
            ttx = self.font_timer.render("inf", True, YELLOW)
            self.screen.blit(ttx, (WIDTH // 2 - ttx.get_width() // 2, info_y + 3))
        spx = self.font_info.render(f"{self.t('speed')}: {abs(self.ball.speed_x):.1f}", True, (180, 180, 180))
        self.screen.blit(spx, (WIDTH // 2 - spx.get_width() // 2, HEIGHT - 20))
        ms = "PvE" if self.game_mode == "pve" else "PvP"
        self.screen.blit(self.font_info.render(ms, True, (180, 180, 180)), (10, HEIGHT - 20))