from metrics.Metric import Metric
from plots import plots

import matplotlib.pyplot as plt
import networkx as nx
import pickle
import os


class KatzCentrality(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight='weight'):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):

        if not os.path.exists('pickle/' + name + 'katz_centrality.pickle'):
            katz_centrality = nx.katz_centrality(self.graph, alpha=0.1, beta=1.0,
                                                 weight=self.edge_attribute_for_weight)  # FIXME alpha, beta
            with open('pickle/' + name + 'katz_centrality.pickle', 'wb') as output:
                pickle.dump(katz_centrality, output, pickle.HIGHEST_PROTOCOL)

        else:
            with open('pickle/' + name + 'katz_centrality.pickle', 'rb') as dc:
                katz_centrality = pickle.load(dc)

        stats['Katz'] = [v for k, v in katz_centrality.items()]

        # top 20 nodes with highest katz rating
        if pr:
            print(stats.sort_values(by='Katz', ascending=False).head(20))

        # Distribution
        distribution = stats.groupby(['Katz']).size().reset_index(name='Frequency')
        sum = distribution['Frequency'].sum()
        distribution['Probability'] = distribution['Frequency'] / sum

        plots.create_plot("plots/" + name + "_katz_distribution.pdf", "Katz centrality distribution",
                          'Katz', distribution['Katz'],
                          "Probability", distribution['Probability'],
                          xticks=[0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks=[0, 0.001],
                          discrete=False)  # FIXME boundaries
        if pr:
            plt.show()

        return stats
