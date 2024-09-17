import { BASE_URL, WS_BASE_URL } from "./routes.js";
import { drawBoard } from "./tetris-common.js";

// DOM elements
const agentSelect = document.getElementById("agent-select");
const startDemoBtn = document.getElementById("start-demo");
let agentWebSocket = null;

const canvasAgentId = "agentplayer-canvas";

// Fetch available agents from the server and populate the dropdown
async function loadAgents() {
  const response = await fetch(`${BASE_URL}/agents`);
  const agents = await response.json();

  agents.forEach((agent) => {
    const option = document.createElement("option");
    option.value = agent;
    option.textContent = agent;
    agentSelect.appendChild(option);
  });
}

// Start WebSocket connection for agent demo
function startDemo() {
  const selectedAgent = agentSelect.value;

  // Close the existing WebSocket connection if any
  if (agentWebSocket) {
    agentWebSocket.close();
  }

  agentWebSocket = new WebSocket(`${WS_BASE_URL}/demo/${selectedAgent}`);

  agentWebSocket.onopen = () => {
    console.log(`WebSocket connection established with ${selectedAgent} agent`);
  };

  agentWebSocket.onmessage = (event) => {
    const gameState = JSON.parse(event.data);
    console.log("Game state received from server:", gameState);
    // Render the updated board using shared function
    drawBoard(gameState.board, canvasAgentId);
  };

  agentWebSocket.onclose = () => {
    console.log("WebSocket connection closed");
  };

  agentWebSocket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
}

window.addEventListener("keydown", (e) => {
  if (e.key === " ") {
    e.preventDefault(); // Prevent default spacebar scrolling
  }
});
// Load the agents when the page is loaded
window.addEventListener("load", loadAgents);

// Start the demo when the button is clicked
startDemoBtn.addEventListener("click", startDemo);
