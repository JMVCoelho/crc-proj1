from metrics.Metric import Metric
from plots import plots

import matplotlib.pyplot as plt
import networkx as nx
import statistics
import pickle
import os


class WeightedDegreeCentrality(Metric):

    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight='weight', n_nodes=None):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)
        self.n_nodes = n_nodes

    def compute(self, stats, name, pr=True):

        if not os.path.exists('pickle/' + name + 'weighted_degree_centrality.pickle'):
            weighted_degree_list = [v for k, v in self.graph.degree(weight=self.edge_attribute_for_weight)]
            with open('pickle/' + name + 'weighted_degree_centrality.pickle', 'wb') as output:
                pickle.dump(weighted_degree_list, output, pickle.HIGHEST_PROTOCOL)

        else:
            with open('pickle/' + name + 'weighted_degree_centrality.pickle', 'rb') as dc:
                weighted_degree_list = pickle.load(dc)

        stats['Weighted Degree'] = weighted_degree_list

        functions_todo = ['Weighted Degree']

        if self.directed:
            if not os.path.exists('pickle/' + name + 'weighted_in_degree_centrality.pickle'):
                weighted_in_degree_list = [v for k, v in self.graph.in_degree(weight=self.edge_attribute_for_weight)]
                with open('pickle/' + name + 'weighted_in_degree_centrality.pickle', 'wb') as output:
                    pickle.dump(weighted_in_degree_list, output, pickle.HIGHEST_PROTOCOL)

            else:
                with open('pickle/' + name + 'weighted_in_degree_centrality.pickle', 'rb') as dc:
                    weighted_in_degree_list = pickle.load(dc)

            if not os.path.exists('pickle/' + name + 'weighted_out_degree_centrality.pickle'):
                weighted_out_degree_list = [v for k, v in self.graph.out_degree(weight=self.edge_attribute_for_weight)]
                with open('pickle/' + name + 'weighted_out_degree_centrality.pickle', 'wb') as output:
                    pickle.dump(weighted_out_degree_list, output, pickle.HIGHEST_PROTOCOL)

            else:
                with open('pickle/' + name + 'weighted_out_degree_centrality.pickle', 'rb') as dc:
                    weighted_out_degree_list = pickle.load(dc)


            stats['Weighted In-Degree'] = weighted_in_degree_list
            stats['Weighted Out-Degree'] = weighted_out_degree_list

            functions_todo = ['Weighted Degree', 'Weighted In-Degree', 'Weighted Out-Degree']

        averages = dict()
        alphas = dict()
        for function in functions_todo:
            # top 10 nodes with highest weighted degree
            if pr:
                print(stats.sort_values(by=function, ascending=False).head(10))

            # Weighted Degree distribution
            distribution = stats.groupby([function]).size().reset_index(name='Frequency')
            sum = distribution['Frequency'].sum()
            distribution['Probability'] = distribution['Frequency'] / sum
            distribution.head(10)

            alpha = plots.create_plot("plots/" + name + "_weighted_" + function + "_distribution.pdf", "",
                                      function, distribution[function],
                                      "Probability", distribution['Probability'],
                                      yticks=[0, 0.001, 0.002, 0.003, 0.005, 0.01],
                                      also_log_scale=True, log_yticks=[1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
                                      powerlaw_xmin=1e1, powerlaw_xmax=1e4)

            if pr:
                plt.show()


            alphas[function] = alpha

            if pr:
                print(function + ' distribution gamma= ', alpha)

            # Average Degree, <k>, <k_in>, <k_out>
            average = statistics.mean(stats[function])
            averages[function] = average
            if pr:
                print("Average", function, "=", average)

        return stats, alphas, averages
