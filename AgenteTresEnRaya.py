from AgenteIA.AgenteJugador import AgenteJugador

class AgenteTresEnRaya(AgenteJugador):
    def __init__(self, jugador, oponente, profundidad_maxima=3):
        # Asegúrate de pasar jugador y oponente al AgenteJugador
        super().__init__(jugador=jugador, oponente=oponente, profundidad_maxima=profundidad_maxima)

    def obtener_movimientos_legales(self, estado):
        movimientos = []
        n = len(estado)
        for i in range(n):
            for j in range(n):
                if estado[i][j] == ' ':
                    movimientos.append((i, j))  # Guardar solo las coordenadas
        return movimientos

    def es_estado_final(self, estado):
        n = len(estado)
        # Evaluar filas y columnas
        for i in range(n):
            if all(estado[i][j] == estado[i][0] and estado[i][0] != ' ' for j in range(n)):
                return True
            if all(estado[j][i] == estado[0][i] and estado[0][i] != ' ' for j in range(n)):
                return True

        # Evaluar diagonales
        if all(estado[i][i] == estado[0][0] and estado[0][0] != ' ' for i in range(n)):
            return True
        if all(estado[i][n-i-1] == estado[0][n-1] and estado[0][n-1] != ' ' for i in range(n)):
            return True

        # Evaluar si el tablero está lleno
        if all(estado[i][j] != ' ' for i in range(n) for j in range(n)):
            return True

        return False

    def evaluar_profundidad_maxima(self, n):
        if n <= 3:
            return 3
        elif n <= 6:
            return 2
        else:
            return 1

    def evaluar(self, estado):
        n = len(estado)
        puntuacion = 0

        # Evaluar filas y columnas
        for i in range(n):
            # Filas
            fila_puntuacion = self.evaluar_linea([estado[i][j] for j in range(n)])
            puntuacion += fila_puntuacion
            
            # Columnas
            columna_puntuacion = self.evaluar_linea([estado[j][i] for j in range(n)])
            puntuacion += columna_puntuacion

        # Evaluar diagonales
        diagonal_principal = self.evaluar_linea([estado[i][i] for i in range(n)])
        diagonal_secundaria = self.evaluar_linea([estado[i][n-i-1] for i in range(n)])
        
        puntuacion += diagonal_principal
        puntuacion += diagonal_secundaria

        return puntuacion

    def evaluar_linea(self, linea):
        jugador_count = linea.count(self.jugador)
        oponente_count = linea.count(self.oponente)
        vacias = linea.count(' ')
        
        # Caso ideal: el jugador ha llenado la línea
        if jugador_count == len(linea):
            return 100
        # Caso oponente ha llenado la línea
        elif oponente_count == len(linea):
            return -100
        # El jugador tiene la mayoría
        elif jugador_count > 0 and oponente_count == 0:
            return 10 * jugador_count
        # El oponente tiene la mayoría
        elif oponente_count > 0 and jugador_count == 0:
            return -10 * oponente_count
        # La línea está vacía o equilibrada
        return 0