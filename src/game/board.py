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


class Board:
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

    ROWS = 20
    COLUMNS = 10

    def __init__(self, board=None, block=None):
        """
        Initializes a new game board instance, setting up an empty board, placing the first block, and selecting the next block.
        """
        self.gameOver = False
        self.rowsRemoved = 0

        if board == None:
            self.board = self._initBoard()
        else:
            self.board = board
        if block == None:
            self.block = Block(3, 0, 0)
        else:
            self.block = block
        self.prevBoard = copy.deepcopy(self.board)

        self._placeBlock()

        self.nextBlock = Block(0, 5, random.randint(0, 6))

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
        match action:
            case Action.MOVE_LEFT:
                new_block.moveLeft()
            case Action.MOVE_RIGHT:
                new_block.moveRight()
            case Action.ROTATE_CLOCKWISE:
                new_block.rotateRight()
            case Action.ROTATE_COUNTERCLOCKWISE:
                new_block.rotateLeft()
            case Action.HARD_DROP:
                while True:
                    new_block.moveDown()
                    self.printBoard()
                    if not self.isValidBlockPosition(new_block):
                        new_block.moveUp()
                        break
            case Action.SOFT_DROP:
                new_block.moveDown()

        # Given the new block position, check if it is valid and update the board
        if self.isValidBlockPosition(new_block):
            print("Valid move")
            self.block = new_block
            self._placeBlock()

    def isValidBlockPosition(self, block: Block) -> bool:
        """
        Checks if the given block's position is valid (not out of bounds, not intersecting with existing blocks, and not causing a game over).

        Args:
            block (Block): The block to check.

        Returns:
            bool: True if the block's position is valid, False otherwise.
        """

        if self._outOfBounds(block):
            print("[DEBUG] Out of bounds")
            return False

        if self._intersects(block):
            print("[DEBUG] Intersects")
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
        ##  TODO: Fix this
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
                    ] = 1  # self.block.color

    def _shiftToNewBlock(self):
        """Places the current block on the board and sets the next block as the current block"""
        self.block = self.nextBlock
        self.nextBlock = Block(0, 5, random.randint(0, 6))
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][
                        j + self.block.x
                    ] = 1  # self.block.color

    def _checkGameState(self) -> int:
        amount = 0
        fullRows = []

        for rowIndex, row in enumerate(
            self.board
        ):  # Itererer over matrisen for å finne fulle rader
            if 0 not in row:  # Sjekker om raden er full
                fullRows.append(
                    rowIndex
                )  # Legger til indeksen til listen over fulle rader
        for rowIndex in reversed(
            fullRows
        ):  # Går gjennom listen over fulle rader i reversert rekkefølge for å fjerne dem
            self._clearRow(rowIndex)  # Fjerner raden basert på dens indeks
            amount += 1  # Øker telleren for antall fjernede rader
        return amount  # Returnerer totalt antall fjernede rader

    def _clearRow(self, rownumber: int):
        """Clears the specified row and moves all rows above down one step"""
        # Fjerner den angitte raden og legger til en ny tom rad ved bunnen av matrisen
        newMatrix = self.board[:rownumber] + self.board[rownumber + 1 :]
        newMatrix.append([0 for _ in range(self.COLUMNS)])
        self.board = newMatrix  # Oppdaterer matrisen med den nye matrisen
        self.rowsRemoved += 1  # Oppdaterer antall fjernede rader

    def getPossibleMoves(self) -> list["Board"]:
        possibleMoves = []

        # Number of rotations which gives unique block positions
        if self.block.type < 3:
            rotations = 2
        elif self.block.type < 6:
            rotations = 4
        else:
            rotations = 1

        for _ in range(rotations):
            for column in range(self.COLUMNS):
                moveBoard = copy.deepcopy(self)
                moveBoard.block.setCoordinates(column - 1, 0)

            if moveBoard.isValidBlockPosition(moveBoard.block):
                moveBoard.doAction(Action.HARD_DROP)

                if moveBoard.board not in possibleMoves:
                    possibleMoves.append(copy.deepcopy(moveBoard.board))

            moveBoard.block.rotateRight()

        return possibleMoves

    def __eq__(self, value: "Board") -> bool:
        for i in range(2):
            pass

        return True

    def printBoard(self):
        print("_______________________________________")
        for row in self.board:
            print("|" + "   ".join(self._checkCharacter(cell) for cell in row) + "|")

        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    def _checkCharacter(self, character) -> str:
        if character == 1:
            return "■"
        else:
            return "▧"


def transition_model(current_state: Board, target_state: Board) -> list[Action]:
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

    return actions
