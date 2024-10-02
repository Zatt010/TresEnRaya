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
        
        for i in range(self.n):
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] != ' ':
                return True
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] != ' ':
                return True

        
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != ' ':
            return True
        if self.tablero[0][self.n-1] == self.tablero[1][self.n-2] == self.tablero[2][0] != ' ':
            return True

        
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
        for i in range(self.n):
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] != ' ':
                return self.tablero[i][0]
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] != ' ':
                return self.tablero[0][i]

        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != ' ':
            return self.tablero[0][0]
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != ' ':
            return self.tablero[0][2]

        if all(self.tablero[i][j] != ' ' for i in range(self.n) for j in range(self.n)):
            return None

        return None