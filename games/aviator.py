import pygame
import random
import time
import math

class AviatorGame:
    def __init__(self, font):
        self.font = font
        self.big_font = pygame.font.SysFont("Arial", 80, bold=True)
        self.reset_game()

    def reset_game(self):
       
        self.multiplier = 1.00
        self.start_time = 0
        self.crash_point = self.generate_crash_point()
        self.status = "WAITING" 
        self.bet_amount = 10
        self.win_amount = 0

    def generate_crash_point(self):
      
        return round(random.uniform(1.01, 10.0) ** random.uniform(1, 1.5), 2)

    def update(self):
        if self.status == "FLYING":
           
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            self.multiplier = round(1.00 * (1.07 ** elapsed), 2)

          
            if self.multiplier >= self.crash_point:
                self.multiplier = self.crash_point
                self.status = "CRASHED"

    def draw(self, screen):
        screen.fill((20, 20, 20)) 

        # multiplicador
        color = (255, 255, 255)
        if self.status == "CRASHED": color = (255, 0, 0)
        if self.status == "CASHED_OUT": color = (0, 255, 0)

        mult_text = self.big_font.render(f"{self.multiplier}x", True, color)
        screen.blit(mult_text, (400, 300))

       
        info = ""
        if self.status == "WAITING": info = "Presiona espacio para apostar $10"
        elif self.status == "FLYING": info = "Presiona enter para COBRAR"
        elif self.status == "CRASHED": info = "Perdiste espacio para reintentar"
        elif self.status == "CASHED_OUT": info = f"Ganaste ${self.win_amount}! presiona espacio para otra"

        info_text = self.font.render(info, True, (200, 200, 200))
        screen.blit(info_text, (300, 500))
        
 
        esc_text = self.font.render("ESC para volver al lobby", True, (100, 100, 100))
        screen.blit(esc_text, (20, 750))

    def handle_event(self, event, game_data):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.reset_game()
                return "MENU"

            
            if event.key == pygame.K_SPACE and self.status in ["WAITING", "CRASHED", "CASHED_OUT"]:
                if game_data["cash"] >= self.bet_amount:
                    game_data["cash"] -= self.bet_amount
                    self.reset_game()
                    self.start_time = pygame.time.get_ticks()
                    self.status = "FLYING"

           
            if event.key == pygame.K_RETURN and self.status == "FLYING":
                self.win_amount = int(self.bet_amount * self.multiplier)
                game_data["cash"] += self.win_amount
                self.status = "CASHED_OUT"

        return "AVIATOR"
