from games.cartas import Baraja

def calcular_puntaje(mano):
    puntaje = 0
    cantidad_ases = 0

    for carta in mano:
        # Determinamos el valor matemático según el string de la carta
        if carta.valor in ['J', 'Q', 'K']:
            puntaje += 10
        elif carta.valor == 'A':
            puntaje += 11
            cantidad_ases += 1
        else:
            puntaje += int(carta.valor) # Transformamos el texto '2', '3', etc. a entero

    # Bucle de corrección matemática para los Ases
    while puntaje > 21 and cantidad_ases > 0:
        puntaje -= 10
        cantidad_ases -= 1

    return puntaje

if __name__ == "__main__":
    mi_baraja = Baraja()
    mi_baraja.revolver()

    mano_jugador = [mi_baraja.dar_carta(), mi_baraja.dar_carta()]
    
    print("Tus cartas son:")
    for c in mano_jugador:
        print(f"- {c}")
        
    print(f"Puntaje total: {calcular_puntaje(mano_jugador)}")