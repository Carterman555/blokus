import sys
import signal
import multiprocessing
import neat
import random

from pathlib import Path
import pickle

from graph import Graph
from custom_reporters import *
from blokusgame.game import Game

class Trainer:

    def __init__(self):

        self.max_generations = None # None = unlimited

        self.pop = None

        self.graph = Graph()
        self.graph.setcolor('Avg Fitness', 'lightblue')
        self.graph.setcolor('Best Fitness', 'lightgreen')

        signal.signal(signal.SIGINT, self.on_quit)

    def eval_gemones(self, genomes, config):

        genome_counter = 0
        for genome_id, genome in genomes:

            genome_counter += 1
            print('', end=f'\rGenome {genome_counter}/{config.pop_size}')


            genomes_to_play: list = genomes
            random.shuffle(genomes_to_play)
            while genomes_to_play:
                blue = genome
                red = genomes_to_play.pop()
                green = genomes_to_play.pop()
                yellow = genomes_to_play.pop()

                game = Game()
                game.train_ai
                



    def train_agent(self, config, checkpoint=0, use_multiprocessing=False):

        if config.population % 3 != 0:
            raise Exception('population must be a multiple of 3.')

        checkpoints_path = 'data/checkpoints'

        if checkpoint == 0:
            self.pop = neat.Population(config)
        else:
            self.pop = neat.Checkpointer.restore_checkpoint(f'{checkpoints_path}/neat-checkpoint-{checkpoint}')
            self.graph.restore_checkpoint(f'{checkpoints_path}/graph-checkpoint-{checkpoint}')

        self.pop.add_reporter(neat.StdOutReporter(True))
        self.pop.add_reporter(neat.Checkpointer(5, filename_prefix=f'{checkpoints_path}/neat-checkpoint-'))
        self.pop.add_reporter(GraphReporter(self.graph, 5, filename_prefix=f'{checkpoints_path}/graph-checkpoint-'))

        root_path = Path(__file__).parent.parent
        self.pop.add_reporter(NetViewer(root_path / 'data'))

        if use_multiprocessing:
            global evaluator
            evaluator = neat.ParallelEvaluator(
                multiprocessing.cpu_count(),
                self.eval_genome,
                initializer=self.init_worker,
            )
            best = self.pop.run(evaluator.evaluate, self.max_generations)
            evaluator.close()
        else:
            best = self.pop.run(self.eval_genomes, self.max_generations)

        # to make graph stay after training
        self.graph.stay()

        with open('data/best-ai.pickle', 'wb') as f:
            pickle.dump(best, f)


    def on_quit(self, sig, frame):

        if evaluator and evaluator.pool:
            evaluator.pool.terminate()

        if self.pop:
            print("\nInterupted: Saving best genome")
            with open('data/best-ai.pickle', 'wb') as f:
                pickle.dump(self.pop.best_genome, f)
        else:
            print('\nInterupted')

        sys.exit(0)

    def quit_worker(self, sig, frame):
        sys.exit(0)

    def init_worker(self):
        signal.signal(signal.SIGINT, self.quit_worker)