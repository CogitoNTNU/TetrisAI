baseScore = 100
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class TetrisGameManager:

    current_piece = None
    new_piece = None
    score = 0

    def __init__(self, board):
        self.board = board
        self.score = 0

    def rotate_piece(self, direction):
        self.current_piece.rotate(direction)


    def move_piece(self, direction):

        self.current_piece.move(direction)

    def drop_piece(self, newPiece):
        if self.legal_move(DOWN):
            self.move_piece(DOWN)

    def is_game_over(self):
        return self.board.is_game_over()

    def start_game(self):
        self.current_piece = self.next_piece()
        self.next_piece = self.next_piece()


    def legal_move(self, x, y):
        return self.board.legal_move(x, y)

    def clear_lines(self):
        lines_cleared = self.board.clear_lines()
        self.update_score(lines_cleared)

    def update_score(self, lines_cleared):
        self.score += baseScore**lines_cleared

    def place_piece(self, direction):
        x = direction[0]
        y = direction[1]
        if self.legal_move(x, y):
            self.board.place_piece(x, y, self.current_piece)

        if self.is_game_over():
            self.stop_game()
        
    def new_piece(self):
        return self.pieces.get_new_piece()
    
    def stop_game(self):
        self.board.stop_game()

print(DOWN.index(1))