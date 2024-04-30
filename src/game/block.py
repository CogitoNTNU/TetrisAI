from dataclasses import dataclass
import random

FIGURES = [
    # Definitions for each Tetris block rotation

    [[4, 5, 6, 7],  [2, 6, 10, 14], [8, 9, 10, 11], [1, 5, 9, 13]],     # I
    [[0, 1, 5, 6],  [2, 5, 6, 9],   [4, 5, 9, 10],  [5, 8, 9, 12]],     # Z
    [[4, 5, 1, 2],  [1, 5, 6, 10],  [8, 9, 5, 6],   [0, 4, 5, 9]],      # S
    [[2, 4, 5, 6],  [1, 5, 9, 10],  [4, 5, 6, 8],   [0, 1, 5, 9]],      # L
    [[0, 4, 5, 6],  [1, 2, 5, 9],   [4, 5, 6, 10],  [1, 5, 8, 9]],      # J
    [[1, 4, 5, 6],  [1, 5, 6, 9],   [4, 5, 6, 9],   [1, 4, 5, 9]],      # T
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

        random.seed(0)
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
    

    def getListCoordinates(self) -> list[tuple[int, int]]:
        """
        Calculates and returns the grid coordinates for each part of the block, based on its current position and orientation.

        Returns:
            list of tuple: A list of tuples (x, y) representing the grid coordinates of the block's parts.
        """
        listCoordinates = []
        for i in self.image():
            x = i % 4
            y = i // 4
            listCoordinates.append((self.x + x, self.y + y))
          

        return listCoordinates

    def getLeftmostImageCoordinate(self) -> int:
        """
        Returns:
            int: The leftmost x-coordinate of the block's image.
        """
        leftmost = 4
        for i in self.image():
            x = i % 4
            if x < leftmost:
                leftmost = x
        return leftmost
    
    def getRightmostImageCoordinate(self) -> int:
        """
        Returns:
            int: The rightmost x-coordinate of the block's image.
        """
        rightmost = 0
        for i in self.image():
            x = i % 4
            if x > rightmost:
                rightmost = x
        return rightmost
    
    def getLowestImageCoordinate(self) -> int:
        """
        Returns:
            int: The bottommost y-coordinate of the block's image.
        """
        botmost = 0
        for i in self.image():
            y = i // 4
            if y > botmost:
                botmost = y
        return botmost
    