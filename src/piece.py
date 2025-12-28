import pygame
from enum import Enum

from constants import SMALL_SQUARE_SIZE, SQUARE_SIZE
from board import Board

class PieceState(Enum):
    OFF_BOARD = 0
    DRAGGING = 1
    ON_BOARD = 2

class Piece:
    def __init__(self, shape: list[list[int]], topleft: tuple, color: str):
        self.shape: list[list[int]] = shape
        self.top: int = topleft[1]
        self.left: int = topleft[0]

        self.rects: list[pygame.Rect] = []

        self.color: str = color

        self.state = PieceState.OFF_BOARD

    def update(self):

        if self.state == PieceState.OFF_BOARD:
            draw_square_size = SMALL_SQUARE_SIZE - 1
        else:
            draw_square_size = SQUARE_SIZE - 1

        self.rects.clear() # might cost lot of memory

        for i, row in enumerate(self.shape):
            for j, num in enumerate(row):
                if num == 1:
                    square_left = self.left + j*draw_square_size
                    square_top = self.top + i*draw_square_size

                    draw_square_left = square_left + j + 1
                    draw_square_top = square_top + i + 1

                    rect = pygame.Rect(draw_square_left, draw_square_top, draw_square_size, draw_square_size)
                    self.rects.append(rect)  # might cost lot of memory


        if self.state == PieceState.DRAGGING:
            self.left = pygame.mouse.get_pos()[0] + self.drag_offset_x
            self.top = pygame.mouse.get_pos()[1] + self.drag_offset_y


    def draw(self, screen):
        for rect in self.rects:
            pygame.draw.rect(screen, self.color, rect)
        
    def click(self):
        if self.state == PieceState.OFF_BOARD and self.is_mouse_over():
            self.state = PieceState.DRAGGING

            scale_factor = SQUARE_SIZE / SMALL_SQUARE_SIZE

            self.drag_offset_x = (self.left - pygame.mouse.get_pos()[0]) * scale_factor
            self.drag_offset_y = (self.top - pygame.mouse.get_pos()[1]) * scale_factor

        elif self.state == PieceState.DRAGGING:

            snap_left, snap_right = self.snap_pos()
            valid_pos = Board.instance.try_place_piece(self, snap_left, snap_right)
            if valid_pos:
                self.state = PieceState.ON_BOARD

                self.left = snap_left
                self.top = snap_right

                return True
        
        return False

    def snap_pos(self) -> tuple:

        snap_left = Board.instance.left - round((Board.instance.left - self.left)/SQUARE_SIZE) * SQUARE_SIZE
        snap_top = Board.instance.top - round((Board.instance.top - self.top)/SQUARE_SIZE) * SQUARE_SIZE
        return (snap_left, snap_top)


    def get_square_count(self):
        count = 0
        for row in self.shape:
            for num in row:
                if num == 1:
                    count += 1
        return count
    
    def get_width(self):
        max_len = 0
        for row in self.shape:
            if len(row) > max_len:
                max_len = len(row)
        return max_len
    
    def get_height(self):
        return len(self.shape)
    
    def is_mouse_over(self):
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False
