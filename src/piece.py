import pygame

from constants import SQUARE_SIZE


class Piece:
    def __init__(self, shape: list[list[int]], topleft: tuple, color: str):
        self.shape: list[list[int]] = shape
        self.top: int = topleft[1]
        self.left: int = topleft[0]

        self.color: str = color

    def draw(self, screen):

        draw_square_size = SQUARE_SIZE - 1

        for i, row in enumerate(self.shape):
            for j, num in enumerate(row):
                if num == 1:
                    square_left = self.left + j*draw_square_size
                    square_top = self.top + i*draw_square_size

                    draw_square_left = square_left + j + 1
                    draw_square_top = square_top + i + 1

                    rect = pygame.Rect(draw_square_left, draw_square_top, draw_square_size, draw_square_size)
                    pygame.draw.rect(screen, self.color, rect)

