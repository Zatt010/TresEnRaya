from Tablero import Tablero
import sys
# piezas_en_linea se define en main y en AgenteJugador y AgenteTresEnraya
if __name__ == "__main__":
    if len(sys.argv) > 2:
        tamano_tablero = int(sys.argv[1])
        piezas_en_linea = int(sys.argv[2])
    else:
        tamano_tablero = 6 
        piezas_en_linea = 3  

    tablero = Tablero(tamano_tablero, piezas_en_linea)
    tablero.run()
