import pygame
from games.cartas import Baraja

VERDE = (20, 90, 40)
VERDE_OSC = (10, 60, 25)
GOLD = (247, 202, 24)
GOLD_DIM = (130, 90, 40)
DARK_RED = (84, 11, 22)
RED_HOV = (163, 22, 43)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
NEGRO = (20, 20, 20)


class Mano:
    def __init__(self):
        self.cartas = []
        self.puntos = 0
        self.ases = 0

    def agregar_carta(self, carta):
        self.cartas.append(carta)
        if carta.valor in ['J', 'Q', 'K']:
            self.puntos += 10
        elif carta.valor == 'A':
            self.puntos += 11
            self.ases += 1
        else:
            self.puntos += int(carta.valor)
        while self.puntos > 21 and self.ases > 0:
            self.puntos -= 10
            self.ases -= 1

    def esta_pasado(self):
        return self.puntos > 21

    def tiene_blackjack(self):
        return self.puntos == 21


class BlackjackGame:
    def __init__(self, font):
        self.font = font
        self.big_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.btn_font = pygame.font.SysFont("Arial", 26, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self.hit_btn = pygame.Rect(200, 680, 180, 55)
        self.stand_btn = pygame.Rect(410, 680, 180, 55)
        self.play_btn = pygame.Rect(380, 400, 240, 60)
        self.bet_minus = pygame.Rect(330, 340, 50, 50)
        self.bet_plus = pygame.Rect(620, 340, 50, 50)

        self.reset_game()

    def reset_game(self):
        self.deck = None
        self.player_hand = None
        self.dealer_hand = None
        self.bet_amount = 50
        self.status = "BETTING"
        self.outcome = ""
        self.win_amount = 0

    def start_round(self, game_data):
        if game_data["cash"] >= self.bet_amount:
            game_data["cash"] -= self.bet_amount
            self.deck = Baraja()
            self.deck.revolver()
            self.player_hand = Mano()
            self.dealer_hand = Mano()
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
        while self.dealer_hand.puntos < 17:
            self.dealer_hand.agregar_carta(self.deck.dar_carta())
        self.status = "ROUND_OVER"
        if self.dealer_hand.esta_pasado():
            self.outcome = "¡El crupier se pasó! Ganaste."
            self.win_amount = self.bet_amount * 2
        elif self.player_hand.puntos > self.dealer_hand.puntos:
            self.outcome = "¡Ganaste!"
            self.win_amount = self.bet_amount * 2
        elif self.player_hand.puntos < self.dealer_hand.puntos:
            self.outcome = "Perdiste contra el crupier."
            self.win_amount = 0
        else:
            self.outcome = "Empate (Push)."
            self.win_amount = self.bet_amount
        game_data["cash"] += self.win_amount

    def _dibujar_carta(self, screen, carta, x, y, oculta=False):
        ancho, alto = 70, 100
        pygame.draw.rect(screen, WHITE, (x, y, ancho, alto), border_radius=6)
        pygame.draw.rect(screen, DARK_GRAY, (x, y, ancho, alto), width=2, border_radius=6)
        if oculta:
            pygame.draw.rect(screen, (30, 30, 120), (x + 4, y + 4, ancho - 8, alto - 8), border_radius=4)
            return
        color = (180, 10, 10) if carta.palo in ["Corazones", "Diamantes"] else NEGRO
        simbolo = {"Corazones": "♥", "Diamantes": "♦", "Tréboles": "♣", "Picas": "♠"}.get(carta.palo, "?")
        val_surf = self.small_font.render(carta.valor, True, color)
        sim_surf = self.small_font.render(simbolo, True, color)
        screen.blit(val_surf, (x + 5, y + 4))
        screen.blit(sim_surf, (x + 5, y + 22))
        centro = self.btn_font.render(simbolo, True, color)
        screen.blit(centro, (x + ancho // 2 - centro.get_width() // 2,
                              y + alto // 2 - centro.get_height() // 2))

    def _dibujar_boton(self, screen, rect, texto, activo=True):
        mouse = pygame.mouse.get_pos()
        hov = rect.collidepoint(mouse) and activo
        bg = RED_HOV if hov else (DARK_RED if activo else (50, 50, 50))
        borde = GOLD if hov else (GOLD_DIM if activo else (80, 80, 80))
        tc = WHITE if activo else DARK_GRAY
        pygame.draw.rect(screen, bg, rect, border_radius=10)
        pygame.draw.rect(screen, borde, rect, width=2, border_radius=10)
        t = self.btn_font.render(texto, True, tc)
        screen.blit(t, (rect.x + (rect.width - t.get_width()) // 2,
                        rect.y + (rect.height - t.get_height()) // 2))

    def draw(self, screen):
        screen.fill(VERDE)
        pygame.draw.ellipse(screen, VERDE_OSC, (100, 50, 800, 600))

        title = self.big_font.render("BLACKJACK", True, GOLD)
        screen.blit(title, (1000 // 2 - title.get_width() // 2, 15))
        pygame.draw.line(screen, GOLD_DIM, (0, 75), (1000, 75), 2)

        if self.status == "BETTING":
            apuesta_surf = self.big_font.render(f"Apuesta: ${self.bet_amount}", True, WHITE)
            screen.blit(apuesta_surf, (1000 // 2 - apuesta_surf.get_width() // 2, 280))
            self._dibujar_boton(screen, self.bet_minus, "−")
            self._dibujar_boton(screen, self.bet_plus, "+")
            self._dibujar_boton(screen, self.play_btn, "JUGAR")
            info = self.small_font.render("Ajusta tu apuesta y presiona JUGAR", True, GRAY)
            screen.blit(info, (1000 // 2 - info.get_width() // 2, 480))
        else:
            oculta = self.status == "PLAYING"

            dealer_lbl = self.font.render("Crupier:", True, GOLD)
            screen.blit(dealer_lbl, (100, 100))
            for i, c in enumerate(self.dealer_hand.cartas):
                self._dibujar_carta(screen, c, 100 + i * 85, 135, oculta=(oculta and i == 1))
            puntos_dealer = self.dealer_hand.cartas[0].valor if oculta else str(self.dealer_hand.puntos)
            pts = self.small_font.render(f"Puntos: {puntos_dealer}", True, GRAY)
            screen.blit(pts, (100, 250))

            player_lbl = self.font.render("Tus cartas:", True, GOLD)
            screen.blit(player_lbl, (100, 390))
            for i, c in enumerate(self.player_hand.cartas):
                self._dibujar_carta(screen, c, 100 + i * 85, 425)
            pts2 = self.small_font.render(f"Puntos: {self.player_hand.puntos}", True, GRAY)
            screen.blit(pts2, (100, 540))

            apuesta_surf = self.small_font.render(f"Apuesta: ${self.bet_amount}", True, GRAY)
            screen.blit(apuesta_surf, (800, 540))

            if self.status == "PLAYING":
                self._dibujar_boton(screen, self.hit_btn, "PEDIR (H)")
                self._dibujar_boton(screen, self.stand_btn, "PLANTARSE (S)")
            elif self.status == "ROUND_OVER":
                color_out = (255, 200, 0) if "Ganaste" in self.outcome else (220, 80, 80) if "Perdiste" in self.outcome else WHITE
                out = self.big_font.render(self.outcome, True, color_out)
                screen.blit(out, (1000 // 2 - out.get_width() // 2, 640))
                again = self.small_font.render("Presiona ESPACIO para volver a apostar", True, GOLD)
                screen.blit(again, (1000 // 2 - again.get_width() // 2, 710))

        esc = self.small_font.render("ESC — volver al lobby", True, DARK_GRAY)
        screen.blit(esc, (20, 760))

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

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.status == "BETTING":
                if self.bet_minus.collidepoint(pos):
                    self.bet_amount = max(10, self.bet_amount - 10)
                elif self.bet_plus.collidepoint(pos):
                    self.bet_amount = min(game_data["cash"], self.bet_amount + 10)
                elif self.play_btn.collidepoint(pos):
                    self.start_round(game_data)
            elif self.status == "PLAYING":
                if self.hit_btn.collidepoint(pos):
                    self.hit()
                elif self.stand_btn.collidepoint(pos):
                    self.stand(game_data)

        return "BLACKJACK"