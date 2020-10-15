from abc import ABC, abstractmethod


class Metric(ABC):

    def __init__(self, graph, weighted, directed, edge_attribute_for_weight=None):
        super().__init__()
        self.graph = graph
        self.weighted = weighted
        self.directed = directed
        self.edge_attribute_for_weight = edge_attribute_for_weight

    @abstractmethod
    def compute(self, stats, name, pr):
        pass

