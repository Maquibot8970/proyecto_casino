import pygame
from data import save_manager
from ui.screens import MenuScreen
from games.aviator import AviatorGame

pygame.init()
save_manager.load() #cargamos datos

screen = pygame.display.set_mode((1000,800))
pygame.display.set_caption ("casino")
font = pygame.font.SysFont("Arial",30) #fuente y tamaño

menu = MenuScreen(font)
aviator = AviatorGame(font)
current_state = "Menu"
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT: #comprobamos si se da a la x en ventana y guardamos
            save_manager.save()
            running = False

        if current_state == "Menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                result = menu.handle_click(event.pos, save_manager.game_data)
                if result == "STARTING_AVIATOR": 
                    current_state = "AVIATOR"
                save_manager.save()
        
        elif current_state == "AVIATOR":
            aviator.update()
            state_signal = aviator.handle_event(event, save_manager.game_data)
            if state_signal == "MENU":
                current_state = "Menu"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            result = menu.handle_click(event.pos, save_manager.game_data)

            if result:
                print(result)
                save_manager.save() 

    if current_state == "Menu":  
        menu.draw(screen, save_manager.game_data)
    elif current_state == "AVIATOR":
        aviator.update()
        aviator.draw(screen)

    pygame.display.flip()

pygame.quit()
