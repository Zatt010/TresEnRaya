from AgenteIA.AgenteJugador import AgenteJugador

class AgenteTresEnRaya(AgenteJugador):
    def __init__(self, jugador, oponente, piezas_en_linea=4, profundidad_maxima=3):
        super().__init__(jugador=jugador, oponente=oponente, piezas_en_linea=piezas_en_linea, profundidad_maxima=profundidad_maxima)
        self.piezas_en_linea = piezas_en_linea

    def programa(self, estado):
        evaluacion, mejor_movimiento = self.minimax(estado, 0, True, float('-inf'), float('inf'))

        if mejor_movimiento is not None:
            fila, col = mejor_movimiento
            return fila, col

        return None
