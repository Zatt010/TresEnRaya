from AgenteIA.AgenteJugador import AgenteJugador

class AgenteTresEnRaya(AgenteJugador):
    def __init__(self, jugador, oponente, profundidad_maxima=3):
        # Asegúrate de pasar jugador y oponente al AgenteJugador
        super().__init__(jugador=jugador, oponente=oponente, profundidad_maxima=profundidad_maxima)

    def obtener_movimientos_legales(self, estado):
        movimientos = []
        for i in range(3):
            for j in range(3):
                if estado[i][j] == ' ':
                    movimientos.append((i, j))  # Guardar solo las coordenadas
        return movimientos

    def es_estado_final(self, estado):
        for i in range(3):
            # Comprobar filas
            if estado[i][0] == estado[i][1] == estado[i][2] != ' ':
                return True
            # Comprobar columnas
            if estado[0][i] == estado[1][i] == estado[2][i] != ' ':
                return True
        # Comprobar diagonales
        if estado[0][0] == estado[1][1] == estado[2][2] != ' ':
            return True
        if estado[0][2] == estado[1][1] == estado[2][0] != ' ':
            return True
        # Comprobar empate
        if all(estado[i][j] != ' ' for i in range(3) for j in range(3)):
            return True
        return False

    def evaluar(self, estado):
        for i in range(3):
            if estado[i][0] == estado[i][1] == estado[i][2] == self.jugador:
                return 10
            if estado[i][0] == estado[i][1] == estado[i][2] == self.oponente:
                return -10
        for i in range(3):
            if estado[0][i] == estado[1][i] == estado[2][i] == self.jugador:
                return 10
            if estado[0][i] == estado[1][i] == estado[2][i] == self.oponente:
                return -10
        if estado[0][0] == estado[1][1] == estado[2][2] == self.jugador:
            return 10
        if estado[0][0] == estado[1][1] == estado[2][2] == self.oponente:
            return -10
        if estado[0][2] == estado[1][1] == estado[2][0] == self.jugador:
            return 10
        if estado[0][2] == estado[1][1] == estado[2][0] == self.oponente:
            return -10
        return 0 