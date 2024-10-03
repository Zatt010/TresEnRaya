from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@socketio.on("hacer_movimiento")
def handle_hacer_movimiento(data):
    # Actualiza el estado del juego
    self.entorno.estado = data["estado"]
    self.entorno.ejecutar(agente_actual)
    self.dibujar_tablero()
    self.socketio.emit("actualizar_estado_juego", {"estado": self.entorno.estado})

if __name__ == "__main__":
    socketio.run(app)