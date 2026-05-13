import tkinter as tk
import random
import time

clas AviatorGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Aviator Casino")
        self.balance = 1000
        self.bet = 50
        self.multiplier = 1.0
        self.running = False
        self.plane_x = 50
        self.plane_y = 240
        self.plane_speed = 2
        self.max_multiplier = 5.0
        self.crash_threshold = random.uniform(1.5, 4.5)

        self.canvas = tk.Canvas(master, width=700, height=350, bg="#002b36")
        self.canvas.pack(padx=10, pady=10)

        controls = tk.Frame(master)
        controls.pack(fill="x", padx=10)

        self.balance_label = tk.Label(controls, text=f"Balance: ${self.balance}")
        self.balance_label.pack(side="left")

        self.bet_label = tk.Label(controls, text=f"Bet: ${self.bet}")
        self.bet_label.pack(side="left", padx=10)

        self.mult_label = tk.Label(controls, text=f"Multiplier: {self.multiplier:.2f}x")
        self.mult_label.pack(side="left", padx=10)

        self.status_label = tk.Label(master, text="Presiona INICIO para despegar", fg="#eee", bg="#073642")
        self.status_label.pack(fill="x", padx=10, pady=(0, 10))

        buttons = tk.Frame(master)
        buttons.pack(fill="x", padx=10)

        self.start_button = tk.Button(buttons, text="INICIO", command=self.start_game)
        self.start_button.pack(side="left", expand=True, fill="x", padx=5)

        self.cashout_button = tk.Button(buttons, text="COBRAR", command=self.cash_out, state="disabled")
        self.cashout_button.pack(side="left", expand=True, fill="x", padx=5)

        self.bet_entry = tk.Entry(buttons, width=10)
        self.bet_entry.insert(0, str(self.bet))
        self.bet_entry.pack(side="left", padx=5)

        self.info_label = tk.Label(master, text="Haz tu apuesta y gana antes de que el avión se estrelle.", fg="#eee", bg="#002b36")
        self.info_label.pack(fill="x", padx=10, pady=(5, 10))

        self.draw_background()
        self.draw_plane()

    def draw_background(self):
        self.canvas.delete("bg")
        self.canvas.create_rectangle(0, 0, 700, 350, fill="#002b36", tags="bg")
        self.canvas.create_line(0, 320, 700, 320, fill="#586e75", width=3, tags="bg")
        for i in range(6):
            x = i * 140
            self.canvas.create_line(x, 0, x, 350, fill="#073642", tags="bg")
        self.canvas.create_text(100, 30, text="Aviator", fill="#93a1a1", font=("Helvetica", 28, "bold"), tags="bg")
        self.canvas.create_text(520, 60, text="Multiplicador", fill="#eee", font=("Helvetica", 14), tags="bg")
        self.canvas.create_rectangle(420, 80, 680, 130, fill="#073642", outline="#586e75", tags="bg")
        self.multiplier_text = self.canvas.create_text(550, 105, text=f"{self.multiplier:.2f}x", fill="#2aa198", font=("Helvetica", 22, "bold"), tags="bg")

    def draw_plane(self):
        self.canvas.delete("plane")
        x, y = self.plane_x, self.plane_y
        self.canvas.create_polygon(x, y, x+40, y+15, x, y+30, fill="#b58900", outline="#cb4b16", width=2, tags="plane")
        self.canvas.create_polygon(x+40, y+15, x+70, y+5, x+70, y+25, fill="#dc322f", outline="#cb4b16", width=2, tags="plane")
        self.canvas.create_oval(x-10, y+8, x+10, y+22, fill="#eee8d5", outline="#93a1a1", tags="plane")
        self.canvas.create_line(x+20, y+15, x+40, y+15, fill="#073642", width=3, tags="plane")

    def update_ui(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.bet_label.config(text=f"Bet: ${self.bet}")
        self.mult_label.config(text=f"Multiplier: {self.multiplier:.2f}x")
        self.canvas.itemconfigure(self.multiplier_text, text=f"{self.multiplier:.2f}x")

    def start_game(self):
        if self.running:
            return
        try:
            bet_value = int(self.bet_entry.get())
        except ValueError:
            self.status_label.config(text="Apuesta inválida.")
            return
        if bet_value <= 0 or bet_value > self.balance:
            self.status_label.config(text="Apuesta debe ser positiva y menor al balance.")
            return
        self.bet = bet_value
        self.balance -= self.bet
        self.running = True
        self.multiplier = 1.0
        self.plane_x = 50
        self.plane_y = 240
        self.plane_speed = 2
        self.crash_threshold = random.uniform(1.5, 4.8)
        self.status_label.config(text="El avión despega... Cobra antes del choque!")
        self.start_button.config(state="disabled")
        self.cashout_button.config(state="normal")
        self.update_ui()
        self.animate()

    def animate(self):
        if not self.running:
            return
        self.plane_x += self.plane_speed
        self.plane_y -= self.plane_speed * 0.4
        self.plane_speed += 0.05
        self.multiplier += 0.02
        if self.plane_y < 40:
            self.plane_y = 40
        self.draw_background()
        self.draw_plane()
        self.update_ui()
        if self.multiplier >= self.crash_threshold:
            self.running = False
            self.cashout_button.config(state="disabled")
            self.start_button.config(state="normal")
            self.status_label.config(text=f"El avión se estrelló en {self.multiplier:.2f}x. Pierdes la apuesta.")
            self.plane_y = 260
            self.draw_background()
            self.draw_plane()
            return
        self.master.after(50, self.animate)

    def cash_out(self):
        if not self.running:
            return
        payout = int(self.bet * self.multiplier)
        self.balance += payout
        self.running = False
        self.cashout_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.status_label.config(text=f"Cobraste {payout} en {self.multiplier:.2f}x. Buen vuelo!")
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    game = AviatorGame(root)
    root.mainloop()

