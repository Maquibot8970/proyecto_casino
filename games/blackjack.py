import pygame
from games.cartas import Baraja

class Mano:
    def __init__(self):
        self.cartas = []
        self.puntos = 0
        self.ases = 0

    def agregar_carta(self, carta):
        self.cartas.append(carta)
        
        # Lógica de asignación de puntos
        if carta.valor in ['J', 'Q', 'K']:
            self.puntos += 10
        elif carta.valor == 'A':
            self.puntos += 11
            self.ases += 1
        else:
            self.puntos += int(carta.valor)

        # Ajuste automático del As (Salvavidas)
        while self.puntos > 21 and self.ases > 0:
            self.puntos -= 10
            self.ases -= 1

    def esta_pasado(self):
        """Retorna True si la mano supera los 21 puntos."""
        return self.puntos > 21

    def tiene_blackjack(self):
        """Retorna True si tiene exactamente 21 puntos."""
        return self.puntos == 21

    def mostrar_mano(self, oculta=False):
        """
        Retorna una cadena con las cartas. 
        Si 'oculta' es True, solo muestra la primera carta (útil para el crupier).
        """
        if oculta and len(self.cartas) > 0:
            return f"[{self.cartas[0]}, <Carta Oculta>]"
        
        nombres = [str(c) for c in self.cartas]
        return f"{' , '.join(nombres)} | Total: {self.puntos}"


class BlackjackGame:
    def __init__(self, font):
        self.font = font
        self.big_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.reset_game()

    def reset_game(self):
        self.deck = None
        self.player_hand = None
        self.dealer_hand = None
        self.bet_amount = 50
        self.status = "BETTING" # "BETTING", "PLAYING", "DEALER_TURN", "ROUND_OVER"
        self.outcome = ""
        self.win_amount = 0

    def start_round(self, game_data):
        if game_data["cash"] >= self.bet_amount:
            game_data["cash"] -= self.bet_amount
            self.deck = Baraja()
            self.deck.revolver()
            self.player_hand = Mano()
            self.dealer_hand = Mano()
            
            # Repartir
            self.player_hand.agregar_carta(self.deck.dar_carta())
            self.dealer_hand.agregar_carta(self.deck.dar_carta())
            self.player_hand.agregar_carta(self.deck.dar_carta())
            self.dealer_hand.agregar_carta(self.deck.dar_carta())
            
            if self.player_hand.tiene_blackjack():
                self.status = "DEALER_TURN"
                self.resolve_dealer_turn(game_data)
            else:
                self.status = "PLAYING"

    def hit(self):
        if self.status == "PLAYING":
            self.player_hand.agregar_carta(self.deck.dar_carta())
            if self.player_hand.esta_pasado():
                self.status = "ROUND_OVER"
                self.outcome = "¡Te pasaste de 21! Perdiste."
                self.win_amount = 0

    def stand(self, game_data):
        if self.status == "PLAYING":
            self.status = "DEALER_TURN"
            self.resolve_dealer_turn(game_data)

    def resolve_dealer_turn(self, game_data):
        # El crupier saca cartas hasta tener 17 o más
        while self.dealer_hand.puntos < 17:
            self.dealer_hand.agregar_carta(self.deck.dar_carta())
            
        self.status = "ROUND_OVER"
        if self.dealer_hand.esta_pasado():
            self.outcome = "¡El crupier se pasó! Ganaste."
            self.win_amount = self.bet_amount * 2
        else:
            if self.player_hand.puntos > self.dealer_hand.puntos:
                self.outcome = "¡Ganaste!"
                self.win_amount = self.bet_amount * 2
            elif self.player_hand.puntos < self.dealer_hand.puntos:
                self.outcome = "Perdiste contra el crupier."
                self.win_amount = 0
            else:
                self.outcome = "Empate (Push)."
                self.win_amount = self.bet_amount
                
        game_data["cash"] += self.win_amount

    def draw(self, screen):
        screen.fill((20, 60, 30)) # Verde mesa de casino
        
        # Título
        title_surf = self.big_font.render("BLACKJACK", True, (247, 202, 24))
        screen.blit(title_surf, (1000 // 2 - title_surf.get_width() // 2, 30))
        
        if self.status == "BETTING":
            # Elegir apuesta
            bet_surf = self.font.render(f"Apuesta actual: ${self.bet_amount}", True, (255, 255, 255))
            screen.blit(bet_surf, (1000 // 2 - bet_surf.get_width() // 2, 300))
            
            info_surf = self.font.render("Usa las flechas ARRIBA/ABAJO para cambiar la apuesta", True, (200, 200, 200))
            screen.blit(info_surf, (1000 // 2 - info_surf.get_width() // 2, 360))
            
            play_surf = self.font.render("Presiona ESPACIO para jugar", True, (247, 202, 24))
            screen.blit(play_surf, (1000 // 2 - play_surf.get_width() // 2, 420))
            
        else:
            
            dealer_title = self.font.render("Crupier:", True, (247, 202, 24))
            screen.blit(dealer_title, (100, 150))
            
            oculta = (self.status == "PLAYING")
            dealer_hand_str = self.dealer_hand.mostrar_mano(oculta=oculta)
            dealer_hand_surf = self.font.render(dealer_hand_str, True, (255, 255, 255))
            screen.blit(dealer_hand_surf, (100, 200))
            
        
            player_title = self.font.render("Tus Cartas:", True, (247, 202, 24))
            screen.blit(player_title, (100, 350))
            
            player_hand_str = self.player_hand.mostrar_mano(oculta=False)
            player_hand_surf = self.font.render(player_hand_str, True, (255, 255, 255))
            screen.blit(player_hand_surf, (100, 400))
            
           
            bet_surf = self.font.render(f"Apuesta: ${self.bet_amount}", True, (200, 200, 200))
            screen.blit(bet_surf, (100, 520))
            
            if self.status == "PLAYING":
                cmd_surf = self.font.render("Presiona H para Pedir S para Plantarse ", True, (247, 202, 24))
                screen.blit(cmd_surf, (100, 600))
            elif self.status == "ROUND_OVER":
                outcome_surf = self.font.render(self.outcome, True, (255, 255, 255))
                screen.blit(outcome_surf, (100, 570))
                
                again_surf = self.font.render("Presiona ESPACIO para volver a apostar", True, (247, 202, 24))
                screen.blit(again_surf, (100, 630))

       
        esc_surf = self.font.render("Pulsar ESC para volver al menú de juegos", True, (200, 200, 200))
        screen.blit(esc_surf, (20, 740))

    def handle_event(self, event, game_data):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.reset_game()
                return "MENU"
                
            if self.status == "BETTING":
                if event.key == pygame.K_UP:
                    self.bet_amount = min(game_data["cash"], self.bet_amount + 10)
                elif event.key == pygame.K_DOWN:
                    self.bet_amount = max(10, self.bet_amount - 10)
                elif event.key == pygame.K_SPACE:
                    self.start_round(game_data)
                    
            elif self.status == "PLAYING":
                if event.key == pygame.K_h:
                    self.hit()
                elif event.key == pygame.K_s:
                    self.stand(game_data)
                    
            elif self.status == "ROUND_OVER":
                if event.key == pygame.K_SPACE:
                    self.status = "BETTING"
              
                    if self.bet_amount > game_data["cash"]:
                        self.bet_amount = max(10, game_data["cash"])
                        
        return "BLACKJACK"