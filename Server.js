const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

let players = {};  // Para almacenar los jugadores
let board = [];    // Tablero de tamaño dinámico
let currentPlayer = 'X';  // El primer jugador será 'X'
let boardSize = 3;  // Valor por defecto, pero será configurado dinámicamente

// Escuchar conexiones
io.on('connection', (socket) => {
  console.log(`Jugador conectado: ${socket.id}`);

  // Recibir el tamaño del tablero del primer jugador que se conecte
  socket.on('setBoardSize', (size) => {
    if (boardSize === 3) { // Solo se setea una vez
      boardSize = size;
      board = Array(boardSize * boardSize).fill(null);  // Inicializar el tablero dinámico
    }

    // Enviar el tamaño del tablero y el estado inicial a los jugadores
    socket.emit('gameState', { board, currentPlayer, boardSize });

    // Asignar el jugador X o O dependiendo del número de jugadores
    if (!players['X']) {
      players['X'] = socket.id;
      socket.emit('playerRole', 'X');
    } else if (!players['O']) {
      players['O'] = socket.id;
      socket.emit('playerRole', 'O');
    }
  });

  // Manejar el movimiento del jugador
  socket.on('playerMove', (data) => {
    const { fila, col, jugador } = data;
    const index = fila * boardSize + col;

    if (board[index] === null && jugador === currentPlayer) {
      board[index] = currentPlayer;
      currentPlayer = currentPlayer === 'X' ? 'O' : 'X';

      // Enviar el estado del tablero actualizado a todos los jugadores
      io.emit('gameState', { board, currentPlayer, boardSize });

      // Verificar si hay un ganador
      const winner = checkWinner(board);
      if (winner) {
        io.emit('gameOver', { winner });
        resetGame();
      }
    }
  });

  // Desconexión del jugador
  socket.on('disconnect', () => {
    console.log(`Jugador desconectado: ${socket.id}`);
    if (players['X'] === socket.id) {
      delete players['X'];
    } else if (players['O'] === socket.id) {
      delete players['O'];
    }
  });
});

// Verificar si hay un ganador
function checkWinner(board) {
  const winningCombinations = generateWinningCombinations(boardSize);
  for (let combination of winningCombinations) {
    const [a, b, c] = combination;
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return board[a]; // El ganador es 'X' o 'O'
    }
  }
  return null;
}

// Generar las combinaciones ganadoras dinámicamente
function generateWinningCombinations(size) {
  const combinations = [];

  // Filas
  for (let i = 0; i < size; i++) {
    const row = [];
    for (let j = 0; j < size; j++) {
      row.push(i * size + j);
    }
    combinations.push(row);
  }

  // Columnas
  for (let i = 0; i < size; i++) {
    const col = [];
    for (let j = 0; j < size; j++) {
      col.push(j * size + i);
    }
    combinations.push(col);
  }

  // Diagonal principal
  const diag1 = [];
  for (let i = 0; i < size; i++) {
    diag1.push(i * size + i);
  }
  combinations.push(diag1);

  // Diagonal secundaria
  const diag2 = [];
  for (let i = 0; i < size; i++) {
    diag2.push(i * size + (size - i - 1));
  }
  combinations.push(diag2);

  return combinations;
}

// Reiniciar el juego
function resetGame() {
  board = Array(boardSize * boardSize).fill(null);
  currentPlayer = 'X';
}

server.listen(5000, () => {
  console.log('Servidor escuchando en el puerto 5000');
});
