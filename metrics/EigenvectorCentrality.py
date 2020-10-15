from metrics.Metric import Metric
from plots import plots

import matplotlib.pyplot as plt
import networkx as nx
import pickle
import os


class EigenvectorCentrality(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight=None):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):

        if not os.path.exists('pickle/' + name + 'eigenvector_centrality.pickle'):
            eigenvector_centrality = nx.eigenvector_centrality(self.graph, weight=self.edge_attribute_for_weight)
            with open('pickle/' + name + 'eigenvector_centrality.pickle', 'wb') as output:
                pickle.dump(eigenvector_centrality, output, pickle.HIGHEST_PROTOCOL)

        else:
            with open('pickle/' + name + 'eigenvector_centrality.pickle', 'rb') as dc:
                eigenvector_centrality = pickle.load(dc)

        stats['Eigenvector'] = [v for k, v in eigenvector_centrality.items()]

        # top 20 nodes with highest eigenvector rating
        print(stats.sort_values(by='Eigenvector', ascending=False).head(20))

        # Distribution
        distribution = stats.groupby(['Eigenvector']).size().reset_index(name='Frequency')
        sum = distribution['Frequency'].sum()
        distribution['Probability'] = distribution['Frequency'] / sum

        # TODO aqui ficava melhor um histograma para ter noção da "classe alta"
        plots.create_plot("plots/" + name + "_eigenvector_distribution.pdf", "Eigenvector centrality distribution",
                          'Eigenvector', distribution['Eigenvector'],
                          "Probability", distribution['Probability'],
                          xticks=[0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks=[0, 0.001], discrete=False)
        plt.show()
        return stats
