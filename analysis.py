from metrics import *

import networkx as nx
import pandas as pd
import os

file = "data/user-projection.edges"
name = "user_projection"
stats_path = "stats.csv"
print = True


def analysis(path_to_graph, report_name, directed, weighted,
             degreeCentrality = False,
             clusterCoefficient = False,
             apl = False,
             eigenvectorCentrality = False,
             katzCentrality = False,
             pagerankCentrality = False,
             betweennessCentrality = False,
             harmonicCentrality = False,
             scc = False):

    if directed:
        g = nx.read_edgelist(path_to_graph, delimiter=' ', create_using=nx.DiGraph)
    else:
        g = nx.read_edgelist(path_to_graph, delimiter=' ', create_using=nx.Graph)

    nodes, edges = EdgesAndNodes(g).compute(stats=None, name=report_name)

    if not os.path.exists(stats_path):
        stats = pd.DataFrame(g.nodes())
        stats.columns = ['Node']

    else:
        stats = pd.read_csv(stats_path)

    # OPTIONAL ARGUMENTS FOR ALL compute(): weighted, directed, edge_attribute_for_weight. Default is false false none.
    try:
        if degreeCentrality:
            stats = DegreeCentrality(g, weighted=weighted, directed=directed, n_nodes=nodes).compute(stats=stats, name=report_name, pr=print)

        if eigenvectorCentrality:
            stats = EigenvectorCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=print)

        if katzCentrality:
            stats = KatzCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=print)

        if pagerankCentrality:
            stats = PageRankCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=print)

        if betweennessCentrality:
            stats = BetweenessCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=print)

        if harmonicCentrality:
            stats = HarmonicCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=print)

        if clusterCoefficient:
            stats = ClusteringCoefficient(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=print)

        if apl:
            AveragePathLength(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=print)

        if scc:
            SCC(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=print)

    except Exception as e:
        stats.to_csv(stats_path, sep=' ')

    stats.to_csv(stats_path, sep=' ')


def full_analysis(path_to_graph, report_name, directed, weighted):
    analysis(path_to_graph, report_name, directed, weighted,
             True, True, True, True, True, True, True, True, True)


# What do you want to do:

#full_analysis(file, name, False, True)

# OR

analysis(file, name, True, True, degreeCentrality=True)


exit(0)

