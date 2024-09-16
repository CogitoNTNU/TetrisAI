// WebSocket connection for single-player mode
const wsSingleplayer = new WebSocket("ws://127.0.0.1:8000/ws/game");

wsSingleplayer.onopen = function () {
  console.log("Single-player WebSocket connection established");
};

wsSingleplayer.onmessage = function (event) {
  const gameState = JSON.parse(event.data);
  console.log("Game state received from server:", gameState);
  drawBoard(gameState.board); // Render the updated board using shared function
};

wsSingleplayer.onclose = function () {
  console.log("Single-player WebSocket connection closed");
};

wsSingleplayer.onerror = function (error) {
  console.error("WebSocket error:", error);
};

// Sending input events to the server
window.addEventListener("keydown", function (e) {
  if (e.key === "ArrowDown") {
    wsSingleplayer.send("SOFT_DROP");
  } else if (e.key === "ArrowLeft") {
    wsSingleplayer.send("MOVE_LEFT");
  } else if (e.key === "ArrowRight") {
    wsSingleplayer.send("MOVE_RIGHT");
  } else if (e.key === " ") {
    wsSingleplayer.send("HARD_DROP");
  } else if (e.key === "ArrowUp") {
    wsSingleplayer.send("ROTATE_CLOCKWISE");
  }
});
