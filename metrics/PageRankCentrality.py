from metrics.Metric import Metric
from plots import plots

import matplotlib.pyplot as plt
import networkx as nx
import pickle
import os


class PageRankCentrality(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight=None):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):
        if self.directed:

            if not os.path.exists('pickle/' + name + 'pagerank_centrality.pickle'):
                pageRank_centrality = nx.pagerank(self.graph, alpha=0.85, weight=self.edge_attribute_for_weight)
                with open('pickle/' + name + 'pagerank_centrality.pickle', 'wb') as output:
                    pickle.dump(pageRank_centrality, output, pickle.HIGHEST_PROTOCOL)

            else:
                with open('pickle/' + name + 'pagerank_centrality.pickle', 'rb') as dc:
                    pageRank_centrality = pickle.load(dc)

            stats['Page Rank'] = [v for k, v in pageRank_centrality.items()]

            # top 20 nodes with highest page rank
            print(stats.sort_values(by='Page Rank', ascending=False).head(20))

            # Distribution
            distribution = stats.groupby(['Page Rank']).size().reset_index(name='Frequency')
            sum = distribution['Frequency'].sum()
            distribution['Probability'] = distribution['Frequency'] / sum

            plots.create_plot("plots/" + name + "_pageRank_distribution.pdf", "Page Rank distribution",
                              'Page Rank value', distribution['Page Rank'],
                              "Probability", distribution['Probability'],
                              xticks=[0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks=[0, 0.001],
                              discrete=False)  # FIXME boundaries
            plt.show()
            return stats
