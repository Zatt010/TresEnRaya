from AgenteIA.Agente import Agente
from collections import namedtuple
from abc import ABC

class AgenteJugador(Agente, ABC):
    def __init__(self, jugador, oponente, programa=None, profundidad_maxima=3):
        super().__init__(programa)
        self.profundidad_maxima = profundidad_maxima
        self.jugador = jugador
        self.oponente = oponente

    def programa(self, percepcion):
        evaluacion, mejor_movimiento = self.minimax(percepcion, 0, True, float('-inf'), float('inf'))

        if mejor_movimiento is not None:
            fila, col = mejor_movimiento
            nuevo_estado = [fila[:] for fila in percepcion]
            nuevo_estado[fila][col] = self.jugador
            return nuevo_estado
        return percepcion  

    def minimax(self, estado, profundidad, maximizador, alfa, beta):
        if self.es_estado_final(estado) or profundidad == self.profundidad_maxima:
            return self.evaluar(estado), None  

        if maximizador:
            max_eval = float('-inf')
            mejor_movimiento = None
            for movimiento in self.obtener_movimientos_legales(estado):
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
            for movimiento in self.obtener_movimientos_legales(estado):
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
        for i in range(3):
            for j in range(3):
                if estado[i][j] == ' ':
                    movimientos.append((i, j))  # Guardar solo las coordenadas
        return movimientos

    def es_estado_final(self, estado):
        raise NotImplementedError

    def evaluar(self, estado):
        raise NotImplementedError
    

    # evaluar  la utilidad, funcion de evaluacion que permita tener la mayor probabilidad de ganar 
    # profundidad maxima de 3 tablero 6x6