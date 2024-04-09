from dataclasses import dataclass
import random

FIGURES = [
    # Definitions for each Tetris block rotation
    [[1, 5, 9, 13], [4, 5, 6, 7],   [2, 6, 10, 14], [8, 9, 10, 11]],    # I
    [[4, 5, 9, 10], [2, 6, 5, 9],   [0, 1, 5, 6],   [1, 5, 4, 8]],      # Z
    [[9, 10, 6, 7], [1, 5, 6, 10],  [5, 6, 2, 3],   [2, 6, 7, 11]],     # S
    [[1, 2, 5, 9],  [0, 4, 5, 6],   [1, 5, 9, 8],   [4, 5, 6, 10]],     # L
    [[1, 2, 6, 10], [5, 6, 7, 9],   [2, 6, 10, 11], [3, 5, 6, 7]],      # J
    [[1, 4, 5, 6],  [1, 4, 5, 9],   [4, 5, 6, 9],   [1, 5, 6, 9]],      # T
    [[1, 2, 5, 6]],                                                     # O
]

# Colors for the blocks
COLORS = [
    # RGB color definitions for each block type
    (0, 255, 255),  # I
    (255, 0, 0),    # Z
    (0, 255, 0),    # S
    (255, 165, 0),  # L
    (0, 0, 255),    # J
    (128, 0, 128),  # T
    (255, 255, 0),  # O
]


@dataclass
class Block:
    """
    Represents a Tetris block, encapsulating its position, type, rotation, and color.

    Attributes:
        x (int): The x-coordinate of the block on the Tetris grid.
        y (int): The y-coordinate of the block on the Tetris grid.
        rotation (int): The rotation state of the block, representing its orientation.
        type (int): The type of the block, determining its shape and color.
        color (tuple): The RGB color of the block.
    """

    def __init__(self, x: int, y: int, blockType: int = None):
        """
        Initializes a Block instance with specified x and y coordinates, and an optional block type.

        Parameters:
            x (int): The initial x-coordinate of the block.
            y (int): The initial y-coordinate of the block.
            blockType (int, optional): The type of the block. Randomly selected if not provided.
        """
        self.x = x
        self.y = y
        self.rotation = 0

        self.type = random.randint(0, 6) if blockType is None else blockType
        self.color = COLORS[self.type]

    def copy(self) -> "Block":
        """
        Creates a copy of the block with the same position, type, and rotation.

        Returns:
            Block: A new instance of Block with identical properties.
        """
        block = Block(self.x, self.y, self.type)
        block.rotation = self.rotation
        return block

    def setCoordinates(self, x: int, y: int):
        self.x = x
        self.y = y

    def rotateLeft(self):
        self.rotation = (self.rotation - 1) % len(FIGURES[self.type])

    def rotateRight(self):
        self.rotation = (self.rotation + 1) % len(FIGURES[self.type])

    def moveUp(self):
        self.y -= 1

    def moveDown(self):
        self.y += 1

    def moveLeft(self):
        self.x -= 1

    def moveRight(self):
        self.x += 1

    def image(self):
        return FIGURES[self.type][self.rotation]

    def getListCoordinates(self) -> list:
        """
        Calculates and returns the grid coordinates for each part of the block, based on its current position and orientation.

        Returns:
            list of tuple: A list of tuples (x, y) representing the grid coordinates of the block's parts.
        """
        imageList = self.image()
        listCoordinates = []
        for i in range(len(imageList)):
            x = 0
            y = 0
            listNr = imageList[i]
            restList = imageList[i] % 4
            divList = imageList[i] // 4

            if restList == 0:
                y = self.y + divList - 1
                x = self.x - 1

            elif restList == 1:
                y = self.y + divList - 1
                x = self.x

            elif restList == 2:
                y = self.y + divList - 1
                x = self.x + 1

            elif restList == 3:
                y = self.y + divList - 1
                x = self.x + 2

            listCoordinates.append((x, y))

        return listCoordinates
