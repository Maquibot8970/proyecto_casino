import pygame
from data import save_manager
from ui import screens

pygame.init()
save_manager.load #cargamos datos

screen = pygame.display.set_mode((1000,800))
pygame.display.set_caption ("casino")
font = pygame.font.SysFont("Arial",30) #fuente y tamaño

menu = screens(font)
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT: #comprobamos si se da a la x en ventana y guardamos
            save_manager.save()
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            result = screen.handle_click(event.pos, save_manager.game_data)

            if result:
                print(result)
                save_manager.save() 

    menu.draw(screen, save_manager.game_data)
    pygame.display.flip()

pygame.quit()
