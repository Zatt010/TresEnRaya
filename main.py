from Tablero import Tablero
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tamano_tablero = int(sys.argv[1])
    else:
        tamano_tablero = 3

    tablero = Tablero(tamano_tablero)
    tablero.run()