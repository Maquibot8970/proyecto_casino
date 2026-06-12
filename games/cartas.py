import random 

class Carta: 
    def __init__(self,palo,valor):
        self.palo = palo
        self.valor = valor 

    # __str__ permite ver el texto en la terminal
    def __str__(self):
        return f"{self.valor} de {self.palo}"

class Baraja:
    def __init__(self):
        self.cartas = [] # Iniciamos con una cadena vacia para despues guardar los objetos
        self.construir_baraja()
    
    def construir_baraja(self):
        palos = ['Corazones', 'Diamantes', 'Tréboles', 'Picas']
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] 

        # Un ciclo anidado (un for dentro de otro) para combinar cada palo con cada valor
        for palo in palos:
            for valor in valores:
                # Instanciamos un objeto Carta y lo agregamos a nuestra lista
                nueva_carta = Carta(palo, valor)
                self.cartas.append(nueva_carta)
    
    def revolver(self):
        # Usamos la librería random para mezclar la lista in-place (ahí mismo)
        random.shuffle(self.cartas)

    def dar_carta(self):
        # pop() saca el último elemento de la lista y lo devuelve. Perfecto para simular que sacamos la carta de hasta arriba.
        if len(self.cartas) > 0:
            return self.cartas.pop()
        else:
            return None