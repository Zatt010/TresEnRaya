from AgenteIA.Agente import Agente
from collections import namedtuple
from abc import ABC

class AgenteJugador(Agente, ABC):
    def __init__(self, jugador, oponente, profundidad_maxima=3, piezas_en_linea=4):
        super().__init__()
        self.profundidad_maxima = profundidad_maxima
        self.jugador = jugador
        self.oponente = oponente
        self.piezas_en_linea = piezas_en_linea

    def programa(self, percepcion):
        evaluacion, mejor_movimiento = self.minimax(percepcion, 0, True, float('-inf'), float('inf'))

        if mejor_movimiento is not None:
            fila, col = mejor_movimiento
            nuevo_estado = [fila[:] for fila in percepcion]
            nuevo_estado[fila][col] = self.jugador
            return nuevo_estado
        return percepcion  

    def minimax(self, estado, profundidad, maximizador, alfa, beta):
        if self.es_estado_final(estado) or profundidad >= self.profundidad_maxima:
            return self.evaluar(estado), None 

        amenaza = self.minimizar_amenazas(estado)
        if amenaza and maximizador:
            return 0, amenaza 

        if maximizador:
            max_eval = float('-inf')
            mejor_movimiento = None
            movimientos = self.obtener_movimientos_legales(estado)
            for movimiento in movimientos:
                nuevo_estado = [fila[:] for fila in estado]
                fila, col = movimiento
                nuevo_estado[fila][col] = self.jugador  
                evaluacion, _ = self.minimax(nuevo_estado, profundidad + 1, False, alfa, beta)
                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejor_movimiento = movimiento 
                alfa = max(alfa, evaluacion)
                if beta <= alfa:
                    break
            return max_eval, mejor_movimiento  

        else:
            min_eval = float('inf')
            mejor_movimiento = None
            movimientos = self.obtener_movimientos_legales(estado)
            for movimiento in movimientos:
                nuevo_estado = [fila[:] for fila in estado]
                fila, col = movimiento
                nuevo_estado[fila][col] = self.oponente  
                evaluacion, _ = self.minimax(nuevo_estado, profundidad + 1, True, alfa, beta)
                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_movimiento = movimiento  
                beta = min(beta, evaluacion)
                if beta <= alfa:
                    break
            return min_eval, mejor_movimiento  

    def obtener_movimientos_legales(self, estado):
        movimientos = []
        n = len(estado)
        for i in range(n):
            for j in range(n):
                if estado[i][j] == ' ':
                    movimientos.append((i, j))  
        return movimientos

    def es_estado_final(self, estado):
        return self.verificar_victoria(estado, self.jugador) or self.verificar_victoria(estado, self.oponente) or all(estado[i][j] != ' ' for i in range(len(estado)) for j in range(len(estado)))

    def evaluar(self, estado):
        puntuacion = 0
        n = len(estado)

        for i in range(n):
            puntuacion += self.evaluar_linea([estado[i][j] for j in range(n)])  # Fila
            puntuacion += self.evaluar_linea([estado[j][i] for j in range(n)])  # Columna

        for i in range(n - self.piezas_en_linea + 1):
            puntuacion += self.evaluar_diagonales(estado, i, True)  # Diagonales principales
            puntuacion += self.evaluar_diagonales(estado, i, False)  # Diagonales secundarias

        if self.verificar_linea_casi_completa(estado, self.jugador):
            puntuacion += 50
        if self.verificar_linea_casi_completa(estado, self.oponente):
            puntuacion -= 50

        if self.verificar_victoria(estado, self.jugador):
            puntuacion += 1000  
        if self.verificar_victoria(estado, self.oponente):
            puntuacion -= 1000  

        return puntuacion

    def evaluar_linea(self, linea):
        jugador_count = linea.count(self.jugador)
        oponente_count = linea.count(self.oponente)
        vacias = linea.count(' ')

        if jugador_count == self.piezas_en_linea:
            return 100
        elif oponente_count == self.piezas_en_linea:
            return -100
        elif jugador_count > 0 and oponente_count == 0:
            return 10 * jugador_count + 5 * vacias  
        elif oponente_count > 0 and jugador_count == 0:
            return -10 * oponente_count - 5 * vacias  

        return 0

    def evaluar_diagonales(self, estado, offset, es_principal):
        n = len(estado)
        puntuacion = 0

        if es_principal:  
            for i in range(n - self.piezas_en_linea + 1):
                diagonal = [estado[i + j][offset + j] for j in range(self.piezas_en_linea)]
                puntuacion += self.evaluar_linea(diagonal)
        else:  
            for i in range(n - self.piezas_en_linea + 1):
                diagonal = [estado[i + j][n - 1 - (offset + j)] for j in range(self.piezas_en_linea)]
                puntuacion += self.evaluar_linea(diagonal)

        return puntuacion

    def verificar_linea_casi_completa(self, estado, jugador):
        n = len(estado)

        for i in range(n):
            if estado[i].count(jugador) == self.piezas_en_linea - 1 and estado[i].count(' ') == 1:
                return True
            columna = [estado[j][i] for j in range(n)]
            if columna.count(jugador) == self.piezas_en_linea - 1 and columna.count(' ') == 1:
                return True

        for i in range(n - self.piezas_en_linea + 1):
            diagonal_principal = [estado[i + j][i + j] for j in range(self.piezas_en_linea)]
            if diagonal_principal.count(jugador) == self.piezas_en_linea - 1 and diagonal_principal.count(' ') == 1:
                return True
            diagonal_secundaria = [estado[i + j][n - 1 - (i + j)] for j in range(self.piezas_en_linea)]
            if diagonal_secundaria.count(jugador) == self.piezas_en_linea - 1 and diagonal_secundaria.count(' ') == 1:
                return True

        return False


    def verificar_victoria(self, estado, jugador):
        n = len(estado)
        for i in range(n):
            for j in range(n - self.piezas_en_linea + 1):
                if all(estado[i][j + k] == jugador for k in range(self.piezas_en_linea)):
                    return True

        for j in range(n):
            for i in range(n - self.piezas_en_linea + 1):
                if all(estado[i + k][j] == jugador for k in range(self.piezas_en_linea)):
                    return True

        for i in range(n - self.piezas_en_linea + 1):
            if all(estado[i + k][i + k] == jugador for k in range(self.piezas_en_linea)):
                return True
            if all(estado[i + k][n - 1 - (i + k)] == jugador for k in range(self.piezas_en_linea)):
                return True

        return False

    def minimizar_amenazas(self, estado):
        for i in range(len(estado)):
            for j in range(len(estado)):
                if estado[i][j] == ' ':
                    estado[i][j] = self.oponente
                    if self.verificar_victoria(estado, self.oponente):
                        estado[i][j] = ' '
                        return (i, j)
                    estado[i][j] = ' '
        return None
