import pygame
from EntornoTresEnRaya import EntornoTresEnRaya
from HumanoTresEnRaya import HumanoTresEnRaya
from AgenteTresEnRaya import AgenteTresEnRaya

class Tablero:
    def __init__(self, n, piezas_en_linea=3):
        pygame.init()
        self.n = n
        self.piezas_en_linea = piezas_en_linea  
        self.width = n * 100
        self.height = n * 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tres en Raya")
        
        # Crear los agentes y entorno
        self.entorno = EntornoTresEnRaya(n, self.piezas_en_linea)
        self.agente1 = HumanoTresEnRaya(jugador='X', oponente='O')
        self.agente2 = AgenteTresEnRaya(jugador='O', oponente='X', piezas_en_linea=self.piezas_en_linea)  # Paso de piezas en línea
        self.entorno.insertar_objeto(self.agente1)
        self.entorno.insertar_objeto(self.agente2)
        
        self.board = ['' for _ in range(n * n)]
        self.currentPlayer = 'X'

        self.run()

    def dibujar_tablero(self):
        self.screen.fill((255, 255, 255))
        for i in range(1, self.n):
            pygame.draw.line(self.screen, (0, 0, 0), (i * 100, 0), (i * 100, self.height), 5)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 100), (self.width, i * 100), 5)
        self.actualizar_tablero()

    def actualizar_tablero(self):
        fuente = pygame.font.Font(None, 100)
        for fila in range(self.n):
            for col in range(self.n):
                if self.entorno.tablero[fila][col] == 'X':
                    texto = fuente.render('X', True, (255, 0, 0))
                    self.screen.blit(texto, (col * 100 + 25, fila * 100 + 10))
                elif self.entorno.tablero[fila][col] == 'O':
                    texto = fuente.render('O', True, (0, 0, 255))
                    self.screen.blit(texto, (col * 100 + 25, fila * 100 + 10))
        pygame.display.flip()

    def run(self):
        jugando = True
        while jugando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False

                if event.type == pygame.MOUSEBUTTONDOWN and self.currentPlayer == 'X':
                    pos = pygame.mouse.get_pos()
                    fila = pos[1] // 100
                    col = pos[0] // 100

                    if self.entorno.tablero[fila][col] == ' ':
                        self.entorno.tablero[fila][col] = self.currentPlayer
                        self.dibujar_tablero()

                        if self.entorno.finalizado():
                            jugando = False
                            break
                        
                        self.currentPlayer = 'O'

            if not self.entorno.finalizado() and self.currentPlayer == 'O':
                agente_actual = self.entorno.agentes[1]  
                self.entorno.percibir(agente_actual)
                self.entorno.ejecutar(agente_actual)
                self.dibujar_tablero()

                if self.entorno.finalizado():
                    jugando = False
                    break

                self.currentPlayer = 'X'

            if self.entorno.finalizado():
                if self.entorno.ganador() == self.agente1.jugador:
                    self.mostrar_mensaje("GANASTE", (0, 255, 0))  
                elif self.entorno.ganador() == self.agente2.jugador:
                    self.mostrar_mensaje("PERDISTE", (255, 0, 0))  
                else:
                    self.mostrar_mensaje("EMPATASTE", (255, 0, 0))  

                pygame.display.flip()  
                pygame.time.delay(4000) 
                jugando = False

            pygame.time.delay(500)

        pygame.quit()

    def mostrar_mensaje(self, mensaje, color):
        self.screen.fill((255, 255, 255))
        fuente = pygame.font.Font(None, 64)
        texto = fuente.render(mensaje, True, color)
        self.screen.blit(texto, (self.width // 2 - texto.get_width() // 2, self.height // 2 - texto.get_height() // 2))
        pygame.display.flip()

