import pygame
from bird import Bird
from pipe import PipePair
from score import ScoreManager

START, PLAYING, GAME_OVER = 0, 1, 2

class Game:
    def __init__(self,width: int, height: int):
        self.width = width
        self.height = height

        self.bird = Bird(100, height // 2)
        self.pipes: list[PipePair] = []

        self.score=0
        self.pipe_gap=160
        self.pipe_width=70
        self.pipe_speed=3.0

        self.state= START
        self.score_manager= ScoreManager()

        self.spawn_every_ms=1400
        self.last_spawn_ms = 0

    def reset(self) -> None:
        self.bird.reset(100, self.height // 2)
        self.pipes.clear()
        self.score=0
        self.pipe_gap=160
        self.state= START
        self.pipe_speed
        self.last_spawn_ms = 0
        self.state=PLAYING

    def maybe_spawn_pipe(self, now_ms: int) -> None:
        if self.last_spawn_ms==0 or now_ms -self.last_spawn_ms >=self.spawn_every_ms:
            self.pipes.append(PipePair(self.width, self.height, self.pipe_gap, self.pipe_width))
            self.last_spawn_ms = now_ms

    def update_difificulty(self) -> None:
        if self.score >0 and self.score % 5 ==0:
            self.pipe_speed -min(self.pipe_speed +0.02, 8.0)
            self.pipe_gap = max(120, self.pipe_gap -1)

    def update_playing(self, now_ms: int) -> None:
        self.maybe_spawn_pipe(now_ms)
        self.bird.update()

        for pipe in self.pipes:
            pipe.update(self.pipe_speed)

            if pipe.collide(self.bird.rect):
                self.state=GAME_OVER
                self.score_manager.try_update_high_score(self.score)
                return
            
            if not pipe.passed and pipe.is_passed_by(self.bird.rect):
                pipe.passed = True
                self.score += 1
                self.update_difificulty()

            if pipe.off_screen():
                self.pipes.remove(pipe)
            
        if self.bird.rect.top < 0 or self.bird.rect.bottom > self.height:
            self.state = GAME_OVER
            self.score_manager.try_update_high_score(self.score)

    def draw(self, screen: pygame.Surface, font) -> None:
       
        screen.fill((135, 206, 235))

        for pipe in self.pipes:
            pipe.draw(screen)

        self.bird.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(f"High Score: {self.score_manager.high_score}", True, (0, 0, 0))
        screen.blit(high_score_text, (10, 40))

        if self.state == START:
            msg1 = font.render("Press SPACE to Start", True, (0, 0, 0))
            screen.blit(msg1, (self.width // 2 - msg1.get_width() // 2, self.height // 2 - 30))
        elif self.state == GAME_OVER:
            msg1= font.render("Game Over", True, (0, 0, 0))
            msg2= font.render("Press R to Restart", True, (0, 0, 0))
            screen.blit(msg1, (self.width // 2 - msg1.get_width() // 2, self.height // 2 - 40))
            screen.blit(msg2, (self.width // 2 - msg2.get_width() // 2, self.height // 2 + 5))