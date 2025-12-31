import neat
from net_vizualizer import NetVizualizer
import json

class GraphReporter(neat.reporting.BaseReporter):

    def __init__(self, graph, generation_interval, filename_prefix):
        self.graph = graph
        self.generation_interval = generation_interval
        self.filename_prefix = filename_prefix

        self.current_generation = None
        self.last_generation_checkpoint = 0

    def start_generation(self, generation):
        self.current_generation = generation

    def graph_fitness(self, config, pop, best_genome):
        total_fitness = 0

        for genome_id, genome in pop.items():

            total_fitness += genome.fitness
            avg_fitness = total_fitness / config.pop_size
    
        self.graph.addpoint('Avg Fitness', avg_fitness)
        self.graph.addpoint('Best Fitness', best_genome.fitness)

    def save_checkpoint(self, generation):
        filepath = f'{self.filename_prefix}{generation}'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.graph.points, f, ensure_ascii=False, indent=4)


    def post_evaluate(self, config, pop, species_set, best_genome):
        self.graph_fitness(config, pop, best_genome)


        checkpoint_due = False

        # The generation whose population is being saved.
        next_generation = self.current_generation + 1

        if self.generation_interval is not None:
            # Compare the upcoming generation index against the last checkpointed
            # generation index to decide whether a new checkpoint is due.
            dg = next_generation - self.last_generation_checkpoint
            if dg >= self.generation_interval:
                checkpoint_due = True

        if checkpoint_due:
            self.save_checkpoint(next_generation)
            self.last_generation_checkpoint = next_generation



class NetViewer(neat.reporting.BaseReporter):

    def __init__(self, dirpath):
        self.dirpath = dirpath

    def post_evaluate(self, config, pop, species_set, best_genome):
        netviz = NetVizualizer()
        netviz.create_net_image(best_genome, config, self.dirpath)

