import pygame
import random
from config import WIDTH, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, TABLE_MARGIN, DIFFICULTY_SETTINGS


class Paddle:
    def __init__(self, x, y, color, speed=8, is_player=True):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.is_player = is_player
        self.speed = speed
        self.score = 0
        self.margin = TABLE_MARGIN

    def move_up(self):
        if self.rect.top > self.margin:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT - self.margin:
            self.rect.y += self.speed

    def ai_move(self, ball, difficulty):
        settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["normal"])
        ai_speed = settings["speed"]
        error_chance = settings["error_chance"]

        # Ошибка: случайное движение
        if error_chance > 0 and random.random() < error_chance:
            action = random.choice(["up", "down", "stay"])
            if action == "up" and self.rect.top > self.margin:
                self.rect.y -= ai_speed * 0.5
            elif action == "down" and self.rect.bottom < HEIGHT - self.margin:
                self.rect.y += ai_speed * 0.5
            return

        # Предугадывание траектории (для сложного и хардкора)
        if settings.get("predict", False):
            if ball.speed_x > 0:
                steps = (self.rect.x - ball.rect.x) / ball.speed_x if ball.speed_x != 0 else 0
                target_y = ball.rect.centery + ball.speed_y * steps * 0.06
                while target_y < self.margin or target_y > HEIGHT - self.margin:
                    if target_y < self.margin:
                        target_y = 2 * self.margin - target_y
                    if target_y > HEIGHT - self.margin:
                        target_y = 2 * (HEIGHT - self.margin) - target_y
            else:
                target_y = HEIGHT // 2
        else:
            target_y = ball.rect.centery

        # ===== ПЛАВНОЕ ДВИЖЕНИЕ К ЦЕЛИ =====
        diff = target_y - self.rect.centery  # насколько далеко цель

        if abs(diff) > 1:  # если разница больше 1 пикселя
            # Чем дальше цель — тем быстрее двигаемся
            # Но не быстрее максимальной скорости ai_speed
            move = diff * 0.25  # 25% от разницы (плавное приближение)
            move = max(-ai_speed, min(ai_speed, move))  # ограничиваем скорость

            new_y = self.rect.y + move
            # Не выходим за границы
            new_y = max(self.margin, new_y)
            new_y = min(HEIGHT - self.margin - self.rect.height, new_y)
            self.rect.y = new_y

    def reset_position(self):
        self.rect.centery = HEIGHT // 2

    def draw(self, screen):
        shadow = self.rect.copy()
        shadow.x += 3
        shadow.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow, border_radius=4)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=4)
        hl = pygame.Rect(self.rect.x + 3, self.rect.y + 5, 4, self.rect.height - 10)
        pygame.draw.rect(screen, (255, 255, 255, 60), hl, border_radius=2)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=4)