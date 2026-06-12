import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from data import save_manager
from ui.screens import *
from games.aviator import AviatorGame

pygame.init()
save_manager.load() #cargamos datos

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    font = pygame.font.SysFont("Arial",30) #fuente y tamaño
    start_screen = GameMenuScreen(font)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                result = start_screen.handle_click(event.pos)
                if result == "AVIATOR":
                   
                    pass
                elif result == "POKER":
               
                    pass
                elif result == "BLACKJACK":
                    
                    pass

        start_screen.draw(screen)
        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()