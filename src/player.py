import pygame
from enum import Enum

from constants import *
from piece import Piece

class PlayerPosition(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOT_LEFT = 2
    BOT_RIGHT = 3

class Player:
    def __init__(self, player_pos: PlayerPosition, color):

        self.player_pos = player_pos

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
                [1],
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
                [1],
                [1, 1],
                [1]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
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
                [1]
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
                [1],
                [1, 1],
                [1],
                [1]
            ],
            [
                [0, 1],
                [0, 1],
                [1, 1, 1]
            ],
            [
                [1],
                [1],
                [1, 1, 1]
            ],
            [
                [1, 1],
                [0, 1, 1],
                [0, 0, 1]
            ],
            [
                [1],
                [1, 1, 1],
                [0, 0, 1]
            ],
            [
                [1],
                [1, 1, 1],
                [0, 1]
            ],
            [
                [0, 1],
                [1, 1, 1],
                [0, 1]
            ]
        ]

        grid_positions = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
            (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3)
        ]

        if len(shapes) != len(grid_positions):
            raise Exception(f'Shapes length ({len(shape)}) is not equal to grid positions length ({len(grid_positions)}).')

        padding = 30
        x_spacing = 50
        y_spacing = 60

        pieces_offset = self.get_pieces_offset(grid_positions, padding, x_spacing, y_spacing)

        self.pieces: list[Piece] = []
        for shape, grid_pos in zip(shapes, grid_positions):
            x = grid_pos[0]*x_spacing + pieces_offset[0]
            y = grid_pos[1]*y_spacing + pieces_offset[1]

            self.pieces.append(Piece(shape, (x, y), color))

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

    def click(self):
        for piece in self.pieces:
            piece.click()

        

