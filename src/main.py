import pygame

from constants import *
from board import Board
from piece import Piece

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    board = Board()

    shape = [
        [1, 0, 0],
        [1, 1, 0]
    ]
    piece = Piece(shape, SCREEN_CENTER, 'blue')

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False           

        gray_darkness = 100
        screen.fill((gray_darkness, gray_darkness, gray_darkness))

        board.draw(screen)
        piece.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()