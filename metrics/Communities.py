from metrics.Metric import Metric

import pandas as pd
import networkx as nx
import pickle
import os


class Communities(Metric):
    def __init__(self, graph, weighted=False, directed=False, edge_attribute_for_weight='weight'):
        super().__init__(graph, weighted, directed, edge_attribute_for_weight)

    def compute(self, stats, name, pr=True, k=None): # if k is integer, it performs k-clique

        if k:
            if not os.path.exists('pickle/' + name + '_cliques.pickle'):
                communities = nx.algorithms.community.k_clique_communities(self.graph, k)
                with open('pickle/' + name + '_cliques.pickle', 'wb') as output:
                    pickle.dump(communities, output, pickle.HIGHEST_PROTOCOL)

            else:
                with open('pickle/' + name + '_cliques.pickle', 'rb') as cf:
                    communities = pickle.load(cf)
            if pr:
                print("Found", len(communities) , "cliques of minimum size", k)

        else:
            if not os.path.exists('pickle/' + name + '_communities.pickle'):
                communities = nx.algorithms.community.greedy_modularity_communities(self.graph, self.edge_attribute_for_weight)
                with open('pickle/' + name + '_communities.pickle', 'wb') as output:
                    pickle.dump(communities, output, pickle.HIGHEST_PROTOCOL)

            else:
                with open('pickle/' + name + '_communities.pickle', 'rb') as cf:
                    communities = pickle.load(cf)
            if pr:
                print("Found", len(communities), "communities")

        if not os.path.exists(name + '_communities.csv'):
            data = pd.DataFrame()
            for i in range(0, len(communities)):
                data.insert(i, "Community " + str(i), communities[i])
                stats.to_csv(name + '_communities.csv', sep=' ')
        else:
            data = pd.read_csv(name + '_communities.csv')

        self.data = data
        return communities

    def find_node_community(self, node, stats, name, pr=True):

        if self.data is not None:
            pass

        elif os.path.exists(name + '_communities.csv'):
            self.data = pd.read_csv(name + '_communities.csv')

        else:
            self.compute(self, stats, name, pr)

        res = []
        communities = self.data.columns
        for com in communities:
            if len(self.data.where(self.data[com] == node)) > 0:
                res.append(com)

        if pr:
            print("Node", node, "is in the communities:", res)

        return res