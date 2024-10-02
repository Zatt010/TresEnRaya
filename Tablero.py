import pygame
from EntornoTresEnRaya import EntornoTresEnRaya
from HumanoTresEnRaya import HumanoTresEnRaya
from AgenteTresEnRaya import AgenteTresEnRaya
class Tablero:
    def __init__(self, n):
        pygame.init()
        self.n = n
        self.width = n * 100
        self.height = n * 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tres en Raya")
        
        self.entorno = EntornoTresEnRaya(n)  # Pass n to EntornoTresEnRaya
        self.agente1 = HumanoTresEnRaya(jugador='X', oponente='O')  # Proporciona el oponente
        self.agente2 = AgenteTresEnRaya(jugador='O', oponente='X')  # Proporciona el oponente
        self.entorno.insertar_objeto(self.agente1)
        self.entorno.insertar_objeto(self.agente2)
        
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

            if not self.entorno.finalizado():
                agente_actual = self.entorno.agentes[self.entorno.turno]
                self.entorno.percibir(agente_actual)
                self.entorno.ejecutar(agente_actual)
                self.dibujar_tablero()


            else:
                
                if self.entorno.ganador() == self.agente1.jugador:
                    self.mostrar_mensaje("GANASTE", (0, 255, 0))  
                elif self.entorno.ganador() == self.agente2.jugador:
                    self.mostrar_mensaje("PERDISTE", (255, 0, 0))  
                else:
                    self.mostrar_mensaje("EMPATASTE", (255, 0, 0))  

                pygame.time.delay(2000)  
                jugando = False

            pygame.time.delay(500)  
        pygame.quit()

    def mostrar_mensaje(self, mensaje, color):
        self.screen.fill((255, 255, 255))  
        fuente = pygame.font.Font(None, 64)
        texto = fuente.render(mensaje, True, color)
        self.screen.blit(texto, (self.width // 2 - texto.get_width() // 2, self.height // 2 - texto.get_height() // 2))
        pygame.display.flip()