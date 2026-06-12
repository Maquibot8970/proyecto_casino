import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from data import save_manager
from ui.screens import *
from games.aviator import AviatorGame

pygame.init()
save_manager.load() #cargamos datos

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    font = pygame.font.SysFont("Arial", 30) #fuente y tamaño
    
    start_menu = StartMenuScreen(font)
    game_menu = GameMenuScreen(font)
    settings_menu = SettingsMenuScreen(font)
    aviator = AviatorGame(font)
    
    current_state = "START_MENU"
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                save_manager.save()
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_state == "GAME_MENU":
                        current_state = "START_MENU"
                    elif current_state == "SETTINGS_MENU":
                        current_state = "START_MENU"
                        
            elif event.type == MOUSEBUTTONDOWN:
                if current_state == "START_MENU":
                    result = start_menu.handle_click(event.pos)
                    if result == "GAME_MENU":
                        current_state = "GAME_MENU"
                    elif result == "SETTINGS":
                        current_state = "SETTINGS_MENU"
                    elif result == "EXIT":
                        save_manager.save()
                        running = False
                elif current_state == "GAME_MENU":
                    result = game_menu.handle_click(event.pos)
                    if result == "AVIATOR":
                        current_state = "AVIATOR"
                    elif result == "POKER":
                        pass
                    elif result == "BLACKJACK":
                        pass
            
            # Si estamos en el juego Aviator, delegamos eventos
            if current_state == "AVIATOR":
                state_signal = aviator.handle_event(event, save_manager.game_data)
                if state_signal == "MENU":
                    current_state = "GAME_MENU"
                    save_manager.save()

        # Actualizaciones dinámicas
        if current_state == "AVIATOR":
            aviator.update()

        # Dibujo de la pantalla correspondiente
        if current_state == "START_MENU":
            start_menu.draw(screen)
        elif current_state == "GAME_MENU":
            game_menu.draw(screen)
        elif current_state == "SETTINGS_MENU":
            settings_menu.draw(screen)
        elif current_state == "AVIATOR":
            aviator.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()