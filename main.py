import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from data import save_manager
from data import audio_manager
from ui.screens import *
from games.aviator import AviatorGame
from games.blackjack import BlackjackGame

pygame.init()
save_manager.load() #cargamos datos

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    font = pygame.font.SysFont("Arial", 30) #fuente y tamaño
    
    # Inicializar audio
    audio_manager.init(save_manager.game_data)
    
    start_menu = StartMenuScreen(font)
    game_menu = GameMenuScreen(font)
    settings_menu = SettingsMenuScreen(font)
    leaderboard_screen = LeaderboardScreen(font)
    game_over_screen = GameOverScreen(font)
    aviator = AviatorGame(font)
    blackjack = BlackjackGame(font)
    
    current_state = "START_MENU"
    clock = pygame.time.Clock()
    running = True
    
    while running:
        
        if save_manager.game_data["cash"] > save_manager.game_data.get("max_cash", 1000):
            save_manager.game_data["max_cash"] = save_manager.game_data["cash"]
            
     
        if save_manager.game_data["cash"] <= 0 and current_state not in ["GAME_OVER", "START_MENU"]:
            current_state = "GAME_OVER"
            game_over_screen.setup(save_manager.game_data.get("max_cash", 1000))

        for event in pygame.event.get():
            if event.type == QUIT:
                save_manager.save()
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_state in ["GAME_MENU", "SETTINGS_MENU", "LEADERBOARD"]:
                        audio_manager.play_click(save_manager.game_data)
                    if current_state == "GAME_MENU":
                        current_state = "START_MENU"
                    elif current_state == "SETTINGS_MENU":
                        current_state = "START_MENU"
                    elif current_state == "LEADERBOARD":
                        current_state = "SETTINGS_MENU"
                        
            elif event.type == MOUSEBUTTONDOWN:
                if current_state == "START_MENU":
                    result = start_menu.handle_click(event.pos)
                    if result:
                        audio_manager.play_click(save_manager.game_data)
                        if result == "GAME_MENU":
                            current_state = "GAME_MENU"
                        elif result == "SETTINGS":
                            current_state = "SETTINGS_MENU"
                        elif result == "EXIT":
                            save_manager.save()
                            running = False
                elif current_state == "SETTINGS_MENU":
                    result = settings_menu.handle_click(event.pos, save_manager.game_data)
                    if result:
                        audio_manager.play_click(save_manager.game_data)
                        if result == "BACK":
                            current_state = "START_MENU"
                            save_manager.save()
                        elif result == "LEADERBOARD":
                            current_state = "LEADERBOARD"
                        elif result in ["TOGGLE_MUSIC", "TOGGLE_SFX"]:
                            audio_manager.update_music_state(save_manager.game_data)
                            save_manager.save()
                elif current_state == "LEADERBOARD":
                    result = leaderboard_screen.handle_click(event.pos)
                    if result:
                        audio_manager.play_click(save_manager.game_data)
                        if result == "BACK":
                            current_state = "SETTINGS_MENU"
                elif current_state == "GAME_MENU":
                    result = game_menu.handle_click(event.pos, save_manager.game_data)
                    if result:
                        audio_manager.play_click(save_manager.game_data)
                        if result == "AVIATOR":
                            current_state = "AVIATOR"
                        elif result == "POKER":
                            pass
                        elif result == "BLACKJACK":
                            current_state = "BLACKJACK"
            
  
            if current_state == "AVIATOR":
                state_signal = aviator.handle_event(event, save_manager.game_data)
                if state_signal == "MENU":
                    audio_manager.play_click(save_manager.game_data)
                    current_state = "GAME_MENU"
                    save_manager.save()
            elif current_state == "BLACKJACK":
                state_signal = blackjack.handle_event(event, save_manager.game_data)
                if state_signal == "MENU":
                    audio_manager.play_click(save_manager.game_data)
                    current_state = "GAME_MENU"
                    save_manager.save()
            elif current_state == "GAME_OVER":
                state_signal = game_over_screen.handle_event(event, save_manager.game_data)
                if state_signal == "SUBMITTED":
                    audio_manager.play_click(save_manager.game_data)
                    current_state = "START_MENU"
                    save_manager.save()
 
  
        if current_state == "AVIATOR":
            aviator.update()
 
       
        if current_state == "START_MENU":
            start_menu.draw(screen)
        elif current_state == "GAME_MENU":
            game_menu.draw(screen, save_manager.game_data)
        elif current_state == "SETTINGS_MENU":
            settings_menu.draw(screen, save_manager.game_data)
        elif current_state == "LEADERBOARD":
            leaderboard_screen.draw(screen, save_manager.game_data)
        elif current_state == "GAME_OVER":
            game_over_screen.draw(screen)
        elif current_state == "AVIATOR":
            aviator.draw(screen)
        elif current_state == "BLACKJACK":
            blackjack.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()