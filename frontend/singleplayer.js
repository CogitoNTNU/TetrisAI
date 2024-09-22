import { WS_BASE_URL } from "./routes.js";
import { drawBoard } from "./tetris-common.js";

const singleplayerWebSocket = new WebSocket(`${WS_BASE_URL}/game`);
console.log(WS_BASE_URL);

const canvasSinglePlayerId = "singleplayer-canvas";

singleplayerWebSocket.onopen = () => {
  console.log("Single-player WebSocket connection established");
};

singleplayerWebSocket.onmessage = (event) => {
  const gameState = JSON.parse(event.data);
  console.log("Game state received from server:", gameState);
  drawBoard(gameState.board, canvasSinglePlayerId);
};

singleplayerWebSocket.onclose = () => {
  console.log("Single-player WebSocket connection closed");
};

singleplayerWebSocket.onerror = (error) => {
  console.error("WebSocket error:", error);
};

// Sending input events to the server
window.addEventListener("keydown", (e) => {
  if (e.key === "ArrowDown") {
    singleplayerWebSocket.send("SOFT_DROP");
  } else if (e.key === "ArrowLeft") {
    singleplayerWebSocket.send("MOVE_LEFT");
  } else if (e.key === "ArrowRight") {
    singleplayerWebSocket.send("MOVE_RIGHT");
  } else if (e.key === " ") {
    singleplayerWebSocket.send("HARD_DROP");
  } else if (e.key === "ArrowUp") {
    singleplayerWebSocket.send("ROTATE_CLOCKWISE");
  }
});
