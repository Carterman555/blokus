import pygame

from constants import *
from board import Board
from piece import Piece
from player import Player, PlayerPosition

class Game:

    def __init__(self):
        self.cur_player_index = 0

    def play(self):

        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        clock = pygame.time.Clock()

        board = Board()

        players = [
            Player(PlayerPosition.TOP_LEFT, 'blue'),
            Player(PlayerPosition.TOP_RIGHT, 'red'),
            Player(PlayerPosition.BOT_LEFT, 'green'),
            Player(PlayerPosition.BOT_RIGHT, 'yellow')
        ]

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    left_click = pygame.mouse.get_pressed()[0]
                    if left_click:
                        placed = players[self.cur_player_index].click()

                        if placed:
                            self.next_turn()


            board.update()

            for player in players:
                player.update()

            gray_darkness = 100
            screen.fill((gray_darkness, gray_darkness, gray_darkness))

            board.draw(screen)

            for player in players:
                player.draw(screen)

            pygame.display.flip()
            dt = clock.tick(60)

        pygame.quit()

    def next_turn(self):
        self.cur_player_index += 1
        self.cur_player_index = self.cur_player_index % 4