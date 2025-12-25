import pygame
from constants import *

class Board:

    instance = None

    def __init__(self):
        self.squares = 20
        self.size = self.squares*SQUARE_SIZE

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

        for i in range(1, self.squares):
            x = self.left + SQUARE_SIZE*i
            pygame.draw.line(screen, line_color, (x, self.top), (x, self.bot-1))

        for i in range(1, self.squares):
            y = self.top + SQUARE_SIZE*i
            pygame.draw.line(screen, line_color, (self.left, y), (self.right-1, y))
