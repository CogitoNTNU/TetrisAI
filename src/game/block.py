class Block:
    def __init__self(self, x, y, blockType):
        self.x = x
        self.y = y
        self.type = blockType
        self.color = blockType
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

    def rotate_left(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

    def rotate_right(self):
        self.rotation = (self.rotation - 1) % len(self.figures[self.type])

    def get_block(self):
        return self.figures[self.type][self.rotation]
    
    def get_color(self):
        return self.colors[self.type]
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    
    

