import random
from copy import copy
import numpy as np

from enum import Enum, auto
from time import sleep

from src.game.block import Block

import heapq
from typing import List, Tuple, Dict

DEMO_SLEEP = 0.02


class Action(Enum):
    """Enumeration for the possible actions that can be performed on the board"""

    MOVE_LEFT = auto()
    """ Move the block to the left """
    MOVE_RIGHT = auto()
    """ Move the block to the right """
    ROTATE_CLOCKWISE = auto()
    """ Rotate the block clockwise """
    ROTATE_COUNTERCLOCKWISE = auto()
    """ Rotate the block counterclockwise """
    HARD_DROP = auto()
    """ Instantly drop the block to the lowest possible position """
    SOFT_DROP = auto()
    """ Move the block one step down """


def get_all_actions() -> list[Action]:
    return [
        Action.MOVE_LEFT,
        Action.MOVE_RIGHT,
        Action.ROTATE_CLOCKWISE,
        Action.ROTATE_COUNTERCLOCKWISE,
        Action.HARD_DROP,
        Action.SOFT_DROP,
    ]


class Tetris:
    """
    Represents the Tetris game board, handling block placements, movements, and rotations, as well as checking for game over conditions.

    Attributes:
        ROWS (int): Number of rows in the game board.
        COLUMNS (int): Number of columns in the game board.
        gameOver (bool): Flag indicating if the game is over.
        rowsRemoved (int): Count of the total rows removed during the game.
        board (list[list[int]]): The game board matrix, where 0 indicates an empty cell and 1 indicates a filled cell.
        prevBoard (list[list[int]]): A copy of the game board before the latest block placement, used to check for valid movements and intersections.
        block (Block): The current block being controlled by the player.
        nextBlock (Block): The next block that will be introduced to the board after the current block is placed.
    """

    ROWS = 23
    SPAWN_ROWS = 3
    COLUMNS = 10
    START_X = 3
    START_Y = 0

    def __init__(
        self,
        board: list[list[int]] = None,
        block: Block = None,
        nextBlock: Block = None,
    ):
        """
        Initializes a new game board instance, setting up an empty board, placing the first block, and selecting the next block.
        """
        self.gameOver = False
        self.rowsRemoved = 0

        if board is None:
            self.board = self._initBoard()
        else:
            self.board = board
        if block is None:
            self.block = Block(self.START_X, self.START_Y, 0)
        else:
            self.block = block

        if nextBlock == None:
            self.nextBlock = Block(self.START_X, self.START_Y, random.randint(0, 6))
        else:
            self.nextBlock = nextBlock

        self.prevBoard = self.deep_copy_list_of_lists(self.board)
        self._placeBlock()

        self.prevBlock = self.block.copy()
        self.nextBlock = Block(self.START_X, self.START_Y, random.randint(0, 6))
        self.blockHasLanded = False

    def _initBoard(self) -> list[list[int]]:
        """Initializes an empty the board"""
        board = []
        for r in range(0, self.ROWS):
            row = []
            for c in range(0, self.COLUMNS):
                row.append(0)
            board.append(row)
        return board

    def getBoard(self) -> list[list[int]]:
        return self.deep_copy_list_of_lists(self.board)

    def deep_copy_list_of_lists(self, original: list[list[int]]) -> list[list[int]]:
        copied = [row[:] for row in original]
        return copied

    def doAction(self, action: Action, demo: bool = False) -> None:
        """
        Performs the specified action on the current block and updates the game board accordingly.

        Args:
            action (Action): The action to perform, as defined in the Action enumeration.
            demo   (bool): If True, the action will be performed with a delay for demonstration purposes.
        """

        # Move the new block according to the action
        new_block = self.block.copy()
        if action == Action.MOVE_LEFT:
            new_block.moveLeft()
        elif action == Action.MOVE_RIGHT:
            new_block.moveRight()
        elif action == Action.ROTATE_CLOCKWISE:
            new_block.rotateRight()
        elif action == Action.ROTATE_COUNTERCLOCKWISE:
            new_block.rotateLeft()
        elif action == Action.HARD_DROP:
            while self.isValidBlockPosition(new_block):
                new_block.moveDown()
        elif action == Action.SOFT_DROP:
            new_block.moveDown()

        # For blocks reaching the bottom of the board, place the block and introduce a new one
        if action in [
            Action.HARD_DROP,
            Action.SOFT_DROP,
        ] and not self.isValidBlockPosition(new_block):
            new_block.moveUp()
            self.blockHasLanded = True
        if self.isValidBlockPosition(new_block):
            self.block = new_block
            self._placeBlock()
            if demo:
                sleep(DEMO_SLEEP)

    def updateBoard(self):
        self.blockHasLanded = False
        self._checkForFullRows()
        self._checkGameOver()
        # Store the previous board state before the new block placement
        self.prevBoard = self.deep_copy_list_of_lists(self.board)
        if self.isGameOver():
            return
        self._shiftToNewBlock()

    def isValidBlockPosition(self, block: Block) -> bool:
        """
        Checks if the given block's position is valid (not out of bounds, not intersecting with existing blocks, and not causing a game over).

        Args:
            block (Block): The block to check.

        Returns:
            bool: True if the block's position is valid, False otherwise.
        """
        return not (
            self._outOfBounds(block) or self._intersects(block) or self.isGameOver()
        )

    def _outOfBounds(self, block: Block) -> bool:
        """Checks if the block is out of bounds"""
        for cord in block.getListCoordinates():
            if (
                cord[0] < 0
                or cord[0] >= self.COLUMNS
                or cord[1] >= self.ROWS
                or cord[1] < 0
            ):
                return True

        return False

    def _intersects(self, block: Block) -> bool:
        """Checks if the block intersects with another block on the board"""
        for cord in block.getListCoordinates():
            if self.prevBoard[cord[1]][cord[0]] != 0:
                return True
        return False

    def isGameOver(self):
        return self.gameOver

    def _placeBlock(self):
        """Places the current block on the board"""
        self.board = self.deep_copy_list_of_lists(self.prevBoard)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][j + self.block.x] = (
                        self.block.type + 1
                    )  # implicit color 1 to 7

    def _shiftToNewBlock(self):
        """Places the current block on the board and sets the next block as the current block"""
        self.prevBlock = self.block.copy()
        self.block = self.nextBlock
        self.nextBlock = Block(self.START_X, self.START_Y, random.randint(0, 6))
        self._placeBlock()

    def _checkGameOver(self):
        """Checks if the game is over"""
        for spawn_row in range(self.SPAWN_ROWS):
            for cell in self.board[spawn_row]:
                if cell > 0:
                    self.gameOver = True
                    return

    def _checkForFullRows(self) -> int:
        """Checks the board for full rows and removes them, returning the number of rows removed"""
        amount = 0
        fullRows = []
        # Find all full rows
        for rowIndex, row in enumerate(self.board):
            # Check if the row is full
            if 0 not in row:
                fullRows.append(rowIndex)
        # Remove all full rows
        for rowIndex in fullRows:
            self._clearRow(rowIndex)
            amount += 1
        return amount

    def _clearRow(self, rownumber: int):
        """Clears the specified row and moves all rows above down one step"""
        # Remove the row and add a new empty row at the top
        newMatrix = self.board[:rownumber] + self.board[rownumber + 1 :]
        newMatrix.insert(0, [0 for _ in range(self.COLUMNS)])
        self.board = newMatrix
        self.rowsRemoved += 1
        self.prevBoard = self.deep_copy_list_of_lists(self.board)

    def checkBlockFits(self, block: Block, x, y) -> "Tetris":
        """Places the given block at the specified position on the board"""
        tetris = self.copy()
        tetris.block = block.copy()
        tetris.block.x = x
        tetris.block.y = y

        valid = tetris.isValidBlockPosition(tetris.block)

        if not valid:
            return None

        onTop = False
        for cord in tetris.block.getListCoordinates():
            if cord[1] == self.ROWS - 1:  # if the block is on the bottom
                onTop = True
                break
            elif (
                self.prevBoard[cord[1] + 1][cord[0]] != 0
            ):  # if the block is on top of another block
                onTop = True
                break

        if onTop:
            tetris._placeBlock()
            return tetris

        return None

    def getPossibleBoards(self) -> list["Tetris"]:
        possible_boards = []
        blockCopy = self.block.copy()

        if self.block.type <= 2:  # I Z S
            rotations = 2
        elif self.block.type == 6:  # O
            rotations = 1
        else:
            rotations = 4

        for rotation in range(rotations):
            blockCopy.rotation = rotation
            for y in range(self.ROWS, 0, -1):
                for x in range(
                    -blockCopy.getLeftmostImageCoordinate(),
                    self.COLUMNS - blockCopy.getLeftmostImageCoordinate(),
                ):
                    # if self.prevBoard[y][x] == 0:
                    tetris = self.checkBlockFits(blockCopy, x, y)
                    if tetris is not None:
                        tetris.prevBoard = self.deep_copy_list_of_lists(tetris.board)
                        possible_boards.append(tetris)

        return possible_boards

    def __eq__(self, other: "Tetris") -> bool:
        if not isinstance(other, Tetris):
            return False

        return self.board == other.board

    def copy(self) -> "Tetris":
        tetris = Tetris(
            self.deep_copy_list_of_lists(self.prevBoard),
            self.block.copy(),
            self.nextBlock.copy(),
        )
        return tetris

    def printBoard(self):
        print("_______________________")
        for row in self.board:
            print("|" + "".join(self._checkCharacter(cell) for cell in row) + "|")

        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    def _checkCharacter(self, character) -> str:
        if character >= 1:
            colors = ["⬜", "🟥", "🟩", "🟧", "🟦", "🟪", "🟨"]
            return colors[character - 1]
        else:
            return "⬛"


def heuristic(a: Block, b: Block) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_neighbors(board: Tetris, block: Block) -> List[Tuple[Block, Action]]:
    neighbors = []
    potential_moves = [
        (block.copy(), Action.ROTATE_CLOCKWISE),
        (block.copy(), Action.ROTATE_COUNTERCLOCKWISE),
        (block.copy(), Action.MOVE_LEFT),
        (block.copy(), Action.MOVE_RIGHT),
        (block.copy(), Action.SOFT_DROP),
    ]

    potential_moves[0][0].rotateRight()
    potential_moves[1][0].rotateLeft()
    potential_moves[2][0].moveLeft()
    potential_moves[3][0].moveRight()
    potential_moves[4][0].moveDown()

    for new_block, action in potential_moves:
        if board.isValidBlockPosition(new_block):
            neighbors.append((new_block, action))
    return neighbors


def reconstruct_path(
    came_from: Dict[Block, Tuple[Block, Action]], current: Block
) -> List[Action]:
    path = []
    while current in came_from:
        current, action = came_from[current]
        path.append(action)
    return path[::-1]


def transition_model(current_state: Tetris, target_state: Tetris) -> List[Action]:
    start = current_state.block
    goal = target_state.block

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor, action in get_neighbors(current_state, current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = (current, action)
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []
