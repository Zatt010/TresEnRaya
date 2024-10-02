# EntornoTresEnRaya.py

import pygame
import copy
from AgenteIA.Entorno import Entorno

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

# Dimensiones del tablero
TAMANO_CUADRO = 100
LINEA_ANCHO = 10

class EntornoTresEnRaya(Entorno):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.tablero = [[' ' for _ in range(n)] for _ in range(n)]
        self.turno = 0
        pygame.init()
        self.screen = pygame.display.set_mode((n * TAMANO_CUADRO, n * TAMANO_CUADRO))
        pygame.display.set_caption("Tres en Raya")
        self.screen.fill(BLANCO)
        self.dibujar_tablero()

    def percibir(self, agente):
        return self.tablero

    def ejecutar(self, agente):
        movimiento = agente.programa(self.tablero)
        if movimiento:  # Asegúrate de que el movimiento no sea None
            self.tablero = movimiento
        self.turno = (self.turno + 1) % 2
        self.dibujar_tablero()

    def finalizado(self):
        # Comprueba filas
        for i in range(self.n):
            if all(self.tablero[i][j] == self.tablero[i][0] and self.tablero[i][j] != ' ' for j in range(self.n)):
                return True

        # Comprueba columnas
        for i in range(self.n):
            if all(self.tablero[j][i] == self.tablero[0][i] and self.tablero[j][i] != ' ' for j in range(self.n)):
                return True

        # Comprueba diagonal principal
        if all(self.tablero[i][i] == self.tablero[0][0] and self.tablero[i][i] != ' ' for i in range(self.n)):
            return True

        # Comprueba diagonal secundaria
        if all(self.tablero[i][self.n - i - 1] == self.tablero[0][self.n - 1] and self.tablero[i][self.n - i - 1] != ' ' for i in range(self.n)):
            return True

        # Comprueba si el tablero está lleno
        if all(self.tablero[i][j] != ' ' for i in range(self.n) for j in range(self.n)):
            return True

        return False

    def dibujar_tablero(self):
        for i in range(1, self.n):
            pygame.draw.line(self.screen, NEGRO, (i * TAMANO_CUADRO, 0), (i * TAMANO_CUADRO, self.n * TAMANO_CUADRO), LINEA_ANCHO)
            pygame.draw.line(self.screen, NEGRO, (0, i * TAMANO_CUADRO), (self.n * TAMANO_CUADRO, i * TAMANO_CUADRO), LINEA_ANCHO)
        self.actualizar_tablero()

    def actualizar_tablero(self):
        fuente = pygame.font.Font(None, 100)
        for fila in range(3):
            for col in range(3):
                if self.tablero[fila][col] == 'X':
                    texto = fuente.render('X', True, ROJO)
                elif self.tablero[fila][col] == 'O':
                    texto = fuente.render('O', True, AZUL)
                else:
                    continue
                self.screen.blit(texto, (col * TAMANO_CUADRO + 25, fila * TAMANO_CUADRO + 10))
        pygame.display.flip()

    def run(self):
        jugando = True
        while jugando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False

            if not self.finalizado():
                agente_actual = self.agentes[self.turno]
                self.percibir(agente_actual)
                self.ejecutar(agente_actual)

            pygame.time.delay(500)  # Delay para visualizar mejor los movimientos

        pygame.quit()

    def ganador(self):
        # Comprueba filas
        for i in range(self.n):
            if all(self.tablero[i][j] == self.tablero[i][0] and self.tablero[i][j] != ' ' for j in range(self.n)):
                return self.tablero[i][0]

        # Comprueba columnas
        for i in range(self.n):
            if all(self.tablero[j][i] == self.tablero[0][i] and self.tablero[j][i] != ' ' for j in range(self.n)):
                return self.tablero[0][i]

        # Comprueba diagonal principal
        if all(self.tablero[i][i] == self.tablero[0][0] and self.tablero[i][i] != ' ' for i in range(self.n)):
            return self.tablero[0][0]

        # Comprueba diagonal secundaria
        if all(self.tablero[i][self.n - i - 1] == self.tablero[0][self.n - 1] and self.tablero[i][self.n - i - 1] != ' ' for i in range(self.n)):
            return self.tablero[0][self.n - 1]

        # Comprueba si el tablero está lleno
        if all(self.tablero[i][j] != ' ' for i in range(self.n) for j in range(self.n)):
            return "EMPATE"

        return None