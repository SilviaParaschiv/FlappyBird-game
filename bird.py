import os
import pygame

class Bird:
    def __init__(self, x: int, y: int):
        self.image = pygame.image.load(os.path.join("assets", "birdbun.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 46))
        self.rect = self.image.get_rect(center=(x, y))

        self.vel_y = 0.0
        self.gravity = 0.55
        self.jump_strength = -8.0

    def jump(self) -> None:
        self.vel_y = 0
        self.vel_y=self.jump_strength

    def update(self) -> None:
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += int(self.vel_y)

    def draw(self, screen: pygame.Surface) ->None:
        screen.blit(self.image, self.rect)

    def reset(self, x: int, y: int) -> None:
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0.0    
