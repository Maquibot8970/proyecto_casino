import pygame 

class MenuScreen:
    def __init__(self,font):
        self.font = font
    self.buttons = {          #(x,y,width,height)
        "aviator":pygame.rect(100,300,200,150),
        "blackjack":pygame.rect(100,300,200,150),
        "poker":pygame.rect(100,300,200,150),
    }

    def draw (self,screen,game_data):
        screen.fill((100,25,24))

        #color
        for game,rect in self.buttons.items():
            is_unlocked = game_data["unlocked_games"][game]
            color = (0,200,0) if is_unlocked else (50,50,50)

            pygame.draw.rect(screen,color,rect)

            #button text
            label = self.font.render(game.capitalize (),True, (255,255,255))
            screen.blit(label,(rect.x + 20, rect.y +60))

