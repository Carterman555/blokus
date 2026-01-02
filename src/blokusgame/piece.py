import pygame
from enum import Enum

from .constants import SMALL_SQUARE_SIZE, SQUARE_SIZE
from . import board
from .helpers import rotate_shape, reflect_shape

class PieceState(Enum):
    OFF_BOARD = 0
    DRAGGING = 1
    ON_BOARD = 2

class PieceAction(Enum):
    START_DRAGGING = 0
    PLACE = 1

class Piece:
    def __init__(self, shape: list[list[int]], topleft: tuple, color: str):
        self.shape: list[list[int]] = shape
        self.top: int = topleft[1]
        self.left: int = topleft[0]

        self.off_board_top = self.top
        self.off_board_left = self.left

        self.rects: list[pygame.Rect] = []

        self.color: str = color

        self.state = PieceState.OFF_BOARD

        self.size = sum([sum(row) for row in shape])

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
        
    def handle_inputs(self, mousebuttondown, mouse_inputs, keydown, keys):

        action = None

        left_click = mousebuttondown and mouse_inputs[0]
        right_click = mousebuttondown and mouse_inputs[2]

        if self.state == PieceState.OFF_BOARD:
            if left_click and self.is_mouse_over():
                self.start_dragging()
                action = PieceAction.START_DRAGGING

        elif self.state == PieceState.DRAGGING:

            if left_click:
                grid_left, grid_right = board.Board.instance.screen_to_grid_pos(*self.snap_pos())
                placed = self.try_place(self.shape, grid_left, grid_right)
                if placed:
                    action = PieceAction.PLACE

            if right_click:
                self.stop_dragging()

            pressed_a = keydown and keys[pygame.K_a]
            pressed_d = keydown and keys[pygame.K_d]
            pressed_s = keydown and keys[pygame.K_s]

            if pressed_a:
                self.rotate(clockwise=False)
            elif pressed_d:
                self.rotate(clockwise=True)
            elif pressed_s:
                self.reflect()


        return action


    def start_dragging(self):
        self.state = PieceState.DRAGGING

        scale_factor = SQUARE_SIZE / SMALL_SQUARE_SIZE

        self.drag_offset_x = (self.left - pygame.mouse.get_pos()[0]) * scale_factor
        self.drag_offset_y = (self.top - pygame.mouse.get_pos()[1]) * scale_factor

    def stop_dragging(self):
        self.state = PieceState.OFF_BOARD

        self.top = self.off_board_top
        self.left = self.off_board_left

    def try_place(self, shape, grid_left, grid_right):
        
        can_place = board.Board.instance.can_place_piece(shape, grid_left, grid_right)
        if can_place:
            self.state = PieceState.ON_BOARD

            self.shape = shape

            screen_left, screen_right = board.Board.instance.grid_to_screen_pos(grid_left, grid_right)
            self.left = screen_left
            self.top = screen_right

            board.Board.instance.place_piece(self, grid_left, grid_right)

        return can_place
    
    def rotate(self, clockwise=True):

        self.shape = rotate_shape(self.shape, clockwise)

        if clockwise:
            new_drag_offset_x = -(self.get_width() * SQUARE_SIZE) - self.drag_offset_y
            self.drag_offset_y = self.drag_offset_x
            self.drag_offset_x = new_drag_offset_x
        else:
            new_drag_offset_x = self.drag_offset_y
            self.drag_offset_y = -(self.get_height() * SQUARE_SIZE) - self.drag_offset_x
            self.drag_offset_x = new_drag_offset_x

    def reflect(self):
        self.shape = reflect_shape(self.shape)
        self.drag_offset_y = -(self.get_height() * SQUARE_SIZE) - self.drag_offset_y

    def snap_pos(self) -> tuple:

        snap_left = board.Board.instance.left - round((board.Board.instance.left - self.left)/SQUARE_SIZE) * SQUARE_SIZE
        snap_top = board.Board.instance.top - round((board.Board.instance.top - self.top)/SQUARE_SIZE) * SQUARE_SIZE
        return (snap_left, snap_top)


    def get_square_count(self):
        count = 0
        for row in self.shape:
            for num in row:
                if num == 1:
                    count += 1
        return count
    
    def get_width(self):
        return len(self.shape[0])
    
    def get_height(self):
        return len(self.shape)
    
    def is_mouse_over(self):
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False
