from metrics.Metric import Metric
from plots import plots

import matplotlib.pyplot as plt
import networkx as nx
import pickle
import os


class BetweennessCentrality(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight='weight'):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):

        if not os.path.exists('pickle/' + name + 'betweenness_centrality.pickle'):
            betweenness_centrality = nx.betweenness_centrality(self.graph,
                                                 weight=self.edge_attribute_for_weight)
            with open('pickle/' + name + 'betweenness_centrality.pickle', 'wb') as output:
                pickle.dump(betweenness_centrality, output, pickle.HIGHEST_PROTOCOL)

        else:
            with open('pickle/' + name + 'betweenness_centrality.pickle', 'rb') as dc:
                betweenness_centrality = pickle.load(dc)

        stats['Betweenness'] = [v for k, v in betweenness_centrality.items()]

        # top 20 nodes with highest betweenness rating
        if pr:
            print(stats.sort_values(by='Betweenness', ascending=False).head(20))

        # Distribution
        distribution = stats.groupby(['Betweenness']).size().reset_index(name='Frequency')
        sum = distribution['Frequency'].sum()
        distribution['Probability'] = distribution['Frequency'] / sum

        plots.create_plot("plots/" + name + "_betweenness_distribution.pdf", "Betweenness centrality distribution",
                          'Betweenness', distribution['Betweenness'],
                          "Probability", distribution['Probability'],
                          xticks=[0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks=[0, 0.001],
                          discrete=False)  # FIXME boundaries
        plt.show()
        return stats
