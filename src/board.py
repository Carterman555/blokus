import pygame
from constants import *
from enum import Enum

class BoardSquareState(Enum):
    EMPTY = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4

class Board:

    instance = None

    def __init__(self):
        self.size_in_squares = 20
        self.size = self.size_in_squares*SQUARE_SIZE

        self.squares = [[BoardSquareState.EMPTY] * self.size_in_squares for x in range(self.size_in_squares)]

        Board.instance = self

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

        # check position is on board
        snap_right = snap_left + (piece.get_width() * SQUARE_SIZE)
        snap_bot = snap_top + (piece.get_height() * SQUARE_SIZE)

        if snap_left < Board.instance.left or \
            snap_right > Board.instance.right \
            or snap_top < Board.instance.top \
            or snap_bot > Board.instance.bot:
            return False

        left_grid_x, top_grid_y = self.screen_to_grid_pos(snap_left, snap_top)

        if left_grid_x == -1:
            raise Exception(f'Trying to place piece off board: pos ({snap_left}, {snap_top})')
        
        # need seperate loops for checking valid pos and setting states because otherwise,
        # it would partially set states before returning false
        for y, row in enumerate(piece.shape):
            for x, num in enumerate(row):
                if num == 0:
                    continue
                
                grid_x = left_grid_x + x
                grid_y = top_grid_y + y

                if self.squares[grid_y][grid_x] != BoardSquareState.EMPTY:
                    return False

        color_to_state = {
            'blue': BoardSquareState.BLUE,
            'red': BoardSquareState.RED,
            'green': BoardSquareState.GREEN,
            'yellow': BoardSquareState.YELLOW
        }

        for y, row in enumerate(piece.shape):
            for x, num in enumerate(row):
                if num == 0:
                    continue

                grid_x = left_grid_x + x
                grid_y = top_grid_y + y

                state = color_to_state[piece.color]
                self.squares[grid_y][grid_x] = state

        return True


    def screen_to_grid_pos(self, screen_x, screen_y):

        grid_x = int((screen_x - self.left) // SQUARE_SIZE)
        grid_y = int((screen_y - self.top) // SQUARE_SIZE)

        if grid_x >= self.size_in_squares or grid_x < 0 \
            or grid_y >= self.size_in_squares or grid_y < 0:
            return -1, -1

        return grid_x, grid_y
    
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