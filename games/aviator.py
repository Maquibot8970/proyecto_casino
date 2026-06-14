import pygame
import random
import math


BG_COLOR        = (20,  12,  14)
PANEL_COLOR     = (28,   5,   8)
DARK_RED        = (84,  11,  22)
RED_HOVER       = (163, 22,  43)
GOLD            = (247, 202,  24)
GOLD_DIM        = (130,  90,  40)
WHITE           = (255, 255, 255)
GRAY            = (200, 200, 200)
DARK_GRAY       = (100, 100, 100)
GREEN           = (0,   200,  80)
CRASHED_RED     = (220,  40,  40)
TRAIL_COLOR     = (247, 202,  24)
SKY_TOP         = (10,   20,  50)
SKY_BOT         = (20,   12,  14)


class AviatorGame:
   
    W, H = 1000, 800

    def __init__(self, font):
        self.font       = font
        self.big_font   = pygame.font.SysFont("Arial", 90, bold=True)
        self.med_font   = pygame.font.SysFont("Arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)
        self.btn_font   = pygame.font.SysFont("Arial", 26, bold=True)

       
        self.start_btn   = pygame.Rect(60,  680, 260, 60)
        self.cashout_btn = pygame.Rect(360, 680, 260, 60)
        self.bet_minus   = pygame.Rect(660, 680,  50, 60)
        self.bet_plus    = pygame.Rect(780, 680,  50, 60)

        self.bet_amount = 10
        self._reset()

    
    def _reset(self):
        self.multiplier   = 1.00
        self.start_time   = 0
        self.crash_point  = self._gen_crash()
        self.status       = "WAITING"   
        self.win_amount   = 0
        
        self.plane_x      = 80.0
        self.plane_y      = float(self.H - 160)
        self.trail        = []          
        self._angle       = 0.0

    def _gen_crash(self):
        return round(random.uniform(1.01, 10.0) ** random.uniform(1.0, 1.5), 2)

   
    def _mult_to_pos(self, mult):
        
        flight_w = self.W - 120
        flight_h = self.H - 240    
        t = min((mult - 1.0) / 9.0, 1.0)   
        x = 80 + flight_w * t
        
        y = (self.H - 160) - flight_h * (t ** 0.7)
        return x, y

   
    def update(self):
        if self.status != "FLYING":
            return

        elapsed         = (pygame.time.get_ticks() - self.start_time) / 1000.0
        self.multiplier = round(1.00 * (1.07 ** elapsed), 2)

        nx, ny = self._mult_to_pos(self.multiplier)
        
        dx = nx - self.plane_x
        dy = ny - self.plane_y
        if dx != 0:
            self._angle = math.degrees(math.atan2(-dy, dx))

        
        if len(self.trail) == 0 or abs(nx - self.trail[-1][0]) > 4:
            self.trail.append((nx, ny))
            if len(self.trail) > 300:
                self.trail.pop(0)

        self.plane_x, self.plane_y = nx, ny

        if self.multiplier >= self.crash_point:
            self.multiplier = self.crash_point
            self.status     = "CRASHED"

    
    def draw(self, screen):
        
        for row in range(self.H):
            t   = row / self.H
            r   = int(SKY_TOP[0] * (1 - t) + SKY_BOT[0] * t)
            g   = int(SKY_TOP[1] * (1 - t) + SKY_BOT[1] * t)
            b   = int(SKY_TOP[2] * (1 - t) + SKY_BOT[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, row), (self.W, row))

   
        rng = random.Random(42)
        for _ in range(60):
            sx = rng.randint(0, self.W)
            sy = rng.randint(0, self.H - 220)
            alpha = rng.randint(100, 255)
            pygame.draw.circle(screen, (alpha, alpha, alpha), (sx, sy), 1)

        
        pygame.draw.rect(screen, PANEL_COLOR, (0, self.H - 200, self.W, 200))
        pygame.draw.line(screen, GOLD_DIM, (0, self.H - 200), (self.W, self.H - 200), 2)

        
        pygame.draw.line(screen, GOLD_DIM,
                         (60, self.H - 160), (self.W - 60, self.H - 160), 2)

        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                alpha = int(255 * (i / len(self.trail)))
                color = (alpha, int(alpha * 0.8), 0)
                pygame.draw.line(screen, color,
                                 (int(self.trail[i-1][0]), int(self.trail[i-1][1])),
                                 (int(self.trail[i][0]),   int(self.trail[i][1])), 2)

       
        if self.status != "WAITING":
            self._draw_plane(screen, int(self.plane_x), int(self.plane_y),
                             self._angle if self.status == "FLYING" else 0)

       
        if self.status == "CRASHED":
            mult_color = CRASHED_RED
            label      = f"{self.multiplier:.2f}x  CRASHED!"
        elif self.status == "CASHED_OUT":
            mult_color = GREEN
            label      = f"{self.multiplier:.2f}x"
        else:
            mult_color = WHITE
            label      = f"{self.multiplier:.2f}x"

        mult_surf = self.big_font.render(label, True, mult_color)
        screen.blit(mult_surf, (self.W // 2 - mult_surf.get_width() // 2, 60))

       
        if self.status == "WAITING":
            info = "Ajusta tu apuesta y presiona  INICIO"
        elif self.status == "FLYING":
            info = f"Presiona  COBRAR  para ganar  ${int(self.bet_amount * self.multiplier)}"
        elif self.status == "CRASHED":
            info = f"El avión se estrelló — perdiste  ${self.bet_amount}.  Ajusta y presiona INICIO"
        else:   
            info = f"¡Ganaste  ${self.win_amount}!  Ajusta y presiona INICIO para otra ronda"

        info_surf = self.small_font.render(info, True, GRAY)
        screen.blit(info_surf, (self.W // 2 - info_surf.get_width() // 2, 175))

       
        mouse = pygame.mouse.get_pos()
        self._draw_button(screen, self.start_btn, "INICIO",
                          enabled=self.status != "FLYING",
                          hovered=self.start_btn.collidepoint(mouse),
                          color_on=DARK_RED, color_hover=RED_HOVER)

        self._draw_button(screen, self.cashout_btn, "COBRAR",
                          enabled=self.status == "FLYING",
                          hovered=self.cashout_btn.collidepoint(mouse) and self.status == "FLYING",
                          color_on=(20, 90, 30), color_hover=(30, 150, 50))

       
        self._draw_button(screen, self.bet_minus, "−",
                          enabled=self.status != "FLYING",
                          hovered=self.bet_minus.collidepoint(mouse) and self.status != "FLYING",
                          color_on=DARK_RED, color_hover=RED_HOVER)
        self._draw_button(screen, self.bet_plus, "+",
                          enabled=self.status != "FLYING",
                          hovered=self.bet_plus.collidepoint(mouse) and self.status != "FLYING",
                          color_on=DARK_RED, color_hover=RED_HOVER)

       
        bet_box = pygame.Rect(715, 680, 60, 60)
        pygame.draw.rect(screen, (10, 10, 10), bet_box, border_radius=8)
        pygame.draw.rect(screen, GOLD_DIM, bet_box, width=2, border_radius=8)
        bet_surf = self.med_font.render(f"${self.bet_amount}", True, GOLD)
        screen.blit(bet_surf, (bet_box.x + bet_box.width // 2 - bet_surf.get_width() // 2,
                               bet_box.y + bet_box.height // 2 - bet_surf.get_height() // 2))

        label_bet = self.small_font.render("Apuesta", True, GRAY)
        screen.blit(label_bet, (715, 750))

        
        if self.status in ("CRASHED", "CASHED_OUT"):
            cp_surf = self.small_font.render(
                f"Crash point: {self.crash_point:.2f}x", True, DARK_GRAY)
            screen.blit(cp_surf, (self.W - cp_surf.get_width() - 20, self.H - 190))

     
        esc_surf = self.small_font.render("ESC — volver al lobby", True, DARK_GRAY)
        screen.blit(esc_surf, (20, self.H - 185))

   
    def _draw_plane(self, screen, cx, cy, angle=0):
        
        size = 36
        surf = pygame.Surface((size * 3, size * 2), pygame.SRCALPHA)
        
        pygame.draw.ellipse(surf, (220, 180, 40),
                            (size // 2, size // 2, size * 2, size - 4))
        
        pygame.draw.polygon(surf, (200, 60, 30), [
            (size // 2, size // 2 + 4),
            (0,         size // 2 - 10),
            (0,         size // 2 + 20),
        ])
        
        pygame.draw.polygon(surf, (180, 140, 20), [
            (size,          size // 2 + 4),
            (size + size//2, 0),
            (size + size,    size // 2 + 4),
        ])
      
        pygame.draw.polygon(surf, (240, 200, 60), [
            (size * 2 + size // 2, size // 2 + 4),
            (size * 3,             size // 2 + size // 4),
            (size * 2 + size // 2, size // 2 + size // 2),
        ])

        rotated = pygame.transform.rotate(surf, angle)
        rect    = rotated.get_rect(center=(cx, cy))
        screen.blit(rotated, rect)

    
    def _draw_button(self, screen, rect, text,
                     enabled=True, hovered=False,
                     color_on=(84, 11, 22), color_hover=(163, 22, 43)):
        if not enabled:
            bg     = (40, 40, 40)
            border = (70, 70, 70)
            tc     = (90, 90, 90)
        elif hovered:
            bg     = color_hover
            border = GOLD
            tc     = WHITE
        else:
            bg     = color_on
            border = GOLD_DIM
            tc     = (220, 220, 220)

        pygame.draw.rect(screen, bg,     rect, border_radius=10)
        pygame.draw.rect(screen, border, rect, width=2, border_radius=10)
        t_surf = self.btn_font.render(text, True, tc)
        screen.blit(t_surf, (rect.x + (rect.width  - t_surf.get_width())  // 2,
                             rect.y + (rect.height - t_surf.get_height()) // 2))

    
    def handle_event(self, event, game_data):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._reset()
                return "MENU"
           
            if self.status in ("WAITING", "CRASHED", "CASHED_OUT"):
                if event.key == pygame.K_UP:
                    self.bet_amount = min(game_data["cash"], self.bet_amount + 10)
                elif event.key == pygame.K_DOWN:
                    self.bet_amount = max(10, self.bet_amount - 10)
                elif event.key == pygame.K_SPACE:
                    self._try_start(game_data)
            if event.key == pygame.K_RETURN and self.status == "FLYING":
                self._cash_out(game_data)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.start_btn.collidepoint(pos) and self.status != "FLYING":
                self._try_start(game_data)
            elif self.cashout_btn.collidepoint(pos) and self.status == "FLYING":
                self._cash_out(game_data)
            elif self.bet_minus.collidepoint(pos) and self.status != "FLYING":
                self.bet_amount = max(10, self.bet_amount - 10)
            elif self.bet_plus.collidepoint(pos) and self.status != "FLYING":
                self.bet_amount = min(game_data["cash"], self.bet_amount + 10)

        return "AVIATOR"

    
    def _try_start(self, game_data):
        if game_data["cash"] < self.bet_amount:
            return
        game_data["cash"] -= self.bet_amount
        self._reset()
        self.start_time = pygame.time.get_ticks()
        self.status     = "FLYING"

    def _cash_out(self, game_data):
        self.win_amount   = int(self.bet_amount * self.multiplier)
        game_data["cash"] += self.win_amount
        self.status       = "CASHED_OUT"
