import os
import sys
import neat
import argparse

from blokusgame.game import Game

if __name__ == '__main__':

    src_path = os.path.dirname(__file__)
    config_path = os.path.join(src_path, 'config')
    config = neat.Config(
        genome_type=neat.DefaultGenome,
        reproduction_type=neat.DefaultReproduction,
        species_set_type=neat.DefaultSpeciesSet,
        stagnation_type=neat.DefaultStagnation,
        filename=config_path
    )

    parser = argparse.ArgumentParser(description='Blokus AI')

    subparser = parser.add_subparsers(dest='command')

    train_parser = subparser.add_parser('train', help='Train the ai agent')
    train_parser.add_argument('-m', '--multiprocessing', action='store_true', help='use multiprocessing when training agents to speed up training')
    train_parser.add_argument('-c', '--checkpoint', default=0, help='train the ai from a given checkpoint')

    aiplay_parser = subparser.add_parser('aiplay', help='Watch the best agent play')

    userplay_parser = subparser.add_parser('userplay', help='Allow user to play blokus')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'train':
        pass

    elif args.command == 'aiplay':
        pass

    elif args.command == 'userplay':
        game = Game()
        game.user_play()