from copy import deepcopy
import time
import asyncio
import json
from src.agents.agent import Agent, playGameDemoStepByStep
from src.game.tetris import Action, Tetris


class TetrisGameManager:
    def __init__(self, board: Tetris, websocket):
        """
        Initialize the game manager with a board of type Tetris and a WebSocket connection.
        """
        self.board = board  # Ensure board is of type Tetris
        self.websocket = websocket  # WebSocket connection for real-time communication
        self.score = 0
        self.currentTime = int(round(time.time() * 1000))
        self.updateTimer = 1  # Timer to control piece dropping
        self.base_fall_delay = (
            1  # Base delay for blocks to fall automatically (in seconds)
        )
        self.fall_delay = self.base_fall_delay  # The actual delay for the current speed
        self.last_fall_time = time.time()  # Track the last time the block fell

    async def movePiece(self, direction: Action):
        """Move the Tetris block in a given direction and send updated game state via WebSocket."""
        self.board.doAction(direction)
        await self.send_game_state()  # Send updated state after action

    def isGameOver(self):
        """Check if the game is over."""
        return self.board.isGameOver()

    def update_fall_delay(self):
        """Update the fall delay based on the score."""
        # For every 10 rows removed (or points scored), decrease the fall delay
        # Ensure it does not go below a minimum fall delay (e.g., 0.1 seconds)
        self.fall_delay = max(self.base_fall_delay - (self.score // 10) * 0.1, 0.1)
        print(f"Updated fall delay: {self.fall_delay}")

    async def startGame(self):
        """Start the game loop for a normal game, receiving inputs and sending game state via WebSocket."""
        await self.send_game_state()  # Send initial game state

        while not self.board.gameOver:
            try:
                # Track the time and automatically move the block down if enough time has passed
                current_time = time.time()
                if current_time - self.last_fall_time >= self.fall_delay:
                    await self.movePiece(Action.SOFT_DROP)
                    self.last_fall_time = current_time

                # Receive player input, but don't reset the fall delay
                try:
                    input_action = await asyncio.wait_for(
                        self.websocket.receive_text(), timeout=0.1
                    )
                    await self.handle_input(input_action)
                except asyncio.TimeoutError:
                    pass  # No input received within 0.1 seconds, keep the block falling

                # Update the board after block lands
                if self.board.blockHasLanded:
                    self.board.updateBoard()
                    self.score += 1  # Increase score each time a block lands
                    self.update_fall_delay()  # Adjust fall speed based on the new score

                await self.send_game_state()  # Send updated state

            except Exception as e:
                print(f"Error in game loop: {e}")
                break

        await self.stopGame()

    async def startDemo(self, agent: Agent):
        """Start the game loop for a demo game with an agent, sending updates via WebSocket."""
        await self.send_game_state()  # Send game state to client
        while not self.board.gameOver:
            playGameDemoStepByStep(agent, self.board)  # Agent plays step by step
            await asyncio.sleep(0.1)  # Small delay to simulate gameplay
            await self.send_game_state()  # Send updated state

        await self.stopGame()

    async def handle_input(self, input_action):
        """Handle input from the client received via WebSocket."""
        if input_action == "SOFT_DROP":
            await self.movePiece(Action.SOFT_DROP)
        elif input_action == "MOVE_LEFT":
            await self.movePiece(Action.MOVE_LEFT)
        elif input_action == "MOVE_RIGHT":
            await self.movePiece(Action.MOVE_RIGHT)
        elif input_action == "HARD_DROP":
            await self.movePiece(Action.HARD_DROP)
        elif input_action == "ROTATE_CLOCKWISE":
            await self.movePiece(Action.ROTATE_CLOCKWISE)

    async def send_game_state(self):
        """Send the current game state to the client via WebSocket."""
        temp = deepcopy(self.board)
        temp_board = temp.board[3:]  # Skip the top hidden rows
        game_state = {
            "board": temp_board,
            "score": self.score,
            "gameOver": self.isGameOver(),
        }
        await self.websocket.send_text(json.dumps(game_state))

    async def stopGame(self):
        """Handle game over logic."""
        await self.websocket.close()
        print("Game Over")
        print(self.board.board)
