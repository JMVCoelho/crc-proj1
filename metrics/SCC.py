from metrics.Metric import Metric

import networkx as nx
import pickle
import os


# acho q n faz sentido calcular SCCs aqui: na bipartida cada par <user business> vai ser 1 SCC
# nas projecoes como nao sao directed, o grafo inteiro é 1 SCC
class SCC(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight='weight'):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True):
        scc = None
        if self.directed:

            if not os.path.exists('pickle/' + name + 'scc.pickle'):
                scc = nx.strongly_connected_components(self.graph)
                with open('pickle/' + name + 'scc.pickle', 'wb') as output:
                    pickle.dump(scc, output, pickle.HIGHEST_PROTOCOL)

            else:
                with open('pickle/' + name + 'scc.pickle', 'rb') as sccp:
                    scc = pickle.load(sccp)

            if pr:
                print("It has", len(scc), "strongly connected components")
            for c in scc:
                if pr:
                    print(">>", c)

        return scc