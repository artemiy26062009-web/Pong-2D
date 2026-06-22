import pygame, random
from config import (WIDTH, HEIGHT, BALL_SIZE, BALL_MAX_SPEED,
                    BALL_ACCELERATION, TABLE_MARGIN, SERVE_SPEED)


class Ball:
    def __init__(self, difficulty="normal"):
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.base_speed = SERVE_SPEED
        self.speed_x = SERVE_SPEED * random.choice((1, -1))
        self.speed_y = SERVE_SPEED * random.choice((0.5, -0.5)) * 0.5
        self.time_without_goal = 0
        self.margin = TABLE_MARGIN
        self.acceleration = BALL_ACCELERATION.get(difficulty, 0.25)
        self.trail = []

    def move(self, dt):
        self.trail.append(self.rect.center)
        if len(self.trail) > 12: self.trail.pop(0)
        self.rect.x += self.speed_x * dt * 60
        self.rect.y += self.speed_y * dt * 60

    def accelerate(self, dt):
        self.time_without_goal += dt
        current_speed = abs(self.speed_x)
        if current_speed < BALL_MAX_SPEED:
            # Плавно разгоняемся от 1.0 до BALL_MAX_SPEED
            new_speed = 1.0 + self.acceleration * self.time_without_goal * 2
            new_speed = min(new_speed, BALL_MAX_SPEED)
            self.speed_x = new_speed if self.speed_x > 0 else -new_speed
            self.speed_y = new_speed if self.speed_y > 0 else -new_speed

    def bounce_wall(self):
        if self.rect.top <= self.margin:
            self.rect.top = self.margin; self.speed_y = abs(self.speed_y); return True
        elif self.rect.bottom >= HEIGHT - self.margin:
            self.rect.bottom = HEIGHT - self.margin; self.speed_y = -abs(self.speed_y); return True
        return False

    def bounce_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
            offset = max(-1, min(1, offset))
            cs = max(abs(self.speed_x), abs(self.speed_y))
            self.speed_y = cs * offset * 0.7
            if paddle.rect.centerx < WIDTH // 2:
                self.speed_x = abs(cs); self.rect.left = paddle.rect.right
            else:
                self.speed_x = -abs(cs); self.rect.right = paddle.rect.left
            return True
        return False

    def reset(self, direction):
        """Медленная подача после гола с плавным ускорением"""
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        # Супер медленная начальная скорость
        self.base_speed = 1.0  # почти стоит
        self.speed_x = 1.0 * direction
        self.speed_y = 0.3 * random.choice((0.5, -0.5))
        self.time_without_goal = 0
        self.trail.clear()

    def draw(self, screen, color):
        for i, pos in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)
            ts = BALL_SIZE * (0.3 + alpha * 0.7)
            tc = (int(color[0] * alpha), int(color[1] * alpha), int(color[2] * alpha))
            tr = pygame.Rect(0, 0, ts, ts);
            tr.center = pos
            pygame.draw.ellipse(screen, tc, tr)
        gr = self.rect.inflate(6, 6)
        pygame.draw.ellipse(screen, (color[0] // 3, color[1] // 3, color[2] // 3, 100), gr)
        pygame.draw.ellipse(screen, color, self.rect)
        pygame.draw.ellipse(screen, (255, 255, 255), (self.rect.x + 3, self.rect.y + 2, 4, 4))