import matplotlib.pyplot as plt
import json

class Graph:
    
    def __init__(self):

        self.points: dict[str, list[float]] = dict()
        self.colors: dict[str, str] = dict()

        plt.ion()

        plt.style.use('dark_background')

    def setcolor(self, label: str, color: str):
        self.colors[label] = color

    def addpoint(self, label: str, value: float):

        if label in self.points:
            self.points[label].append(value)
        else:
            self.points[label] = [value]

        plt.cla()

        for cur_label, cur_points in self.points.items():
            plt.plot(cur_points, color=self.colors[cur_label], label=cur_label)

        plt.title('Asteroids AI')
        plt.xlabel('Generation Number')
        plt.ylabel('Fitness')
        plt.legend()

        plt.tight_layout()

        plt.pause(0.1)
        plt.show(block=False)

    def stay(self):
        plt.show(block=True)

    def restore_checkpoint(self, filepath):
        with open(filepath, 'r') as f:
            self.points = json.load(f)