import pygame
from bird import Bird
from pipe import PipePair
from score import ScoreManager

START, PLAYING, GAME_OVER = 0, 1, 2

class Game:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.bird = Bird(100, height // 2)
        self.pipes: list[PipePair] = []

        self.score = 0
        self.pipe_gap = 200
        self.pipe_width = 70
        self.pipe_speed = 4.5

        self.state = START
        self.mode = 1 
        self.score_manager = ScoreManager()

        self.spawn_start_ms = 1200
        self.spawn_min_ms = 500
        self.spawn_decay= 70
        self.spawn_every_ms=self.spawn_start_ms
        self.last_spawn_ms = 0
        
        self.show_info = False
        self.buttons = self._build_buttons()

    def reset(self) -> None:
        self.bird.reset(100, self.height // 2)
        self.pipes.clear()
        self.score = 0
        
        if  self.mode == 2:
            self.pipe_gap = 220
            self.pipe_speed = 3.9
            self.spawn_start_ms = 1800
            self.spawn_min_ms = 750
            self.spawn_decay = 100
        else:
            self.pipe_gap = 200
            self.pipe_speed = 4.5
            self.spawn_start_ms = 1350
            self.spawn_min_ms = 500
            self.spawn_decay = 60

        self.last_spawn_ms = 0
        self.spawn_every_ms = self.spawn_start_ms
        self.state = PLAYING
        self.show_info = False

    def _build_buttons(self) -> dict[str, pygame.Rect]:
        return {
            "start": pygame.Rect(16, 16, 110, 44),
            "restart": pygame.Rect(136, 16, 110, 44),
            "info": pygame.Rect(256, 16, 110, 44),
            "Mod Clasic": pygame.Rect(16, 70, 180, 40),
            "Mod Avansat": pygame.Rect(206, 70, 180, 40),
        }

    def _pipe_config(self) -> dict:
        if self.mode == 2:
            return {
                "moving": True,
                "body_color": (166, 118, 255),
                "border_color": (110, 70, 200),
                "highlight_color": (210, 190, 255),
            }
        return {
            "moving": False,
            "body_color": (66, 165, 60),
            "border_color": (32, 91, 32),
            "highlight_color": (125, 200, 120),
        }

    def handle_click(self, pos: tuple[int, int]) -> None:
        if self.buttons["start"].collidepoint(pos) and self.state in (START, GAME_OVER):
            self.reset()
            return
        if self.buttons["restart"].collidepoint(pos) and self.state == GAME_OVER:
            self.reset()
            return
        if self.buttons["info"].collidepoint(pos):
            self.show_info = not self.show_info
            return
        if self.buttons["Mod Clasic"].collidepoint(pos):
            self.mode = 1
            if self.state in (PLAYING, GAME_OVER):
                self.reset()
            return
        if self.buttons["Mod Avansat"].collidepoint(pos):
            self.mode = 2
            if self.state in (PLAYING, GAME_OVER):
                self.reset()
            return

    def maybe_spawn_pipe(self, now_ms: int) -> None:
        if self.last_spawn_ms == 0 or now_ms - self.last_spawn_ms >= self.spawn_every_ms:
            cfg = self._pipe_config()
            self.pipes.append(PipePair(self.width, self.height, self.pipe_gap, self.pipe_width, **cfg))
            self.last_spawn_ms = now_ms

    def update_difficulty(self) -> None:
        if self.score > 0 and self.score % 5 == 0:
            self.pipe_speed = min(self.pipe_speed + 0.03, 8.0)
            self.pipe_gap = max(160, self.pipe_gap - 1)

    def update_playing(self, now_ms: int) -> None:
        self.maybe_spawn_pipe(now_ms)
        self.update_spawn_rate()
        self.bird.update()

        for pipe in list(self.pipes):
            pipe.update(self.pipe_speed, now_ms)

            if pipe.collide(self.bird.rect):
                self.state = GAME_OVER
                self.score_manager.try_update_high_score(self.score)
                return

            if not pipe.passed and pipe.is_passed_by(self.bird.rect):
                pipe.passed = True
                self.score += 1
                self.update_difficulty()
                self.update_spawn_rate()

            if pipe.off_screen():
                self.pipes.remove(pipe)

        if self.bird.rect.top < 0 or self.bird.rect.bottom > self.height:
            self.state = GAME_OVER
            self.score_manager.try_update_high_score(self.score)

    def update_spawn_rate(self) -> None:
        
        self.spawn_every_ms = max(self.spawn_min_ms, self.spawn_start_ms - self.score*self.spawn_decay)

    def _draw_background(self, screen: pygame.Surface) -> None:
        if self.mode == 2:
            top_color = (85, 100, 160)
            bottom_color = (145, 120, 200)
        else:
            top_color = (132, 206, 235)
            bottom_color = (195, 245, 215)
        for y in range(self.height):
            t = y / max(1, self.height - 1)
            r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
            g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
            b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (self.width, y))

    def _draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str,
                      enabled: bool = True, active: bool = False) -> None:
        base_color = (255, 255, 255) if enabled else (200, 200, 200)
        if active:
            base_color = (230, 245, 255)
        border_color = (40, 120, 90)
        text_color = (20, 60, 50)
        pygame.draw.rect(screen, base_color, rect, border_radius=8)
        pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)
        font = pygame.font.Font(None, 28)
        text = font.render(label, True, text_color)
        screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    def _draw_info_overlay(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        font_title = pygame.font.Font(None, 40)
        font_body = pygame.font.Font(None, 30)
        title = font_title.render("How to Play", True, (255, 255, 255))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 2 - 120))

        lines = [
            "Press SPACE to flap",
            "Avoid the pipes",
            "Pass pipes to score",
            "Press R after a crash to retry",
            "Use the Info button to toggle this"
        ]
        for i, text in enumerate(lines):
            line = font_body.render(text, True, (240, 240, 240))
            screen.blit(line, (self.width // 2 - line.get_width() // 2, self.height // 2 - 60 + i * 32))

    def draw(self, screen: pygame.Surface, font) -> None:
        self._draw_background(screen)

        for pipe in self.pipes:
            pipe.draw(screen)

        self.bird.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (10, 40, 40))
        screen.blit(score_text, (12, 130))

        high_score_text = font.render(f"High Score: {self.score_manager.high_score}", True, (10, 40, 40))
        screen.blit(high_score_text, (12, 160))

        self._draw_button(screen, self.buttons["start"], "Start", enabled=self.state in (START, GAME_OVER))
        self._draw_button(screen, self.buttons["restart"], "Restart", enabled=self.state == GAME_OVER)
        self._draw_button(screen, self.buttons["info"], "Info")
        self._draw_button(screen, self.buttons["Mod Clasic"], "Mod Clasic", active=self.mode == 1)
        self._draw_button(screen, self.buttons["Mod Avansat"], "Mod Avansat", active=self.mode == 2)

        if self.state == START:
            msg1 = font.render("Choose a mode, then Start", True, (10, 40, 40))
            msg2 = font.render("Mod Clasic: Classic green", True, (10, 40, 40))
            msg3 = font.render("Mod Avansat: Purple moving", True, (10, 40, 40))
            screen.blit(msg1, (self.width // 2 - msg1.get_width() // 2, self.height // 2 - 50))
            screen.blit(msg2, (self.width // 2 - msg2.get_width() // 2, self.height // 2 - 10))
            screen.blit(msg3, (self.width // 2 - msg3.get_width() // 2, self.height // 2 + 30))
        elif self.state == GAME_OVER:
            msg1 = font.render("Game Over", True, (10, 40, 40))
            msg2 = font.render("Press R or Restart", True, (10, 40, 40))
            screen.blit(msg1, (self.width // 2 - msg1.get_width() // 2, self.height // 2 - 40))
            screen.blit(msg2, (self.width // 2 - msg2.get_width() // 2, self.height // 2 + 5))

        if self.show_info:
            self._draw_info_overlay(screen)
