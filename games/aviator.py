import pygame

class AviatorGame:
    def __init__(self, font):
        self.font = font
        self.active = False 

    def draw(self, screen):
        screen.fill((20, 20, 20)) 
        text = self.font.render("AVIATOR Press ESC to return to lobby", True, (255, 255, 255))
        screen.blit(text, (300, 380))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU" 
        return "AVIATOR"