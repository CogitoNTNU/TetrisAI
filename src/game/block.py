import random

import random

class Block:

    def __init__(self, x, y, blockType):
        self.x = x
        self.y = y
        self.type = random.randint(0, 6)        

        self.color = self.colors[random.randint(0,6)]        
        # self.type = random.randint(0,6)
        self.type = blockType
        self.color = self.colors[blockType]
        # self.color = random.choice(self.colors)
        # self.rotation = random.randint(0, len(self.figures[self.type]) - 1)
        self.rotation = 0
    

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],   # I
        [[4, 5, 9, 10], [2, 6, 5, 9]],   # Z 
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],   #L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # J
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # T
        [[1, 2, 5, 6]] # O
    ]

    # Colors for the blocks
    colors = [
        (0, 255, 255),  # I
        (255, 0, 0),    # Z
        (0, 255, 0),    # S
        (255, 165, 0),  # L
        (0, 0, 255),    # J
        (128, 0, 128),  # T
        (255, 255, 0)   # O
    ]


    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def rotate_left(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

    def rotate_right(self):
        self.rotation = (self.rotation - 1) % len(self.figures[self.type])

    def image(self): return self.figures[self.type][self.rotation]

    def move_down(self):
        self.y += 1
    
    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    
