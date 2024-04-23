import random
import copy

from enum import Enum, auto

from src.game.block import Block


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

    def __init__(self, board: list[list[int]] = None, block: Block = None):
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
        self.prevBoard = copy.deepcopy(self.board)

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
        return copy.deepcopy(self.board)

    def doAction(self, action: Action) -> None:
        """
        Performs the specified action on the current block and updates the game board accordingly.

        Args:
            action (Action): The action to perform, as defined in the Action enumeration.
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
        if (
            action in [Action.HARD_DROP, Action.SOFT_DROP]
            and not self.isValidBlockPosition(new_block)
        ):
            new_block.moveUp()
            self.blockHasLanded = True
        if self.isValidBlockPosition(new_block):
            self.block = new_block
            self._placeBlock()

        
    def updateBoard(self):
        self.blockHasLanded = False
        self._checkForFullRows()
        self._checkGameOver()
        # Store the previous board state before the new block placement
        self.prevBoard = copy.deepcopy(self.board)
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

        if self._outOfBounds(block):
            return False

        if self._intersects(block):
            return False

        if self.isGameOver():
            return False

        return True

    def _outOfBounds(self, block: Block) -> bool:
        """Checks if the block is out of bounds"""
        for row in range(4):
            for column in range(4):
                if row * 4 + column in block.image():
                    if (
                        row + block.y > self.ROWS - 1
                        or row + block.y < 0
                        or column + block.x > self.COLUMNS - 1
                        or column + block.x < 0
                    ):
                        return True

        return False

    def _intersects(self, block: Block) -> bool:
        """Checks if the block intersects with another block on the board"""
        for row in range(4):
            for column in range(4):
                if row * 4 + column in block.image():
                    # Check if the block intersects with the board
                    # That is, if the block is on top of another block that is not itself
                    blockOverlaps = self.prevBoard[row + block.y][column + block.x] > 0
                    isItSelf = (
                        block.x + column == self.block.x
                        and block.y + row == self.block.y
                    )

                    if blockOverlaps and not isItSelf:
                        return True
        return False

    def isGameOver(self):
        return self.gameOver

    def _placeBlock(self):
        """Places the current block on the board"""
        self.board = copy.deepcopy(self.prevBoard)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][
                        j + self.block.x
                    ] = self.block.type + 1  # implicit color 1 to 7
        

    def _shiftToNewBlock(self):
        """Places the current block on the board and sets the next block as the current block"""
        self.prevBlock = self.block.copy()
        self.block = self.nextBlock
        self.nextBlock = Block(self.START_X, self.START_Y, random.randint(0, 6))
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][
                        j + self.block.x
                    ] = self.block.type + 1  # implicit color 1 to 7

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
        self.prevBoard = copy.deepcopy(self.board)

    def getPossibleBoards(self) -> list["Tetris"]:
        possibleMoves = []

        # Number of rotations which gives unique block positions
        if self.block.type < 3:
            rotations = 2
        elif self.block.type < 6:
            rotations = 4
        else:
            rotations = 1

        rotationBoard = copy.deepcopy(self)
        for _ in range(rotations):
            for column in range(0, self.COLUMNS + (4 - self.block.getRightmostImageCoordinate())):
                moveBoard = copy.deepcopy(rotationBoard)

                # Calibrate the to the left
                toLeft = moveBoard.block.x + moveBoard.block.getLeftmostImageCoordinate()
                for _ in range(toLeft + 1):
                    moveBoard.doAction(Action.MOVE_LEFT)
                # Move the block to the correct column
                for _ in range(column):
                    moveBoard.doAction(Action.MOVE_RIGHT)

                moveBoard.doAction(Action.HARD_DROP)
                if not moveBoard.isValidBlockPosition(moveBoard.block):
                    continue

                moveBoard.prevBoard = copy.deepcopy(moveBoard.board)
                if moveBoard not in possibleMoves:
                    possibleMoves.append(moveBoard)

            rotationBoard.doAction(Action.ROTATE_CLOCKWISE)

        return possibleMoves

    def __eq__(self, other: "Tetris") -> bool:
        if not isinstance(other, Tetris):
            return False

        # Check if the blocks are the same
        for r in range(self.ROWS):
            for c in range(self.COLUMNS):
                if self.board[r][c] != other.board[r][c]:
                    return False

        return True

    def printBoard(self):
        print("_______________________________________")
        for row in self.board:
            print("|" + "   ".join(self._checkCharacter(cell) for cell in row) + "|")

        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    def _checkCharacter(self, character) -> str:
        if character >= 1:
            return "■"
        else:
            return "▧"


def transition_model(current_state: Tetris, target_state: Tetris) -> list[Action]:
    """
    Calculates the sequence of actions required to transition from the current board state to the target board state.

    Args:
        current_state (Board): The current state of the Tetris board.
        target_state (Board): The desired target state of the board.

    Returns:
        list[Action]: A list of actions that need to be performed to achieve the target state.
    """

    actions = []

    if current_state == target_state:
        actions.append(Action.SOFT_DROP)
        print("No transition needed")
        return actions

    # Find where the last block is in the target state
    target_block = target_state.block

    # Find the correct rotation
    needed_rotation = target_block.rotation - current_state.block.rotation
    actions += [Action.ROTATE_CLOCKWISE] * needed_rotation

    # Move the block to the correct x and y position
    if current_state.block.x < target_block.x:
        actions += [Action.MOVE_RIGHT] * (target_block.x - current_state.block.x)
    elif current_state.block.x > target_block.x:
        actions += [Action.MOVE_LEFT] * (current_state.block.x - target_block.x)
    # Move the block down to the correct y position as it would be used in reality
    actions.append(Action.HARD_DROP)

    return actions
