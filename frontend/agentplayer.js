const agentSelect = document.getElementById("agent-select");
const startDemoBtn = document.getElementById("start-demo");
let wsAgent = null; // WebSocket connection for agent demo

// Fetch available agents from the server and populate the dropdown
async function loadAgents() {
  const response = await fetch("http://127.0.0.1:8000/agents");
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
  if (wsAgent) {
    wsAgent.close();
  }

  wsAgent = new WebSocket(`ws://127.0.0.1:8000/ws/demo/${selectedAgent}`);

  wsAgent.onopen = function () {
    console.log(`WebSocket connection established with ${selectedAgent} agent`);
  };

  wsAgent.onmessage = function (event) {
    const gameState = JSON.parse(event.data);
    console.log("Game state received from server:", gameState);
    drawBoard(gameState.board); // Render the updated board using shared function
  };

  wsAgent.onclose = function () {
    console.log("WebSocket connection closed");
  };

  wsAgent.onerror = function (error) {
    console.error("WebSocket error:", error);
  };
}

// Load the agents when the page is loaded
window.addEventListener("load", loadAgents);

// Start the demo when the button is clicked
startDemoBtn.addEventListener("click", startDemo);
