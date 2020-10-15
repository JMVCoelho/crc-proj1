from metrics.Metric import Metric
from plots import plots

import matplotlib.pyplot as plt
import networkx as nx
import statistics
import pickle
import os


class ClusteringCoefficient(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight='weight'):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):

        if not os.path.exists('pickle/' + name + '_clustering_coefficient.pickle'):
            clustering_coefficients = nx.clustering(self.graph, weight=self.edge_attribute_for_weight)
            with open('pickle/' + name + '_clustering_coefficient.pickle', 'wb') as output:
                pickle.dump(clustering_coefficients, output, pickle.HIGHEST_PROTOCOL)

        else:
            with open('pickle/' + name + '_clustering_coefficient.pickle', 'rb') as cf:
                clustering_coefficients = pickle.load(cf)

        stats['Clustering'] = [v for k, v in clustering_coefficients.items()]

        # how many nodes with clustering 1?
        max_clustering_nodes = [k for k, v in clustering_coefficients.items() if v == 1.0]
        if pr:
            print("Nodes with clustering 1.0:", len(max_clustering_nodes))
            print(max_clustering_nodes)

        # how many nodes with clustering 0.5?
        med_clustering_nodes = [k for k, v in clustering_coefficients.items() if 0.48 < v < 0.52]
        if pr:
            print("Nodes with clustering 0.5:", len(med_clustering_nodes))
            print(med_clustering_nodes)

        # how many nodes with clustering 0?
        min_clustering_nodes = [k for k, v in clustering_coefficients.items() if v == 0.0]
        if pr:
            print("Nodes with clustering 0.0:", len(min_clustering_nodes))
            print(min_clustering_nodes)

        # Clustering distribution
        distribution = stats.groupby(['Clustering']).size().reset_index(name='Frequency')
        sum = distribution['Frequency'].sum()
        distribution['Probability'] = distribution['Frequency'] / sum

        plots.create_plot("plots/" + name + "_clustering_distribution.pdf", "Clustering coefficient distribution",
                          "Clustering coefficient", distribution['Clustering'],
                          "Probability", distribution['Probability'])
        #plt.show()

        # Average Clustering, <C>
        coefs = []
        for pair in clustering_coefficients.items():
            coefs.append(pair[1])
        average_clustering = statistics.mean(coefs)
        if pr:
            print("Average Clustering Coefficient, <C> =", average_clustering)

        return stats, average_clustering
