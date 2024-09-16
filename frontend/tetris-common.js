// Define block colors
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

// Shared function to draw the Tetris board with the correct colors
/**
 *
 * @param {number[][]} board - The Tetris board represented as a 2D array
 */
function drawBoard(board, canvasId) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext("2d");
  const blockSize = 40;

  // Clear the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let y = 0; y < board.length; y++) {
    for (let x = 0; x < board[y].length; x++) {
      const blockType = board[y][x];
      const color = COLORS[blockType];

      // Only draw the block if it's not an empty block
      if (blockType !== 0) {
        ctx.fillStyle = color;
        ctx.fillRect(x * blockSize, y * blockSize, blockSize, blockSize);
      }
    }
  }
}
