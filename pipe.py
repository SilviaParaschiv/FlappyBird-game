import math
import random
import pygame

class PipePair:
    def __init__(self, x: int, screen_h: int, gap: int, width: int,
                 moving: bool = False,
                 body_color: tuple[int, int, int] = (66, 165, 60),
                 border_color: tuple[int, int, int] = (32, 91, 32),
                 highlight_color: tuple[int, int, int] = (125, 200, 120)):
        margin = 80
        top_h = random.randint(margin, screen_h - gap - margin)

        self.screen_h = screen_h
        self.gap = gap
        self.top_h = top_h
        self.moving = moving

        self.body_color = body_color
        self.border_color = border_color
        self.highlight_color = highlight_color

        self.top = pygame.Rect(x, 0, width, top_h)
        self.bottom = pygame.Rect(x, top_h + gap, width, screen_h - (top_h + gap))

        self.move_amp = 36
        self.move_speed = 0.0035
        self.phase = random.uniform(0, math.pi)

        self.passed = False

    def update(self, speed: float, now_ms: int) -> None:
        dx = int(speed)
        self.top.x -= dx
        self.bottom.x -= dx

        if self.moving:
            offset = int(math.sin(self.phase + now_ms * self.move_speed) * self.move_amp)
        else:
            offset = 0

        self.top.y = offset
        self.top.height = self.top_h

        self.bottom.y = self.top_h + self.gap + offset
        self.bottom.height = self.screen_h - self.bottom.y

    def draw(self, screen: pygame.Surface) -> None:
        body_color = self.body_color
        border_color = self.border_color
        highlight_color = self.highlight_color
        cap_height = 16

        def draw_one(rect: pygame.Rect) -> None:
            pygame.draw.rect(screen, body_color, rect, border_radius=6)
            pygame.draw.rect(screen, border_color, rect, width=3, border_radius=6)

            h = max(8, rect.height - 16)
            highlight_rect = pygame.Rect(rect.x + int(rect.width * 0.15), rect.y + 8, 6, h)
            pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=4)

            cap_y = rect.y - cap_height if rect.y > 0 else rect.y + rect.height
            cap_rect = pygame.Rect(rect.x - 4, cap_y, rect.width + 8, cap_height)
            pygame.draw.rect(screen, body_color, cap_rect, border_radius=6)
            pygame.draw.rect(screen, border_color, cap_rect, width=3, border_radius=6)

        draw_one(self.top)
        draw_one(self.bottom)

    def off_screen(self) -> bool:
        return self.top.right < 0

    def collide(self, bird_rect: pygame.Rect) -> bool:
        return self.top.colliderect(bird_rect) or self.bottom.colliderect(bird_rect)

    def is_passed_by(self, bird_rect: pygame.Rect) -> bool:
        return self.top.right < bird_rect.left
