from metrics.Metric import Metric

import networkx as nx
import pandas as pd
import pickle
import statistics
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

    def community_homogeneity(self, stats, name, community_name, ratings_path_file):
        df = pd.read_csv(ratings_path_file, header=None, usecols=[0, 2], sep=' ')

        def user_mode(user):
            res_df = df[df[0] == user]
            ratings = res_df[2].to_list()
            try:
                mode = statistics.mode(ratings)
            except statistics.StatisticsError: # there is not exactly one most common value
                mode = int(statistics.mean(ratings))
            return mode

        def community_ratings_stdev(_name):
            modes = []
            for _user in self.communities[_name]:
                modes.append(user_mode(_user))
            print("The ratings std deviation of", _name, "is", statistics.pstdev(modes))

        if os.path.exists(name+ '_sorted_communities.pickle'):
            with open(name + '_sorted_communities.pickle', 'rb') as dc:
                self.communities = pickle.load(dc)
        else:
            self.compute(self, stats, name, False)

        if isinstance(community_name, str) and community_name == "all":
            community_names = list(self.communities.keys())
            print("\n\nAll Communities:")
            for _name in community_names:
                community_ratings_stdev(_name)

        else:
            community_ratings_stdev(community_name)


