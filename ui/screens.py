import pygame 

class MenuScreen:
    def __init__(self,font):
        self.font = font
    self.buttons = {          #(x,y,width,height)
        "aviator":pygame.rect(100,300,200,150),
        "blackjack":pygame.rect(100,300,200,150),
        "poker":pygame.rect(100,300,200,150),
    }