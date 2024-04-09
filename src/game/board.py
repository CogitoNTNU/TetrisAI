import random
import copy
from enum import Enum, auto

from src.game.block import Block


class Action(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    ROTATE_CLOCKWISE = auto()
    ROTATE_COUNTERCLOCKWISE = auto()
    DROP = auto()
    SOFT_DROP = auto()


class Board:
    rows = 20
    columns = 10

    def __init__(self):
        self.gameOver = False
        self.rowsRemoved = 0

        self.board = self._initBoard()
        self.prevBoard = copy.deepcopy(self.board)

        self.block = Block(3, 0, 0)
        self.placeBlock()

        self.nextBlock = Block(0, 5, random.randint(0, 6))

    def _initBoard(self) -> list[list[int]]:
        """Initializes an empty the board"""
        board = []
        for r in range(0, self.rows):
            row = []
            for c in range(0, self.columns):
                row.append(0)
            board.append(row)
        return board

    def getBoard(self) -> list[list[int]]:
        return copy.deepcopy(self.board)

    def doAction(self, action: Action) -> None:
        """Performs the specified action on the board"""

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
            case Action.DROP:
                while True:
                    new_block.moveDown()
                    if not self.isValidBlockPosition(new_block):
                        new_block.moveUp()
                        break
            case Action.SOFT_DROP:
                new_block.moveDown()

        # Given the new block position, check if it is valid and update the board
        if self.isValidBlockPosition(new_block):
            print("Valid move")
            self.block = new_block
            self.placeBlock()

    def isValidBlockPosition(self, block: Block) -> bool:
        """Checks if the block can move in the specified direction"""

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
                        row + block.y > self.rows - 1
                        or row + block.y < 0
                        or column + block.x > self.columns - 1
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
                        or block.y + row == self.block.y
                    )

                    if blockOverlaps and not isItSelf:
                        return True
        return False

    def isGameOver(self):
        return self.gameOver

    def blockLanded(self):
        pass

    def placeBlock(self):
        """Places the current block on the board"""
        self.board = copy.deepcopy(self.prevBoard)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][
                        j + self.block.x
                    ] = 1  # self.block.color
        return (
            self.checkGameState()
        )  # hvis denne sjekkes hver gang og gir false, var det ikke mulig å plassere blokken og spillet er over ffs.

    def newBlock(self):
        """Creates a new block and places it on the board"""
        self.block = Block(0, 5, random.randint(0, 6))
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][
                        j + self.block.x
                    ] = 1  # self.block.color
        return (
            self.checkGameState()
        )  # hvis denne sjekkes hver gang og gir false, var det ikke mulig å plassere blokken og spillet er over ffs.

    def checkGameState(self) -> int:
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
        newMatrix.append([0 for _ in range(self.columns)])
        self.board = newMatrix  # Oppdaterer matrisen med den nye matrisen
        self.rowsRemoved += 1  # Oppdaterer antall fjernede rader

    def getPossibleMoves(self) -> list["Board"]:
        possibleMoves = []
        firstRotation = self.block.rotation
        currentRotation = firstRotation

        while True:
            for i in range(self.columns):
                moveBoard = copy.deepcopy(self)
                moveBoard.block.setCoordinates(i, 0)
                for j in range(currentRotation):
                    moveBoard.block.rotateRight()
                moveBoard.placeBlock()

                while moveBoard.isValidBlockPosition(moveBoard.block.moveDown):
                    moveBoard.block.moveDown()

                possibleMoves.append(copy.deepcopy(moveBoard))

            moveBoard.block.rotateRight()
            currentRotation += 1

            if moveBoard.block.rotation != firstRotation:
                continue
            else:
                break

    def printBoard(self):
        print("_______________________________________")
        for row in self.board:
            print("|" + "   ".join(self.checkCharacter(cell) for cell in row) + "|")

        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    def checkCharacter(self, character) -> str:
        if character == 1:
            return "■"
        else:
            return "▧"


def transition_model(current_state: Board, target_state: Board) -> list[Action]:
    """
    Returns the sequence of actions needed to transition from the current state to the target state.

    Args:
        new_state: The new state to transition to

    Returns:
        The resulting state
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
