from metrics.Metric import Metric

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

        if not os.path.exists(name + '_sorted_communities.pickle'):
            # undo frozen sets and do community names
            sorted_communities = dict()
            for i in range(0, len(communities)):
                sorted_communities["Community " + str(i + 1)] = list(communities[i])

            # save
            with open(name + '_sorted_communities.pickle', 'wb') as output:
                pickle.dump(sorted_communities, output, pickle.HIGHEST_PROTOCOL)
        else:
            with open(name + '_sorted_communities.pickle', 'rb') as dc:
                sorted_communities = pickle.load(dc)

        self.communities = sorted_communities
        return sorted_communities

    def find_node_community(self, node, stats, name, pr=True):
        if os.path.exists(name + '_sorted_communities.pickle'):
            with open(name + '_sorted_communities.pickle', 'rb') as dc:
                self.communities = pickle.load(dc)
        else:
            self.compute(self, stats, name, pr)

        res = []

        community_names = list(self.communities.keys())
        community_users = list(self.communities.values())

        for community in community_users:
            if node in community:
                res.append(community_names[community_users.index(community)])

        if pr:
            print("Node", node, "is in the communities:", res)

        return res

    def community_sizes(self, stats, name, top=10, pr=True):
        if os.path.exists(name + '_sorted_communities.pickle'):
            with open(name + '_sorted_communities.pickle', 'rb') as dc:
                self.communities = pickle.load(dc)
        else:
            self.compute(self, stats, name, pr)

        community_names = list(self.communities.keys())

        if isinstance(top, str) and top == "all":
            print("\n\nAll Communities:")
            for name in community_names:
                print(name, len(self.communities[name]))

        if isinstance(top, int):
            print("\n\nBigger Communities:")
            for i in range(0, top):
                name = community_names[i]
                print(name, len(self.communities[name]))