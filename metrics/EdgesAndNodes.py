from metrics.Metric import Metric

import networkx as nx


class EdgesAndNodes(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight=None):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):
        n_nodes, n_edges = nx.number_of_nodes(self.graph), nx.number_of_edges(self.graph)

        if pr:
            print("Number of Nodes:", n_nodes)
            print("Number of Edges:", n_edges)

        return n_nodes, n_edges
