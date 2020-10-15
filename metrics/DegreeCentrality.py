from metrics.Metric import Metric
from plots import plots

import matplotlib.pyplot as plt
import networkx as nx
import statistics
import pickle
import os


class DegreeCentrality(Metric):

    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight=None, n_nodes=None):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)
        self.n_nodes = n_nodes

    def compute(self, stats, name, pr=True):

        if not os.path.exists('pickle/' + name + 'degree_centrality.pickle'):
            degree_centrality = nx.degree_centrality(self.graph)
            with open('pickle/' + name + 'degree_centrality.pickle', 'wb') as output:
                pickle.dump(degree_centrality, output, pickle.HIGHEST_PROTOCOL)

        else:
            with open('pickle/' + name + 'degree_centrality.pickle', 'rb') as dc:
                degree_centrality = pickle.load(dc)

        stats['Degree'] = [v for k, v in degree_centrality.items()]

        functions_todo = ['Degree']

        if self.directed:
            in_degree_centrality = nx.in_degree_centrality(self.graph)
            out_degree_centrality = nx.out_degree_centrality(self.graph)
            stats['In-Degree'] = [v for k, v in in_degree_centrality.items()]
            stats['Out-Degree'] = [v for k, v in out_degree_centrality.items()]

            functions_todo = ['Degree', 'In-Degree', 'Out-Degree']

        for function in functions_todo:
            # un-normalize
            stats[function] = round(stats[function] * (self.n_nodes - 1))
            # top 10 nodes with highest degree
            if pr:
                print(stats.sort_values(by=function, ascending=False).head(10))

            # Degree distribution
            distribution = stats.groupby([function]).size().reset_index(name='Frequency')
            sum = distribution['Frequency'].sum()
            distribution['Probability'] = distribution['Frequency'] / sum
            distribution.head(10)

            alpha = plots.create_plot("plots/" + name + "_degree_distribution.pdf", function + " distribution",
                                      function, distribution[function],
                                      "Probability", distribution['Probability'],
                                      yticks=[0, 0.001, 0.002, 0.003, 0.007],
                                      also_log_scale=True, log_yticks=[1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
                                      powerlaw_xmin=1e1, powerlaw_xmax=1e4)
            plt.show()
            if pr:
                print(function + ' distribution gamma= ', alpha)

            # Average Degree, <k>, <k_in>, <k_out>
            average = statistics.mean(stats[function])
            if pr:
                print("Average", function, "=", average)

        return stats
