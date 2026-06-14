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

MANOS = ["Royal Flush","Straight Flush","Póker","Full House","Color","Escalera","Trío","Doble Par","Par J/Q/K/A","Sin premio"]
PAGOS = [800, 50, 25, 9, 6, 4, 3, 2, 1, 0]


class PokerGame:
    def __init__(self, font):
        self.font = font
        self.big_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.btn_font = pygame.font.SysFont("Arial", 26, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 21)
        self.play_btn = pygame.Rect(380, 390, 240, 60)
        self.draw_btn = pygame.Rect(380, 640, 240, 60)
        self.bet_minus = pygame.Rect(330, 330, 50, 50)
        self.bet_plus = pygame.Rect(620, 330, 50, 50)
        self.reset_game()

    def reset_game(self):
        self.deck = None
        self.hand = []
        self.held = [False] * 5
        self.bet_amount = 10
        self.status = "BETTING"
        self.outcome = ""
        self.win_amount = 0

    def start_round(self, game_data):
        if game_data["cash"] >= self.bet_amount:
            game_data["cash"] -= self.bet_amount
            self.deck = Baraja()
            self.deck.revolver()
            self.hand = [self.deck.dar_carta() for _ in range(5)]
            self.held = [False] * 5
            self.status = "DRAWING"

    def draw_cards(self, game_data):
        for i in range(5):
            if not self.held[i]:
                self.hand[i] = self.deck.dar_carta()
        rank = self._evaluar()
        self.outcome = MANOS[rank]
        self.win_amount = self.bet_amount * PAGOS[rank]
        game_data["cash"] += self.win_amount
        self.status = "RESULT"

    def _evaluar(self):
        v = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14}
        vals = sorted([v[c.valor] for c in self.hand], reverse=True)
        flush = len(set(c.palo for c in self.hand)) == 1
        straight = (vals[0] - vals[4] == 4 and len(set(vals)) == 5) or vals == [14,5,4,3,2]
        counts = sorted([vals.count(x) for x in set(vals)], reverse=True)
        if flush and straight and vals[0] == 14 and vals[1] == 13: return 0
        if flush and straight: return 1
        if counts[0] == 4: return 2
        if counts[:2] == [3, 2]: return 3
        if flush: return 4
        if straight: return 5
        if counts[0] == 3: return 6
        if counts[:2] == [2, 2]: return 7
        if counts[0] == 2 and any(vals.count(x) == 2 and x >= 11 for x in set(vals)): return 8
        return 9

    def _carta(self, screen, carta, x, y, held=False):
        w, h = 80, 115
        pygame.draw.rect(screen, WHITE, (x, y, w, h), border_radius=6)
        pygame.draw.rect(screen, GOLD if held else DARK_GRAY, (x, y, w, h), width=3 if held else 2, border_radius=6)
        if held:
            s = self.small_font.render("HOLD", True, GOLD)
            screen.blit(s, (x + w//2 - s.get_width()//2, y - 26))
        color = (180, 10, 10) if carta.palo in ["Corazones", "Diamantes"] else NEGRO
        sim = {"Corazones":"♥","Diamantes":"♦","Tréboles":"♣","Picas":"♠"}.get(carta.palo, "?")
        screen.blit(self.small_font.render(carta.valor, True, color), (x + 5, y + 4))
        screen.blit(self.small_font.render(sim, True, color), (x + 5, y + 24))
        c = self.btn_font.render(sim, True, color)
        screen.blit(c, (x + w//2 - c.get_width()//2, y + h//2 - c.get_height()//2))

    def _boton(self, screen, rect, texto, activo=True):
        hov = rect.collidepoint(pygame.mouse.get_pos()) and activo
        bg = RED_HOV if hov else (DARK_RED if activo else (50, 50, 50))
        borde = GOLD if hov else (GOLD_DIM if activo else (80, 80, 80))
        pygame.draw.rect(screen, bg, rect, border_radius=10)
        pygame.draw.rect(screen, borde, rect, width=2, border_radius=10)
        t = self.btn_font.render(texto, True, WHITE if activo else DARK_GRAY)
        screen.blit(t, (rect.x + (rect.width - t.get_width())//2, rect.y + (rect.height - t.get_height())//2))

    def draw(self, screen):
        screen.fill(VERDE)
        pygame.draw.ellipse(screen, VERDE_OSC, (50, 50, 900, 680))
        title = self.big_font.render("VIDEO POKER", True, GOLD)
        screen.blit(title, (1000//2 - title.get_width()//2, 15))
        pygame.draw.line(screen, GOLD_DIM, (0, 75), (1000, 75), 2)

        if self.status == "BETTING":
            s = self.big_font.render(f"Apuesta: ${self.bet_amount}", True, WHITE)
            screen.blit(s, (1000//2 - s.get_width()//2, 270))
            self._boton(screen, self.bet_minus, "−")
            self._boton(screen, self.bet_plus, "+")
            self._boton(screen, self.play_btn, "JUGAR")
            info = self.small_font.render("Ajusta la apuesta y presiona JUGAR o ESPACIO", True, GRAY)
            screen.blit(info, (1000//2 - info.get_width()//2, 470))
        else:
            sx = 1000//2 - (5 * 90)//2
            for i, c in enumerate(self.hand):
                self._carta(screen, c, sx + i * 90, 270, self.held[i])
            if self.status == "DRAWING":
                info = self.small_font.render("Clic en cartas para guardar (HOLD) → luego ROBAR CARTAS o ESPACIO", True, GRAY)
                screen.blit(info, (1000//2 - info.get_width()//2, 415))
                self._boton(screen, self.draw_btn, "ROBAR CARTAS")
            elif self.status == "RESULT":
                color = (255, 210, 0) if self.win_amount > 0 else (220, 80, 80)
                out = self.big_font.render(self.outcome, True, color)
                screen.blit(out, (1000//2 - out.get_width()//2, 415))
                if self.win_amount > 0:
                    g = self.font.render(f"¡Ganaste ${self.win_amount}!", True, (0, 220, 80))
                    screen.blit(g, (1000//2 - g.get_width()//2, 475))
                again = self.small_font.render("Presiona ESPACIO para nueva ronda", True, GOLD)
                screen.blit(again, (1000//2 - again.get_width()//2, 525))

        hud = self.small_font.render(f"Apuesta: ${self.bet_amount}", True, GRAY)
        screen.blit(hud, (20, 90))

        tx, ty = 720, 85
        for i, (m, p) in enumerate(zip(MANOS[:-1], PAGOS[:-1])):
            color = GOLD if (self.status == "RESULT" and self.outcome == m) else GRAY
            screen.blit(self.small_font.render(f"{m}: x{p}", True, color), (tx, ty + i * 27))

        screen.blit(self.small_font.render("ESC — volver al lobby", True, DARK_GRAY), (20, 760))

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
            elif self.status == "DRAWING" and event.key == pygame.K_SPACE:
                self.draw_cards(game_data)
            elif self.status == "RESULT" and event.key == pygame.K_SPACE:
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
            elif self.status == "DRAWING":
                sx = 1000//2 - (5 * 90)//2
                for i in range(5):
                    if pygame.Rect(sx + i * 90, 270, 80, 115).collidepoint(pos):
                        self.held[i] = not self.held[i]
                if self.draw_btn.collidepoint(pos):
                    self.draw_cards(game_data)

        return "POKER"
