from AgenteIA.AgenteJugador import AgenteJugador

class AgenteTresEnRaya(AgenteJugador):
    def __init__(self, jugador, oponente, profundidad_maxima=3):
        super().__init__(jugador=jugador, oponente=oponente, profundidad_maxima=profundidad_maxima)

    def obtener_movimientos_legales(self, estado):
        movimientos = []
        n = len(estado)
        for i in range(n):
            for j in range(n):
                if estado[i][j] == ' ':
                    movimientos.append((i, j))
        return movimientos

    def es_estado_final(self, estado):
        n = len(estado)

        for i in range(n):
            if all(estado[i][j] == estado[i][0] and estado[i][0] != ' ' for j in range(n)):
                return True
            if all(estado[j][i] == estado[0][i] and estado[0][i] != ' ' for j in range(n)):
                return True

        if all(estado[i][i] == estado[0][0] and estado[0][0] != ' ' for i in range(n)):
            return True
        if all(estado[i][n-i-1] == estado[0][n-1] and estado[0][n-1] != ' ' for i in range(n)):
            return True

        
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

        
        for i in range(n):
            
            fila_puntuacion = self.evaluar_linea([estado[i][j] for j in range(n)])
            puntuacion += fila_puntuacion
            
            
            columna_puntuacion = self.evaluar_linea([estado[j][i] for j in range(n)])
            puntuacion += columna_puntuacion

        
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
        
        elif jugador_count > 0 and oponente_count == 0:
            return 10 * jugador_count
        
        elif oponente_count > 0 and jugador_count == 0:
            return -10 * oponente_count
        
        return 0