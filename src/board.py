import pygame
from constants import *
from enum import Enum

class BoardSquareState(Enum):
    EMPTY = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4

class ValidSquareState(Enum):
    NEUTRAL = 0
    INVALID = 1
    REQUIRED = 2

class Board:

    instance = None

    def __init__(self):
        Board.instance = self

        self.size_in_squares = 20
        self.size = self.size_in_squares*SQUARE_SIZE

        self.squares = [[BoardSquareState.EMPTY] * self.size_in_squares for x in range(self.size_in_squares)]

        


    def update(self):
        self.top = SCREEN_CENTER[1] - self.size/2
        self.bot = SCREEN_CENTER[1] + self.size/2
        self.left = SCREEN_CENTER[0] - self.size/2
        self.right = SCREEN_CENTER[0] + self.size/2

        self.rect = pygame.Rect(self.left, self.top, self.size, self.size)

    def draw(self, screen):
        pygame.draw.rect(screen,'darkgray', self.rect)

        line_color = (230, 230, 230)

        for i in range(1, self.size_in_squares):
            x = self.left + SQUARE_SIZE*i
            pygame.draw.line(screen, line_color, (x, self.top), (x, self.bot-1))

        for i in range(1, self.size_in_squares):
            y = self.top + SQUARE_SIZE*i
            pygame.draw.line(screen, line_color, (self.left, y), (self.right-1, y))


    def try_place_piece(self, piece, snap_left, snap_top):

        if not self.piece_on_board(piece, snap_left, snap_top):
            return False
        
        color_to_state = {
            'blue': BoardSquareState.BLUE,
            'red': BoardSquareState.RED,
            'green': BoardSquareState.GREEN,
            'yellow': BoardSquareState.YELLOW
        }

        starting_corners = {
            BoardSquareState.BLUE: (0, 0),
            BoardSquareState.RED: (19, 0),
            BoardSquareState.GREEN: (0, 19),
            BoardSquareState.YELLOW: (19, 19)
        }

        piece_state = color_to_state[piece.color]
        starting_corner = starting_corners[piece_state]

        left_grid_x, top_grid_y = self.screen_to_grid_pos(snap_left, snap_top)

        valid_squares = [[ValidSquareState.NEUTRAL] * self.size_in_squares for x in range(self.size_in_squares)]
        valid_squares[starting_corner[1]][starting_corner[0]] = ValidSquareState.REQUIRED

        for y in range(self.size_in_squares):
            for x in range(self.size_in_squares):

                # can't place overlapping with another piece
                if self.squares[y][x] != BoardSquareState.EMPTY:
                    valid_squares[y][x] = ValidSquareState.INVALID

                if self.squares[y][x] == piece_state:

                    # can't place next to your own piece
                    self.try_set_state(valid_squares, x-1, y, ValidSquareState.INVALID)
                    self.try_set_state(valid_squares, x+1, y, ValidSquareState.INVALID)
                    self.try_set_state(valid_squares, x, y-1, ValidSquareState.INVALID)
                    self.try_set_state(valid_squares, x, y+1, ValidSquareState.INVALID)

                    # have to place on corner of one of your pieces
                    self.try_set_state(valid_squares, x-1, y-1, ValidSquareState.REQUIRED)
                    self.try_set_state(valid_squares, x+1, y-1, ValidSquareState.REQUIRED)
                    self.try_set_state(valid_squares, x-1, y+1, ValidSquareState.REQUIRED)
                    self.try_set_state(valid_squares, x+1, y+1, ValidSquareState.REQUIRED)


        # need seperate loops for checking valid pos and setting states because otherwise,
        # it would partially set states before returning false
        in_required_pos = False
        for y, row in enumerate(piece.shape):
            for x, num in enumerate(row):
                if num == 0:
                    continue
                
                grid_x = left_grid_x + x
                grid_y = top_grid_y + y

                if valid_squares[grid_y][grid_x] == ValidSquareState.INVALID:
                    return False
                
                if valid_squares[grid_y][grid_x] == ValidSquareState.REQUIRED:
                    in_required_pos = True

        if not in_required_pos:
            return False
        
        for y, row in enumerate(piece.shape):
            for x, num in enumerate(row):
                if num == 0:
                    continue

                grid_x = left_grid_x + x
                grid_y = top_grid_y + y

                self.squares[grid_y][grid_x] = piece_state

        return True
    
    def try_set_state(self, valid_squares, x, y, state):
        valid = self.grid_pos_on_board(x, y) and valid_squares[y][x] != ValidSquareState.INVALID
        if valid:
            valid_squares[y][x] = state

    def piece_on_board(self, piece, snap_left, snap_top):

        # check position is on board
        snap_right = snap_left + (piece.get_width() * SQUARE_SIZE)
        snap_bot = snap_top + (piece.get_height() * SQUARE_SIZE)

        if snap_left < Board.instance.left or \
            snap_right > Board.instance.right \
            or snap_top < Board.instance.top \
            or snap_bot > Board.instance.bot:
            return False
        
        return True


    def screen_to_grid_pos(self, screen_x, screen_y):

        grid_x = int((screen_x - self.left) // SQUARE_SIZE)
        grid_y = int((screen_y - self.top) // SQUARE_SIZE)

        if not self.grid_pos_on_board(grid_x, grid_y):
            return -1, -1

        return grid_x, grid_y
    
    def grid_pos_on_board(self, grid_x, grid_y):
        return grid_x < self.size_in_squares and grid_x >= 0 \
            and grid_y < self.size_in_squares and grid_y >= 0

    def print_state(self):

        state_to_char = {
            BoardSquareState.EMPTY: ' ',
            BoardSquareState.BLUE: 'B',
            BoardSquareState.RED: 'R',
            BoardSquareState.GREEN: 'G',
            BoardSquareState.YELLOW: 'Y'
        }

        for row in self.squares:
            print([state_to_char[state] for state in row])