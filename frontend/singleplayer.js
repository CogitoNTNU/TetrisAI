// WebSocket connection for single-player mode
const singleplayerWebSocket = new WebSocket("ws://127.0.0.1:8000/ws/game");

singleplayerWebSocket.onopen = () => {
  console.log("Single-player WebSocket connection established");
};

singleplayerWebSocket.onmessage = (event) => {
  const gameState = JSON.parse(event.data);
  console.log("Game state received from server:", gameState);
  drawBoard(gameState.board); // Render the updated board using shared function
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
