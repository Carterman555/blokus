import pygame
from enum import Enum

from .constants import *
from .player import Player
from .piece import PieceState
from .helpers import rotate_shape, reflect_shape

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

        self.color_to_state = {
            'blue': BoardSquareState.BLUE,
            'red': BoardSquareState.RED,
            'green': BoardSquareState.GREEN,
            'yellow': BoardSquareState.YELLOW
        }


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


    # try every orientation of every piece for the player
    def can_player_place(self, player: Player):

        required_positions = []
        for y, row in enumerate(self.valid_squares):
            for x, square_state in enumerate(row):
                if square_state == ValidSquareState.REQUIRED:
                    required_positions.append((x, y))

        for piece in player.pieces:
            if piece.state != PieceState.OFF_BOARD:
                continue

            for pos in required_positions:
                shape = piece.shape.copy()
                for _ in range(2):
                    for _ in range(4):
                        for y, row in enumerate(shape):
                            for x, num in enumerate(row):
                                if num == 0:
                                    continue

                                grid_left = pos[0] - x
                                grid_top = pos[1] - y

                                if not self.grid_pos_on_board(grid_left, grid_top):
                                    continue

                                left, top = self.grid_to_screen_pos(grid_left, grid_top)
                                if self.can_place_piece(shape, left, top):
                                    return True
                                
                        shape = rotate_shape(shape)
                    shape = reflect_shape(shape)

        return False


    def place_piece(self, piece, snap_left, snap_top):

        left_grid_x, top_grid_y = self.screen_to_grid_pos(snap_left, snap_top)
        
        for y, row in enumerate(piece.shape):
            for x, num in enumerate(row):
                if num == 0:
                    continue

                grid_x = left_grid_x + x
                grid_y = top_grid_y + y

                piece_state = self.color_to_state[piece.color]
                self.squares[grid_y][grid_x] = piece_state

        return True
    
    def can_place_piece(self, shape, snap_left, snap_top):

        if not self.piece_on_board(shape, snap_left, snap_top):
            return False
        
        left_grid_x, top_grid_y = self.screen_to_grid_pos(snap_left, snap_top)

        # need seperate loops for checking valid pos and setting states because otherwise,
        # it would partially set states before returning false
        in_required_pos = False
        for y, row in enumerate(shape):
            for x, num in enumerate(row):
                if num == 0:
                    continue
                
                grid_x = left_grid_x + x
                grid_y = top_grid_y + y

                if self.valid_squares[grid_y][grid_x] == ValidSquareState.INVALID:
                    return False
                
                if self.valid_squares[grid_y][grid_x] == ValidSquareState.REQUIRED:
                    in_required_pos = True

        if not in_required_pos:
            return False
        
        return True


    def update_valid_squares(self, color):

        def try_set_state(x, y, state):
            valid = self.grid_pos_on_board(x, y) and self.valid_squares[y][x] != ValidSquareState.INVALID
            if valid:
                self.valid_squares[y][x] = state
        
        starting_corners = {
            BoardSquareState.BLUE: (0, 0),
            BoardSquareState.RED: (self.size_in_squares-1, 0),
            BoardSquareState.GREEN: (0, self.size_in_squares-1),
            BoardSquareState.YELLOW: (self.size_in_squares-1, self.size_in_squares-1)
        }

        piece_state = self.color_to_state[color]
        starting_corner = starting_corners[piece_state]

        self.valid_squares = [[ValidSquareState.NEUTRAL] * self.size_in_squares for x in range(self.size_in_squares)]
        self.valid_squares[starting_corner[1]][starting_corner[0]] = ValidSquareState.REQUIRED

        for y in range(self.size_in_squares):
            for x in range(self.size_in_squares):

                # can't place overlapping with another piece
                if self.squares[y][x] != BoardSquareState.EMPTY:
                    self.valid_squares[y][x] = ValidSquareState.INVALID

                if self.squares[y][x] == piece_state:

                    # can't place next to your own piece
                    try_set_state(x-1, y, ValidSquareState.INVALID)
                    try_set_state(x+1, y, ValidSquareState.INVALID)
                    try_set_state(x, y-1, ValidSquareState.INVALID)
                    try_set_state(x, y+1, ValidSquareState.INVALID)

                    # have to place on corner of one of your pieces
                    try_set_state(x-1, y-1, ValidSquareState.REQUIRED)
                    try_set_state(x+1, y-1, ValidSquareState.REQUIRED)
                    try_set_state(x-1, y+1, ValidSquareState.REQUIRED)
                    try_set_state(x+1, y+1, ValidSquareState.REQUIRED)

    def piece_on_board(self, shape, snap_left, snap_top):

        # check position is on board
        width = len(shape[0])
        height = len(shape)

        snap_right = snap_left + (width * SQUARE_SIZE)
        snap_bot = snap_top + (height * SQUARE_SIZE)

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
    
    def grid_to_screen_pos(self, grid_x, grid_y):
        if not self.grid_pos_on_board(grid_x, grid_y):
            raise Exception('Grid pos not on board')
        
        screen_x = (grid_x * SQUARE_SIZE) + self.left
        screen_y = (grid_y * SQUARE_SIZE) + self.top

        return screen_x, screen_y
    
    def grid_pos_on_board(self, grid_x, grid_y):
        return grid_x < self.size_in_squares and grid_x >= 0 \
            and grid_y < self.size_in_squares and grid_y >= 0        

    def get_sparse_board(self, color):

        this = []
        other = []

        state = self.color_to_state[color]

        for row in self.squares:
            for cur_state in row:
                if cur_state == state:
                    this.append(1)
                    other.append(0)
                else:
                    this.append(0)
                    other.append(1)

        return this + other


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