import pygame
from data import save_manager
from ui.screens import MenuScreen, StartMenuScreen
from games.aviator import AviatorGame

pygame.init()
save_manager.load() #cargamos datos

screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",30) #fuente y tamaño

menu = MenuScreen(font)
aviator = AviatorGame(font)
current_state = "START_MENU"
running = True
start_menu = StartMenuScreen(font)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = event.pos
            result = start_menu.handle_click(click_pos)
            if result == "START":
                current_state = "MENU"
            elif result == "SETTINGS":
                current_state = "SETTINGS_MENU"

    screen.fill((28, 5, 8))

    if current_state == "START_MENU":
        start_menu.draw(screen)

    pygame.display.flip()
    clock.tick(60)  #60 fps

pygame.quit()