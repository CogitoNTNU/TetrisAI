const ws = new WebSocket("ws://127.0.0.1:8000/ws/game");

const canvas = document.getElementById("game-canvas");
const ctx = canvas.getContext("2d");

// Define the same color scheme as in the Python code
const COLORS = [
  "rgba(0, 0, 0, 0)", // No color (transparent)
  "rgb(0, 255, 255)", // I block (cyan)
  "rgb(255, 0, 0)", // Z block (red)
  "rgb(0, 255, 0)", // S block (green)
  "rgb(255, 165, 0)", // L block (orange)
  "rgb(0, 0, 255)", // J block (blue)
  "rgb(128, 0, 128)", // T block (purple)
  "rgb(255, 255, 0)", // O block (yellow)
];

ws.onopen = function () {
  console.log("WebSocket connection established");
};

ws.onmessage = function (event) {
  const gameState = JSON.parse(event.data);
  console.log("Game state received from server:", gameState);
  drawBoard(gameState.board); // Render the updated board
};

ws.onclose = function () {
  console.log("WebSocket connection closed");
};

ws.onerror = function (error) {
  console.error("WebSocket error:", error);
};

// Draw the Tetris board with the correct colors
function drawBoard(board) {
  const blockSize = 40; // Size of each block
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

  for (let y = 0; y < board.length; y++) {
    for (let x = 0; x < board[y].length; x++) {
      const blockType = board[y][x];
      const color = COLORS[blockType]; // Get the color based on the block type

      if (blockType !== 0) {
        // Don't draw for empty spaces
        ctx.fillStyle = color;
        ctx.fillRect(x * blockSize, y * blockSize, blockSize, blockSize);
      }
    }
  }
}

// Sending input events to the server
window.addEventListener("keydown", function (e) {
  if (e.key === "ArrowDown") {
    ws.send("SOFT_DROP");
  } else if (e.key === "ArrowLeft") {
    ws.send("MOVE_LEFT");
  } else if (e.key === "ArrowRight") {
    ws.send("MOVE_RIGHT");
  } else if (e.key === " ") {
    ws.send("HARD_DROP");
  } else if (e.key === "ArrowUp") {
    ws.send("ROTATE_CLOCKWISE");
  }
});
