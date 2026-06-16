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
        self.play_button_rect = pygame.Rect(380, 280, 240, 60)
        self.settings_button_rect = pygame.Rect(380, 360, 240, 60)
        self.exit_button_rect = pygame.Rect(380, 440, 240, 60)

    def draw(self, screen):
       
        screen.fill((28, 5, 8))
        
     
        pygame.draw.line(screen, (163, 22, 43), (0, 120), (1000, 120), 4)
        
    
        title_surf = self.title_font.render("CASINO", True, (247, 202, 24))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 45))

        
        mouse_pos = pygame.mouse.get_pos()
        is_hovered_play = self.play_button_rect.collidepoint(mouse_pos)
        is_hovered_settings = self.settings_button_rect.collidepoint(mouse_pos)
        is_hovered_exit = self.exit_button_rect.collidepoint(mouse_pos)
        
        bg_color_play = (163, 22, 43) if is_hovered_play else (84, 11, 22)
        border_color_play = (247, 202, 24) if is_hovered_play else (130, 90, 40)
        text_color_play = (255, 255, 255) if is_hovered_play else (220, 220, 220)
        
        bg_color_settings = (163, 22, 43) if is_hovered_settings else (84, 11, 22)
        border_color_settings = (247, 202, 24) if is_hovered_settings else (130, 90, 40)
        text_color_settings = (255, 255, 255) if is_hovered_settings else (220, 220, 220)

        bg_color_exit = (163, 22, 43) if is_hovered_exit else (84, 11, 22)
        border_color_exit = (247, 202, 24) if is_hovered_exit else (130, 90, 40)
        text_color_exit = (255, 255, 255) if is_hovered_exit else (220, 220, 220)
        
        pygame.draw.rect(screen, bg_color_play, self.play_button_rect, border_radius=10)
        pygame.draw.rect(screen, border_color_play, self.play_button_rect, width=2, border_radius=10)
        text_surf_play = self.button_font.render("Iniciar", True, text_color_play)
        screen.blit(text_surf_play, (
            self.play_button_rect.x + (self.play_button_rect.width - text_surf_play.get_width()) // 2,
            self.play_button_rect.y + (self.play_button_rect.height - text_surf_play.get_height()) // 2
        ))
        
        pygame.draw.rect(screen, bg_color_settings, self.settings_button_rect, border_radius=10)
        pygame.draw.rect(screen, border_color_settings, self.settings_button_rect, width=2, border_radius=10)
        text_surf_settings = self.button_font.render("Configuración", True, text_color_settings)
        screen.blit(text_surf_settings, (
            self.settings_button_rect.x + (self.settings_button_rect.width - text_surf_settings.get_width()) // 2,
            self.settings_button_rect.y + (self.settings_button_rect.height - text_surf_settings.get_height()) // 2
        ))

        pygame.draw.rect(screen, bg_color_exit, self.exit_button_rect, border_radius=10)
        pygame.draw.rect(screen, border_color_exit, self.exit_button_rect, width=2, border_radius=10)
        text_surf_exit = self.button_font.render("Salir", True, text_color_exit)
        screen.blit(text_surf_exit, (
            self.exit_button_rect.x + (self.exit_button_rect.width - text_surf_exit.get_width()) // 2,
            self.exit_button_rect.y + (self.exit_button_rect.height - text_surf_exit.get_height()) // 2
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
        self.button_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.music_button = pygame.Rect(380, 240, 240, 60)
        self.sound_button = pygame.Rect(380, 320, 240, 60)
        self.leaderboard_button = pygame.Rect(380, 400, 240, 60)
        self.back_button = pygame.Rect(380, 480, 240, 60)

    def draw(self, screen, game_data):
        screen.fill((28, 5, 8))
        
        # Title
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title_surf = title_font.render("Configuración", True, (247, 202, 24))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 45))
        pygame.draw.line(screen, (163, 22, 43), (0, 120), (1000, 120), 4)
        
        mouse_pos = pygame.mouse.get_pos()
     
        buttons = [
            ("music", self.music_button, "Música: ACTIVADA" if game_data.get("music_enabled", True) else "Música: DESACTIVADA"),
            ("sound", self.sound_button, "Sonido: ACTIVADO" if game_data.get("sound_enabled", True) else "Sonido: DESACTIVADO"),
            ("leaderboard", self.leaderboard_button, "Ver Leaderboard"),
            ("back", self.back_button, "Volver")
        ]
        
        for name, rect, text in buttons:
            is_hovered = rect.collidepoint(mouse_pos)
            bg_color = (163, 22, 43) if is_hovered else (84, 11, 22)
            border_color = (247, 202, 24) if is_hovered else (130, 90, 40)
            text_color = (255, 255, 255) if is_hovered else (220, 220, 220)
            
            pygame.draw.rect(screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(screen, border_color, rect, width=2, border_radius=10)
            
            text_surf = self.button_font.render(text, True, text_color)
            screen.blit(text_surf, (
                rect.x + (rect.width - text_surf.get_width()) // 2,
                rect.y + (rect.height - text_surf.get_height()) // 2
            ))

    def handle_click(self, pos, game_data):
        if self.music_button.collidepoint(pos):
            game_data["music_enabled"] = not game_data.get("music_enabled", True)
            return "TOGGLE_MUSIC"
        elif self.sound_button.collidepoint(pos):
            game_data["sound_enabled"] = not game_data.get("sound_enabled", True)
            return "TOGGLE_SFX"
        elif self.leaderboard_button.collidepoint(pos):
            return "LEADERBOARD"
        elif self.back_button.collidepoint(pos):
            return "BACK"
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

        self.aviator_button_rect = pygame.Rect(150, 250, 120, 140)
        self.poker_button_rect = pygame.Rect(440, 250, 120, 140)
        self.blackjack_button_rect = pygame.Rect(730, 250, 120, 140)
        self.restart_button_rect = pygame.Rect(20, 20, 120, 40)
        self.button_font = pygame.font.SysFont("Arial", 22, bold=True)

    def draw(self, screen, game_data):
        screen.fill((28, 5, 8))
        
        
        cash_surf = self.font.render(f"Dinero: ${game_data['cash']}", True, (247, 202, 24))
        screen.blit(cash_surf, (1000 - cash_surf.get_width() - 50, 50))
        
        unlocked = game_data["unlocked_games"]

        if self.aviator_image:
            screen.blit(self.aviator_image, self.aviator_button_rect)
            title_surf = self.font.render("AVIATOR", True, (247, 202, 24))
            screen.blit(title_surf, (self.aviator_button_rect.centerx - title_surf.get_width() // 2, self.aviator_button_rect.bottom + 10))
            status_str = "Desbloqueado" if unlocked.get("aviator") else "Bloqueado ($500)"
            status_color = (0, 255, 0) if unlocked.get("aviator") else (200, 50, 50)
            status_surf = self.font.render(status_str, True, status_color)
            screen.blit(status_surf, (self.aviator_button_rect.centerx - status_surf.get_width() // 2, self.aviator_button_rect.bottom + 45))

        if self.poker_image:
            screen.blit(self.poker_image, self.poker_button_rect)
            title_surf = self.font.render("POKER", True, (247, 202, 24))
            screen.blit(title_surf, (self.poker_button_rect.centerx - title_surf.get_width() // 2, self.poker_button_rect.bottom + 10))
            status_str = "Desbloqueado" if unlocked.get("poker") else "Bloqueado ($500)"
            status_color = (0, 255, 0) if unlocked.get("poker") else (200, 50, 50)
            status_surf = self.font.render(status_str, True, status_color)
            screen.blit(status_surf, (self.poker_button_rect.centerx - status_surf.get_width() // 2, self.poker_button_rect.bottom + 45))

        if self.blackjack_image:
            screen.blit(self.blackjack_image, self.blackjack_button_rect)
            title_surf = self.font.render("BLACKJACK", True, (247, 202, 24))
            screen.blit(title_surf, (self.blackjack_button_rect.centerx - title_surf.get_width() // 2, self.blackjack_button_rect.bottom + 10))
            status_str = "Desbloqueado" if unlocked.get("blackjack") else "Bloqueado ($500)"
            status_color = (0, 255, 0) if unlocked.get("blackjack") else (200, 50, 50)
            status_surf = self.font.render(status_str, True, status_color)
            screen.blit(status_surf, (self.blackjack_button_rect.centerx - status_surf.get_width() // 2, self.blackjack_button_rect.bottom + 45))

        title_surf = self.font.render("Elije tu juego", True, (247, 202, 24))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 50))
        
        mouse_pos = pygame.mouse.get_pos()
        is_hovered_restart = self.restart_button_rect.collidepoint(mouse_pos)
        bg_color = (163, 22, 43) if is_hovered_restart else (84, 11, 22)
        pygame.draw.rect(screen, bg_color, self.restart_button_rect, border_radius=10)
        pygame.draw.rect(screen, (247, 202, 24), self.restart_button_rect, width=2, border_radius=10)
        restart_surf = self.button_font.render("Reiniciar", True, (255, 255, 255))
        screen.blit(restart_surf, (self.restart_button_rect.x + (self.restart_button_rect.width - restart_surf.get_width()) // 2, self.restart_button_rect.y + (self.restart_button_rect.height - restart_surf.get_height()) // 2))

    def handle_click(self, pos, game_data):
        if self.restart_button_rect.collidepoint(pos):
            return "RESTART"
            
        unlocked = game_data["unlocked_games"]
        for game_key, rect, result_key in [
            ("aviator", self.aviator_button_rect, "AVIATOR"),
            ("poker", self.poker_button_rect, "POKER"),
            ("blackjack", self.blackjack_button_rect, "BLACKJACK")
        ]:
            if rect.collidepoint(pos):
                if unlocked.get(game_key, False):
                    return result_key
                elif game_data["cash"] >= 500:
                    game_data["cash"] -= 500
                    unlocked[game_key] = True
                    return result_key
        return None


class LeaderboardScreen:
    def __init__(self, font):
        self.font = font
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.header_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.back_button = pygame.Rect(380, 600, 240, 60)

    def draw(self, screen, game_data):
        screen.fill((28, 5, 8))
        
        # Title
        title_surf = self.title_font.render("LEADERBOARD", True, (247, 202, 24))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 45))
        pygame.draw.line(screen, (163, 22, 43), (0, 120), (1000, 120), 4)
        
        # Headers
        rank_header = self.header_font.render("RANGO", True, (247, 202, 24))
        name_header = self.header_font.render("NOMBRE", True, (247, 202, 24))
        score_header = self.header_font.render("MÁX. DINERO", True, (247, 202, 24))
        
        screen.blit(rank_header, (200, 160))
        screen.blit(name_header, (400, 160))
        screen.blit(score_header, (650, 160))
        
        pygame.draw.line(screen, (130, 90, 40), (150, 200), (850, 200), 2)
        
        # Draw top 5 scores
        leaderboard = game_data.get("leaderboard", [])
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x.get("score", 0), reverse=True)[:5]
        
        y_pos = 220
        for i, entry in enumerate(sorted_leaderboard):
            rank_surf = self.font.render(f"#{i+1}", True, (255, 255, 255))
            name_surf = self.font.render(entry.get("name", "N/A"), True, (255, 255, 255))
            score_surf = self.font.render(f"${entry.get('score', 0)}", True, (255, 255, 255))
            
            screen.blit(rank_surf, (220, y_pos))
            screen.blit(name_surf, (400, y_pos))
            screen.blit(score_surf, (680, y_pos))
            y_pos += 60
            
        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.back_button.collidepoint(mouse_pos)
        bg_color = (163, 22, 43) if is_hovered else (84, 11, 22)
        border_color = (247, 202, 24) if is_hovered else (130, 90, 40)
        text_color = (255, 255, 255) if is_hovered else (220, 220, 220)
        
        pygame.draw.rect(screen, bg_color, self.back_button, border_radius=10)
        pygame.draw.rect(screen, border_color, self.back_button, width=2, border_radius=10)
        
        text_surf = self.font.render("Volver", True, text_color)
        screen.blit(text_surf, (
            self.back_button.x + (self.back_button.width - text_surf.get_width()) // 2,
            self.back_button.y + (self.back_button.height - text_surf.get_height()) // 2
        ))

    def handle_click(self, pos):
        if self.back_button.collidepoint(pos):
            return "BACK"
        return None


class GameOverScreen:
    def __init__(self, font):
        self.font = font
        self.title_font = pygame.font.SysFont("Arial", 55, bold=True)
        self.name = ""
        self.max_cash = 1000

    def setup(self, max_cash):
        self.max_cash = max_cash
        self.name = ""

    def draw(self, screen):
        screen.fill((28, 5, 8))
        
        # Title Game Over
        title_surf = self.title_font.render("FIN DEL JUEGO", True, (200, 50, 50))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 150))
        
        msg_surf = self.font.render("Te has quedado sin dinero.", True, (220, 220, 220))
        screen.blit(msg_surf, (1000 // 2 - msg_surf.get_width() // 2, 250))
        
        score_surf = self.font.render(f"Máximo dinero conseguido: ${self.max_cash}", True, (247, 202, 24))
        screen.blit(score_surf, (1000 // 2 - score_surf.get_width() // 2, 310))
        
        prompt_surf = self.font.render("Ingresa tu nombre para guardar récord:", True, (220, 220, 220))
        screen.blit(prompt_surf, (1000 // 2 - prompt_surf.get_width() // 2, 400))
        
        # Render input box
        input_box = pygame.Rect(300, 460, 400, 60)
        pygame.draw.rect(screen, (84, 11, 22), input_box, border_radius=10)
        pygame.draw.rect(screen, (247, 202, 24), input_box, width=2, border_radius=10)
        
        name_surf = self.font.render(self.name + "|", True, (255, 255, 255))
        screen.blit(name_surf, (input_box.x + 20, input_box.y + (input_box.height - name_surf.get_height()) // 2))
        
        enter_surf = self.font.render("Presiona ENTER para guardar y continuar", True, (130, 90, 40))
        screen.blit(enter_surf, (1000 // 2 - enter_surf.get_width() // 2, 560))

    def handle_event(self, event, game_data):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(self.name.strip()) > 0:
                    player_name = self.name.strip()
                
                    leaderboard = game_data.get("leaderboard", [])
                    leaderboard.append({"name": player_name, "score": self.max_cash})
                    
                    leaderboard.sort(key=lambda x: x.get("score", 0), reverse=True)
                    game_data["leaderboard"] = leaderboard[:10]
                    
               
                    game_data["cash"] = 1000
                    game_data["max_cash"] = 1000
                    game_data["has_made_first_choice"] = False
                    for game in game_data["unlocked_games"]:
                        game_data["unlocked_games"][game] = False
                    
                    return "SUBMITTED"
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            else:
             
                if len(self.name) < 15 and (event.unicode.isalnum() or event.unicode in [' ', '_', '-']):
                    self.name += event.unicode
        return None
