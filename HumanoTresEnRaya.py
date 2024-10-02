# HumanoTresEnRaya.py

import pygame
from AgenteTresEnRaya import AgenteTresEnRaya
import copy

class HumanoTresEnRaya(AgenteTresEnRaya):
    def __init__(self, jugador='X', oponente='O'):
        super().__init__(jugador, oponente)
        self.movida_valida = False
        self.ultima_movida = None

    def programa(self, estado):
        self.movida_valida = False
        while not self.movida_valida:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    fila, col = self.traducir_coordenadas(x, y)
                    if estado[fila][col] == ' ':
                        self.ultima_movida = (fila, col)
                        self.movida_valida = True
        return self.hacer_movida(estado, self.ultima_movida)

    def traducir_coordenadas(self, x, y):
        fila = y // 100
        col = x // 100
        return fila, col

    def hacer_movida(self, estado, movida):
        fila, col = movida
        nuevo_estado = copy.deepcopy(estado)  # Hacer una copia profunda
        nuevo_estado[fila][col] = self.jugador
        return nuevo_estado
