import pygame
import random

class PipePair:
    def __init__(self, x: int, screen_h: int, gap: int, width: int):
        margin=80
        top_h= random.randint(margin, screen_h - gap - margin)

        self.top=pygame.Rect(x, 0, width, top_h)
        self.bottom=pygame.Rect(x, top_h+gap, width, screen_h -(top_h+gap))

        self.passed=False
    def update(self, speed: float)->None:
        dx=int(speed)
        self.top.x -= dx
        self.bottom.x -= dx

    def draw(self, screen: pygame.Surface)->None:
        pygame.draw.rect(screen, (0,190,0), self.top)
        pygame.draw.rect(screen, (0,190,0), self.bottom)

    def off_screen(self)->bool:
        return self.top.right <0
    
    def collide(self, bird_rect: pygame.Rect)->bool:
        return self.top.colliderect(bird_rect) or self.bottom.colliderect(bird_rect)
    
    def is_passed_by(self, bird_rect: pygame.Rect)->bool:
       return self.top.right < bird_rect.left