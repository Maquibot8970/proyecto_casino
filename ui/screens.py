import pygame 

class MenuScreen:
    def __init__(self,font):
        self.font = font
        self.buttons = {          #(x,y,width,height)
        "aviator":pygame.Rect(100,300,200,150),
        "blackjack":pygame.Rect(400,300,200,150),
        "poker":pygame.Rect(700,300,200,150),
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

    def handle_click(self,pos,game_data):
        for game, rect in self.buttons.items():
            if rect.collidepoint(pos) : #choice free game
                if not game_data["has_made_first_choice"]:
                    game_data["unlocked_games"][game] = True
                    game_data["has_made_first_choice"] = True
                    if game == "aviator":
                        return "STARTING_AVIATOR"
                    return f"entering {game}"
                
                
                if game_data["unlocked_games"].get(game, False):
                    if game == "aviator":
                        return "STARTING_AVIATOR"
                    return f"launching {game.upper()}"
                
                # purchase
                if game_data["cash"] >= 500:
                    game_data["cash"] -= 500
                    game_data["unlocked_games"][game] = True
                    return f"{game.capitalize()} purchased"
                else:
                    return "Not enough cash. Need $500 to unlock."
            return None
