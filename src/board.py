import pygame
from constants import *

class Board:

    def __init__(self):
        self.squares = 20
        self.size = self.squares*SQUARE_SIZE

    def draw(self, screen):

        top = SCREEN_CENTER[1] - self.size/2
        bot = SCREEN_CENTER[1] + self.size/2
        left = SCREEN_CENTER[0] - self.size/2
        right = SCREEN_CENTER[0] + self.size/2

        rect = pygame.Rect(left, top, self.size, self.size)

        pygame.draw.rect(screen,'darkgray', rect)

        line_color = (230, 230, 230)

        square_size = self.size / self.squares
        for i in range(1, self.squares):
            x = left + square_size*i
            pygame.draw.line(screen, line_color, (x, top), (x, bot-1))

        for i in range(1, self.squares):
            y = top + square_size*i
            pygame.draw.line(screen, line_color, (left, y), (right-1, y))