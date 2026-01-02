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

        self.game_over = False

        

    def handle_user_inputs(self):
        mousebuttondown = False
        keydown = False

        for event in pygame.event.get():

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

        self.players = [
            Player(PlayerPosition.TOP_LEFT, 'blue'),
            Player(PlayerPosition.TOP_RIGHT, 'red'),
            Player(PlayerPosition.BOT_RIGHT, 'yellow'),
            Player(PlayerPosition.BOT_LEFT, 'green')
        ]

        self.cur_player = self.players[self.cur_player_index]

        self.board.update_valid_squares(self.cur_player.color)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            if not self.game_over:
                self.handle_user_inputs()

            for player in self.players:
                player.update()

            self.draw()
            
            dt = self.clock.tick(60)

    def train_ai(self, blue_genome, red_genome, green_genome, yellow_genome, config):

        self.init_game(create_screen=True)

        blue_net = neat.nn.FeedForwardNetwork.create(blue_genome, config)
        red_net = neat.nn.FeedForwardNetwork.create(red_genome, config)
        yellow_net = neat.nn.FeedForwardNetwork.create(green_genome, config)
        green_net = neat.nn.FeedForwardNetwork.create(yellow_genome, config)

        self.players = [
            Player(PlayerPosition.TOP_LEFT, 'blue', blue_net),
            Player(PlayerPosition.TOP_RIGHT, 'red', red_net),
            Player(PlayerPosition.BOT_RIGHT, 'yellow', yellow_net),
            Player(PlayerPosition.BOT_LEFT, 'green', green_net)
        ]

        self.cur_player = self.players[self.cur_player_index]

        self.board.update_valid_squares(self.cur_player.color)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            self.cur_player.handle_ai_input(self.board)
            self.on_place()

            if self.game_over:
                blue_genome.fitness = self.players[0].score
                red_genome.fitness = self.players[1].score
                yellow_genome.fitness = self.players[2].score
                green_genome.fitness = self.players[3].score
                break

            for player in self.players:
                player.update()

            self.draw()
            
            dt = self.clock.tick(-1)


    def on_place(self):
        self.next_turn()

        turns_skipped = 0
        while not self.cur_player.can_place:

            self.next_turn()

            turns_skipped += 1
            skipped_all_players = turns_skipped >= len(self.players)
            if skipped_all_players:
                self.on_game_over()
                break


    def next_turn(self):
        self.cur_player_index += 1
        self.cur_player_index = self.cur_player_index % 4
        self.cur_player = self.players[self.cur_player_index]

        self.board.update_valid_squares(self.cur_player.color)

        if self.cur_player.can_place:
            self.cur_player.can_place = self.board.can_player_place(self.cur_player)

    def on_game_over(self):
        self.game_over = True

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
