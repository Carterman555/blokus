import pygame
from enum import Enum

from constants import *
from piece import Piece, PieceAction

class PlayerPosition(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOT_LEFT = 2
    BOT_RIGHT = 3

class Player:
    def __init__(self, player_pos: PlayerPosition, color):

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

        self.text = self.font.render(str(self.score), True, self.color)
        screen.blit(self.text, text_positions[self.player_pos])

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

        

