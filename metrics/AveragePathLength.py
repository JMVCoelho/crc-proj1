from metrics.Metric import Metric

import networkx as nx
import pickle
import os


class AveragePathLength(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight='weight'):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):

        if not os.path.exists('pickle/' + name + '_average_path_length.pickle'):
            average_shortest_path_length = nx.average_shortest_path_length(self.graph,
                                                                           weight=self.edge_attribute_for_weight)

            with open('pickle/' + name + '_average_path_length.pickle', 'wb') as output:
                pickle.dump(average_shortest_path_length, output, pickle.HIGHEST_PROTOCOL)

        else:
            with open('pickle/' + name + '_average_path_length.pickle', 'rb') as dc:
                average_shortest_path_length = pickle.load(dc)

        if pr:
            print("Average Shortest Path Length, <L> =", average_shortest_path_length)

        return average_shortest_path_length
