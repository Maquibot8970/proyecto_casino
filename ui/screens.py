import pygame
from pygame.locals import *

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


class StartMenuScreen:
    def __init__(self, font):
        self.font = font
      
        self.title_font = pygame.font.SysFont("Arial", 65, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.play_button = pygame.Rect(380, 280, 240, 60)
        self.settings_button = pygame.Rect(380, 360, 240, 60)  

    def draw(self, screen):
       
        screen.fill((28, 5, 8))
        
     
        pygame.draw.line(screen, (163, 22, 43), (0, 120), (1000, 120), 4)
        
    
        title_surf = self.title_font.render("CASINO", True, (247, 202, 24))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 45))

        
        mouse_pos = pygame.mouse.get_pos()
        is_hovered_play = self.play_button.collidepoint(mouse_pos)
        is_hovered_settings = self.settings_button.collidepoint(mouse_pos)
        
        bg_color_play = (163, 22, 43) if is_hovered_play else (84, 11, 22)
        border_color_play = (247, 202, 24) if is_hovered_play else (130, 90, 40)
        text_color_play = (255, 255, 255) if is_hovered_play else (220, 220, 220)
        
        bg_color_settings = (163, 22, 43) if is_hovered_settings else (84, 11, 22)
        border_color_settings = (247, 202, 24) if is_hovered_settings else (130, 90, 40)
        text_color_settings = (255, 255, 255) if is_hovered_settings else (220, 220, 220)
        
        pygame.draw.rect(screen, bg_color_play, self.play_button, border_radius=10)
        pygame.draw.rect(screen, border_color_play, self.play_button, width=2, border_radius=10)
        text_surf_play = self.button_font.render("Iniciar", True, text_color_play)
        screen.blit(text_surf_play, (
            self.play_button.x + (self.play_button.width - text_surf_play.get_width()) // 2,
            self.play_button.y + (self.play_button.height - text_surf_play.get_height()) // 2
        ))
        
        pygame.draw.rect(screen, bg_color_settings, self.settings_button, border_radius=10)
        pygame.draw.rect(screen, border_color_settings, self.settings_button, width=2, border_radius=10)
        text_surf_settings = self.button_font.render("Configuración", True, text_color_settings)
        screen.blit(text_surf_settings, (
            self.settings_button.x + (self.settings_button.width - text_surf_settings.get_width()) // 2,
            self.settings_button.y + (self.settings_button.height - text_surf_settings.get_height()) // 2
        ))

    def handle_click(self, pos):
        if self.play_button_rect.collidepoint(pos):
            return "GAME_MENU"
        elif self.settings_button_rect.collidepoint(pos):
            return "SETTINGS"
        elif self.exit_button_rect.collidepoint(pos):
            return "EXIT"
        return None

class SettingsMenuScreen:
    def __init__(self, font):
        self.font = font

    def draw(self, screen):
        screen.fill((28, 5, 8))
        title_surf = self.font.render("Configuración", True, (247, 202, 24))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 45))

    def handle_click(self, pos):
        return None

class GameMenuScreen:
    def __init__(self, font):
        self.font = font
      
     
        self.image_path_aviator = "assets/images/aviator.png"
        self.image_path_poker = "assets/images/poker.png"
        self.image_path_blackjack = "assets/images/blackjack.png"

        self.aviator_image = pygame.image.load(self.image_path_aviator)
        self.poker_image = pygame.image.load(self.image_path_poker)
        self.blackjack_image = pygame.image.load(self.image_path_blackjack)


        self.aviator_image = pygame.transform.scale(self.aviator_image, (100, 100))
        self.poker_image = pygame.transform.scale(self.poker_image, (100, 100))
        self.blackjack_image = pygame.transform.scale(self.blackjack_image, (100, 100))

 
        self.aviator_button_rect = pygame.Rect(250, 200, 120, 140)
        self.poker_button_rect = pygame.Rect(600, 200, 120, 140)
        self.blackjack_button_rect = pygame.Rect(950, 200, 120, 140)

    def draw(self, screen):
        screen.fill((28, 5, 8))
        
   
        if self.aviator_image:
            screen.blit(self.aviator_image, self.aviator_button_rect)
            title_surf = self.font.render("AVIATOR", True, (247, 202, 24))
            screen.blit(title_surf, (self.aviator_button_rect.centerx - title_surf.get_width() // 2, self.aviator_button_rect.bottom + 10))

        if self.poker_image:
            screen.blit(self.poker_image, self.poker_button_rect)
            title_surf = self.font.render("POKER", True, (247, 202, 24))
            screen.blit(title_surf, (self.poker_button_rect.centerx - title_surf.get_width() // 2, self.poker_button_rect.bottom + 10))

        if self.blackjack_image:
            screen.blit(self.blackjack_image, self.blackjack_button_rect)
            title_surf = self.font.render("BLACKJACK", True, (247, 202, 24))
            screen.blit(title_surf, (self.blackjack_button_rect.centerx - title_surf.get_width() // 2, self.blackjack_button_rect.bottom + 10))

        title_surf = self.font.render("Elije tu juego", True, (247, 202, 24))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 50))


    def handle_click(self, pos):
        if self.aviator_button_rect.collidepoint(pos):
            return "AVIATOR"
        elif self.poker_button_rect.collidepoint(pos):
            return "POKER"
        elif self.blackjack_button_rect.collidepoint(pos):
            return "BLACKJACK"
        return None
