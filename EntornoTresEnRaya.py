import pygame
from AgenteIA.Entorno import Entorno
import copy
# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

# Dimensiones del tablero
TAMANO_CUADRO = 100
LINEA_ANCHO = 10

class EntornoTresEnRaya(Entorno):
    def __init__(self, n, piezas_en_linea):
        super().__init__()
        self.n = n
        self.piezas_en_linea = piezas_en_linea  # Objetivo de piezas en línea para ganar
        self.tablero = [[' ' for _ in range(n)] for _ in range(n)]
        self.turno = 0
        pygame.init()
        self.screen = pygame.display.set_mode((n * TAMANO_CUADRO, n * TAMANO_CUADRO))
        pygame.display.set_caption(f"{n} en Raya")
        self.screen.fill(BLANCO)
        self.dibujar_tablero()

    def verificar_linea(self, fila, col, delta_fila, delta_col):
        objetivo = self.tablero[fila][col]
        if objetivo == ' ':
            return False

        for i in range(1, self.piezas_en_linea):
            nueva_fila = fila + i * delta_fila
            nueva_col = col + i * delta_col
            if not (0 <= nueva_fila < self.n and 0 <= nueva_col < self.n):
                return False
            if self.tablero[nueva_fila][nueva_col] != objetivo:
                return False
        return True

    def finalizado(self):
        for fila in range(self.n):
            for col in range(self.n):
                if self.tablero[fila][col] != ' ':
                    if (self.verificar_linea(fila, col, 1, 0) or  # Horizontal
                        self.verificar_linea(fila, col, 0, 1) or  # Vertical
                        self.verificar_linea(fila, col, 1, 1) or  # Diagonal principal
                        self.verificar_linea(fila, col, 1, -1)):  # Diagonal secundaria
                        return True

        if all(self.tablero[fila][col] != ' ' for fila in range(self.n) for col in range(self.n)):
            return True
        return False

    def ganador(self):
        for fila in range(self.n):
            for col in range(self.n):
                if self.tablero[fila][col] != ' ':
                    if (self.verificar_linea(fila, col, 1, 0) or
                        self.verificar_linea(fila, col, 0, 1) or
                        self.verificar_linea(fila, col, 1, 1) or
                        self.verificar_linea(fila, col, 1, -1)):
                        return self.tablero[fila][col]
        return None

    def percibir(self, agente):
        return copy.deepcopy(self.tablero)

    def ejecutar(self, agente):
        movimiento = agente.programa(self.tablero)
        
        if isinstance(movimiento, (tuple, list)) and len(movimiento) == 2:
            fila, col = movimiento  # Desempaqueta fila y col
            self.tablero[fila][col] = agente.jugador
            self.turno = (self.turno + 1) % 2
            self.dibujar_tablero()
        else:
            print(f"Movimiento inválido: {movimiento}")  

    def dibujar_tablero(self):
        for i in range(1, self.n):
            pygame.draw.line(self.screen, NEGRO, (i * TAMANO_CUADRO, 0), (i * TAMANO_CUADRO, self.n * TAMANO_CUADRO), LINEA_ANCHO)
            pygame.draw.line(self.screen, NEGRO, (0, i * TAMANO_CUADRO), (self.n * TAMANO_CUADRO, i * TAMANO_CUADRO), LINEA_ANCHO)
        self.actualizar_tablero()

    def actualizar_tablero(self):
        fuente = pygame.font.Font(None, 100)
        for fila in range(self.n):
            for col in range(self.n):
                if self.tablero[fila][col] == 'X':
                    texto = fuente.render('X', True, ROJO)
                    self.screen.blit(texto, (col * TAMANO_CUADRO + 25, fila * TAMANO_CUADRO + 10))
                elif self.tablero[fila][col] == 'O':
                    texto = fuente.render('O', True, AZUL)
                    self.screen.blit(texto, (col * TAMANO_CUADRO + 25, fila * TAMANO_CUADRO + 10))
        pygame.display.flip()
