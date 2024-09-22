import time
import asyncio
import json
from fastapi import WebSocket

from src.agents.agent import Agent, playGameDemoStepByStep
from src.game.tetris import Action, Tetris


class TetrisGameManager:
    def __init__(self, board: Tetris, websocket: WebSocket):
        """
        Initialize the game manager with a board of type Tetris and a WebSocket connection.
        """
        self.board = board
        self.websocket = websocket  # WebSocket connection for real-time communication
        self.current_time = int(round(time.time() * 1000))
        self.update_timer = 1  # Timer to control piece dropping

        self.start_fall_delay_in_seconds = 1
        self.current_fall_delay = self.start_fall_delay_in_seconds
        self.last_fall_time = time.time()
        self.fastest_fall_delay = 0.1

    async def movePiece(self, direction: Action):
        """Move the Tetris block in a given direction and send updated game state via WebSocket."""
        self.board.doAction(direction)
        await self.send_game_state()

    def isGameOver(self):
        """Check if the game is over."""
        return self.board.isGameOver()

    def update_fall_delay(self):
        """Update the fall delay based on the score."""
        # Speed up the block falling speed based on the number of lines cleared
        LINES_CLEAR_FOR_LEVEL = 10
        LEVEL_SPEEDUP_FACTOR = 0.1

        self.current_fall_delay = max(
            self.start_fall_delay_in_seconds
            - (self.board.rowsRemoved // LINES_CLEAR_FOR_LEVEL) * LEVEL_SPEEDUP_FACTOR,
            self.fastest_fall_delay,
        )
        print(f"Updated fall delay: {self.current_fall_delay}")

    async def startGame(self):
        """Start the game loop for a normal game, receiving inputs and sending game state via WebSocket."""
        # Send initial game state
        await self.send_game_state()

        while not self.board.gameOver:
            try:
                # Track the time and automatically move the block down if enough time has passed
                current_time = time.time()
                if current_time - self.last_fall_time >= self.current_fall_delay:
                    await self.movePiece(Action.SOFT_DROP)
                    self.last_fall_time = current_time

                # Receive player input, but don't reset the fall delay
                try:
                    input_action = await asyncio.wait_for(
                        self.websocket.receive_text(), timeout=0.1
                    )
                    await self.handle_input(input_action)
                except asyncio.TimeoutError:
                    # No input received within 0.1 seconds, keep the block falling
                    pass

                # Update the board after block lands
                if self.board.blockHasLanded:
                    self.board.updateBoard()
                    self.update_fall_delay()

                await self.send_game_state()

            except Exception as e:
                print(f"Error in game loop: {e}")
                break

        await self.stopGame()

    async def startDemo(self, agent: Agent):
        """Start the game loop for a demo game with an agent, sending updates via WebSocket."""
        # Send game state to client
        await self.send_game_state()
        while not self.board.gameOver:
            playGameDemoStepByStep(agent, self.board)
            await asyncio.sleep(0.1)  # Small delay to simulate gameplay
            await self.send_game_state()

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

        # Determine the landing position of the block
        simulated_board = self.board.copy()
        while simulated_board.isValidBlockPosition(simulated_board.block):
            simulated_board.block.moveDown()
        simulated_board.block.moveUp()

        # Mark the landing position of the block on the board
        LANDING_BLOCK_COLOR = -1
        for i in range(4):
            for j in range(4):
                if i * 4 + j in simulated_board.block.image():
                    simulated_board.board[i + simulated_board.block.y][
                        j + simulated_board.block.x
                    ] = LANDING_BLOCK_COLOR

        # Skip the top hidden rows for the visible board
        visible_board = simulated_board.board[3:]

        game_state = {
            "nextBlock": self.board.nextBlock.type,
            "board": visible_board,
            "score": self.board.rowsRemoved,
            "gameOver": self.isGameOver(),
            "nextPiece": self.board.nextBlock.type,
        }

        await self.websocket.send_text(json.dumps(game_state))

    async def stopGame(self):
        """Handle game over logic."""
        await self.websocket.close()
        print("Game Over")
        print(f"Final Score: {self.board.rowsRemoved}")
