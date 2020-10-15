from metrics.Metric import Metric
from plots import plots

import matplotlib.pyplot as plt
import networkx as nx
import pickle
import os


class HarmonicCentrality(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight='weight'):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):

        if not os.path.exists('pickle/' + name + 'harmonic_centrality.pickle'):
            harmonic_centrality = nx.harmonic_centrality(self.graph)
            with open('pickle/' + name + 'harmonic_centrality.pickle', 'wb') as output:
                pickle.dump(harmonic_centrality, output, pickle.HIGHEST_PROTOCOL)

        else:
            with open('pickle/' + name + 'harmonic_centrality.pickle', 'rb') as dc:
                harmonic_centrality = pickle.load(dc)

        stats['Harmonic'] = [v for k, v in harmonic_centrality.items()]

        # top 20 nodes with highest harmonic rating
        if pr:
            print(stats.sort_values(by='Harmonic', ascending=False).head(20))

        # Distribution
        distribution = stats.groupby(['Harmonic']).size().reset_index(name='Frequency')
        sum = distribution['Frequency'].sum()
        distribution['Probability'] = distribution['Frequency'] / sum

        plots.create_plot("plots/" + name + "_harmonic_distribution.pdf", "Harmonic centrality distribution",
                          'Harmonic', distribution['Harmonic'],
                          "Probability", distribution['Probability'],
                          xticks=[0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks=[0, 0.001],
                          discrete=False)  # FIXME boundaries
        plt.show()
        return stats
