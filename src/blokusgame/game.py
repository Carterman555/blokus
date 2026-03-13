import pygame
import time
import sys
import neat

from .constants import *
from .board import Board
from .piece import PieceAction
from .player import Player, PlayerPosition

class Game:

    def init_game(self, create_screen=True):
        pygame.init()

        self.cur_player_index = 0

        self.font = pygame.font.Font(None, 48)

        if create_screen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

        self.board = Board()

        self.players = [
            Player(PlayerPosition.TOP_LEFT, 'blue'),
            Player(PlayerPosition.TOP_RIGHT, 'red'),
            Player(PlayerPosition.BOT_RIGHT, 'yellow'),
            Player(PlayerPosition.BOT_LEFT, 'green')
        ]

        self.cur_player = self.players[self.cur_player_index]

        self.board.update_valid_squares(self.cur_player.color)

    def handle_user_inputs(self):
        mousebuttondown = False
        keydown = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown = True

            if event.type == pygame.KEYDOWN:
                keydown = True

        action = self.cur_player.handle_inputs(
            mousebuttondown,
            pygame.mouse.get_pressed(),
            keydown,
            pygame.key.get_pressed()
        )

        if action == PieceAction.PLACE:
            self.on_place()

    def handle_ai_input(self, net):

        board_input = self.board.get_sparse_board()
        output = net.activate(board_input)



        

    def draw(self):

        gray_darkness = 100
        self.screen.fill((gray_darkness, gray_darkness, gray_darkness))

        self.board.draw(self.screen)

        for player in self.players:
            player.draw(self.screen)

        text = self.font.render(f'{self.cur_player.color}\'s turn', True, self.cur_player.color)
        text_rect = text.get_rect()
        padding = 20
        text_rect.center = (SCREEN_CENTER[0], (text_rect.height/2) + padding)

        self.screen.blit(text, text_rect)

        pygame.display.flip()


    def user_play(self):

        self.init_game()

        while True:

            self.handle_user_inputs()

            self.board.update()

            for player in self.players:
                player.update()

            self.draw()
            
            dt = self.clock.tick(60)

    def train_ai(self, genome, config):

        self.init_game(create_screen=False)

        net = neat.nn.FeedForwardNetwork(genome, config)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            self.handle_ai_input()

            self.board.update()

            for player in self.players:
                player.update()

            # self.draw()
            
            dt = self.clock.tick(60)


    def on_place(self):
        self.next_turn()

        turns_skipped = 0
        while not self.cur_player.can_place:

            self.next_turn()

            turns_skipped += 1
            skipped_all_players = turns_skipped >= len(self.players)
            if skipped_all_players:
                self.game_over()
                break


    def next_turn(self):
        self.cur_player_index += 1
        self.cur_player_index = self.cur_player_index % 4
        self.cur_player = self.players[self.cur_player_index]

        self.board.update_valid_squares(self.cur_player.color)

        start = time.process_time()
        if self.cur_player.can_place:
            self.cur_player.can_place = self.board.can_player_place(self.cur_player)

    def game_over(self):
        print('Game Over')
        winners = []
        max_score = 0
        for player in self.players:
            if player.score == max_score:
                winners.append(player.color)
            if player.score > max_score:
                max_score = player.score
                winners = [player.color]


        if len(winners) == 1:
            print(f'The winner is {winners[0]}!')

        elif len(winners) > 1:
            print(f'The winners are {', '.join(winners)}!')
