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

    # --- ESTO ES UN METODO DE CONTROL LISTO PARA USARSE---

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