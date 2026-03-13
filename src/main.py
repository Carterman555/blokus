import sys
import argparse

from blokusgame.game import Game
from trainer import Trainer

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Blokus')

    subparser = parser.add_subparsers(dest='command')

    # train_parser = subparser.add_parser('train', help='Train the ai agent')
    # train_parser.add_argument('-m', '--multiprocessing', action='store_true', help='use multiprocessing when training agents to speed up training')
    # train_parser.add_argument('-c', '--checkpoint', default=0, help='train the ai from a given checkpoint')

    # aiplay_parser = subparser.add_parser('aiplay', help='Watch the best agent play')

    userplay_parser = subparser.add_parser('userplay', help='Allow user to play blokus')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # if args.command == 'train':
    #     trainer = Trainer()
    #     trainer.train_agent()

    # elif args.command == 'aiplay':
    #     pass

    elif args.command == 'userplay':
        game = Game()
        game.user_play()