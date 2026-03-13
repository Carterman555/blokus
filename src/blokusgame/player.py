import pygame
from enum import Enum
import math

from .constants import *
from .piece import Piece, PieceAction, PieceState
from .helpers import rotate_shape, reflect_shape

class PlayerPosition(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOT_LEFT = 2
    BOT_RIGHT = 3

class Player:
    def __init__(self, player_pos:PlayerPosition, color, net=None):

        self.player_pos = player_pos
        self.color = color

        shapes = [
            [
                [1]
            ],
            [
                [1],
                [1]
            ],
            [
                [1],
                [1],
                [1]
            ],
            [
                [1, 0],
                [1, 1]
            ],
            [
                [1],
                [1],
                [1],
                [1]
            ],
            [
                [0, 1],
                [0, 1],
                [1, 1]
            ],
            [
                [1, 0],
                [1, 1],
                [1, 0]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1, 0],
                [0, 1, 1]
            ],
            [
                [1],
                [1],
                [1],
                [1],
                [1]
            ],
            [
                [0, 1],
                [0, 1],
                [0, 1],
                [1, 1]
            ],
            [
                [0, 1],
                [0, 1],
                [1, 1],
                [1, 0]
            ],
            [
                [0, 1],
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [0, 1],
                [1, 1]
            ],
            [
                [1, 0],
                [1, 1],
                [1, 0],
                [1, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 1]
            ],
            [
                [1, 0, 0],
                [1, 0, 0],
                [1, 1, 1]
            ],
            [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 1]
            ],
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 1]
            ],
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ]
        ]

        off_board_positions = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
            (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3)
        ]

        if len(shapes) != len(off_board_positions):
            raise Exception(f'Shapes length ({len(shape)}) is not equal to grid positions length ({len(off_board_positions)}).')

        padding = 30
        x_spacing = 50
        y_spacing = 60

        pieces_offset = self.get_pieces_offset(off_board_positions, padding, x_spacing, y_spacing)

        self.pieces: list[Piece] = []
        for shape, grid_pos in zip(shapes, off_board_positions):
            x = grid_pos[0]*x_spacing + pieces_offset[0]
            y = grid_pos[1]*y_spacing + pieces_offset[1]

            self.pieces.append(Piece(shape, (x, y), self.color))

        self.score = 0

        self.font = pygame.font.Font(None, 48)

        self.can_place = True

        self.net = net

    def get_pieces_offset(self, grid_positions, padding, x_spacing, y_spacing):

        max_grid_x = max([x for x, y in grid_positions])
        last_piece_width = SMALL_SQUARE_SIZE*3
        pieces_width = (x_spacing*max_grid_x) + last_piece_width

        right_x_offset = SCREEN_WIDTH - (pieces_width + padding)

        max_grid_y = max([y for x, y in grid_positions])
        last_piece_height = SMALL_SQUARE_SIZE*3
        pieces_height = (y_spacing*max_grid_y) + last_piece_height

        bot_y_offset = SCREEN_HEIGHT - (pieces_height + padding)

        if self.player_pos == PlayerPosition.TOP_LEFT:
            return (padding, padding)
        elif self.player_pos == PlayerPosition.TOP_RIGHT:
            return (right_x_offset, padding)
        elif self.player_pos == PlayerPosition.BOT_LEFT:
            return (padding, bot_y_offset)
        elif self.player_pos == PlayerPosition.BOT_RIGHT:
            return (right_x_offset, bot_y_offset)


    def update(self):
        for piece in self.pieces:
            piece.update()

    def draw(self, screen):
        for piece in self.pieces:
            piece.draw(screen)

        text_positions = {
            PlayerPosition.TOP_LEFT: (30, 260),
            PlayerPosition.TOP_RIGHT: (968, 260),
            PlayerPosition.BOT_LEFT: (30, 430),
            PlayerPosition.BOT_RIGHT: (968, 430)
        }

        text = self.font.render(str(self.score), True, self.color)
        screen.blit(text, text_positions[self.player_pos])

    def handle_inputs(self, mousebuttondown, mouse_inputs, keydown, keys):

        action = None
        placed_piece_size = 0

        for piece in self.pieces:
            cur_action = piece.handle_inputs(mousebuttondown, mouse_inputs, keydown, keys)
            if cur_action != None:
                action = cur_action
                placed_piece_size = piece.size

        if action == PieceAction.PLACE:
            self.score += placed_piece_size

        return action
    
    def handle_ai_input(self, board):

        if not board.can_player_place(self):
            raise Exception(f'{self.color} player cannot place.')
        
        board_input = board.get_sparse_board(self.color)
        output = self.net.activate(board_input)

        piece_output = output[0:21]
        rotation_output = output[21:25]
        reflection_output = output[25:27]

        grid_x_output = output[27 : 27+board.size_in_squares]
        grid_y_output = output[27+board.size_in_squares : 27 + (board.size_in_squares*2)]

        def sort_indices(l):
            return sorted(
                range(len(l)),
                key=lambda i: l[i],
                reverse=True
            )

        grid_x_sorted = sort_indices(grid_x_output)
        grid_y_sorted = sort_indices(grid_y_output)
        piece_indices = sort_indices(piece_output)
        rotation_amounts = sort_indices(rotation_output)
        reflect_amounts = sort_indices(reflection_output)
        
        piece: Piece = None
        for idx in piece_indices:
            if self.pieces[idx].state != PieceState.OFF_BOARD:
                continue

            piece = self.pieces[idx]

            for grid_left in grid_x_sorted:
                for grid_top in grid_y_sorted:
                    for rotation_amount in rotation_amounts:
                        for reflect_amount in reflect_amounts:
                            
                            shape = piece.shape
                            for _ in range(rotation_amount):
                                shape = rotate_shape(shape)

                            if reflect_amount == 1: # reflect_amount is either 0 or 1
                                shape = reflect_shape(shape)

                            placed = piece.try_place(shape, grid_left, grid_top)

                            if placed:
                                self.score += piece.get_square_count()
                                return True

        return False
    
            