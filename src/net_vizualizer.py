import neat
from pathlib import Path
import graphviz

class NetVizualizer:
    def create_net_image(self, genome, config, dirpath):

        dirpath = Path(dirpath)

        d = graphviz.Digraph(comment='Neural Net')
        d.format = 'svg'

        d.attr(rankdir='LR')
        d.attr(ranksep='5', nodesep='0.3')
        d.attr(overlap='scale')
        d.attr(splines='line')
        d.attr(outputorder='edgesfirst')

        d.attr(
            'node',
            shape='circle',
            fixedsize='true',
            width='0.7',
            style='filled',
            fillcolor='lightgray',
            label=''
        )

        d.attr('edge', arrowsize='0.25')

        fillcolors = {
            'input': 'orange',
            'hidden': 'lightgray',
            'output': 'lightblue'
        }

        net = neat.nn.RecurrentNetwork.create(genome, config)

        # Create subgraphs for input and output nodes to enforce same rank
        with d.subgraph() as s:
            s.attr(rank='same')
            for key in net.input_nodes:
                s.node(str(key), fillcolor=fillcolors['input'])

        for node_eval in net.node_evals:
            key = node_eval[0]
            is_hidden = key not in net.input_nodes and key not in net.output_nodes
            if is_hidden:
                d.node(str(key), fillcolor=fillcolors['hidden'])

        # Create subgraph for output nodes
        with d.subgraph() as s:
            s.attr(rank='same')
            for key in net.output_nodes:
                s.node(str(key), fillcolor=fillcolors['output'])

        for gene_pair, connection in genome.connections.items():
            color = 'black'
            if not connection.enabled:
                color = 'lightgray'

            d.edge(str(gene_pair[0]), str(gene_pair[1]), color=color)

        d.render(filename=str(dirpath / 'netviz'), engine='dot')

    



        

