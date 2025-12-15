import pygame
from game import Game, START, PLAYING, GAME_OVER

WIDTH=420
HEIGHT=650
FPS=60

def main():
    pygame.init()
    screen=pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    font=pygame.font.SysFont(None, 32)

    game=Game(WIDTH, HEIGHT)

    running=True
    while running:
        now_ms=pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if game.state==START:
                        game.reset()
                    elif game.state==PLAYING and not game.show_info:
                        game.bird.jump()
                elif event.key==pygame.K_RETURN:
                    if game.state==PLAYING and not game.show_info:
                        game.bird.strong_jump()

                elif event.key==pygame.K_r and game.state==GAME_OVER:
                    game.reset()
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                game.handle_click(event.pos)
                

        if game.state==PLAYING and not game.show_info:
            game.update_playing(now_ms)

        game.draw(screen, font)

        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    main()
