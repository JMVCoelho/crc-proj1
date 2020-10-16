from metrics.EdgesAndNodes import EdgesAndNodes
from metrics.DegreeCentrality import DegreeCentrality
from metrics.SCC import SCC
from metrics.ClusteringCoefficient import ClusteringCoefficient
from metrics.AveragePathLength import AveragePathLength
from metrics.EigenvectorCentrality import EigenvectorCentrality
from metrics.KatzCentrality import KatzCentrality
from metrics.PageRankCentrality import PageRankCentrality
from metrics.BetweenessCentrality import BetweennessCentrality
from metrics.HarmonicCentrality import HarmonicCentrality


import networkx as nx
import pandas as pd
import os

file = "data/user-projection.edges"
name = "user_projection_"
stats_path = "stats.csv"
_print = True


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

    print("\nReading...\n")
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
            print("\nDegree Centrality...\n")
            res = DegreeCentrality(g, weighted=weighted, directed=directed, n_nodes=nodes).compute(stats=stats, name=report_name, pr=_print)
            stats = res[0]
            stats.to_csv(stats_path, sep=' ')
        if eigenvectorCentrality:
            print("\nEigenvector Centrality...\n")
            stats = EigenvectorCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=_print)
            stats.to_csv(stats_path, sep=' ')
        if katzCentrality:
            print("\nKatze Centrality...\n")
            stats = KatzCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=_print)
            stats.to_csv(stats_path, sep=' ')
        if pagerankCentrality:
            print("\nPR Centrality...\n")
            stats = PageRankCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=_print)
            stats.to_csv(stats_path, sep=' ')
        if betweennessCentrality:
            print("\nBetweenness Centrality...\n")
            stats = BetweennessCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=_print)
            stats.to_csv(stats_path, sep=' ')
        if harmonicCentrality:
            print("\nHarmonic Centrality...\n")
            stats = HarmonicCentrality(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=_print)
            stats.to_csv(stats_path, sep=' ')
        if clusterCoefficient:
            print("\nClustering...\n")
            res = ClusteringCoefficient(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=_print)
            stats = res[0]
            stats.to_csv(stats_path, sep=' ')
        if apl:
            print("\nAPL...\n")
            AveragePathLength(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=_print)

        if scc:
            print("\nSCC...\n")
            SCC(g, weighted=weighted, directed=directed).compute(stats=stats, name=report_name, pr=_print)

    except Exception as e:
        if stats:
            stats.to_csv(stats_path, sep=' ')
        print(e)

    if stats:
        stats.to_csv(stats_path, sep=' ')


def full_analysis(path_to_graph, report_name, directed, weighted):
    analysis(path_to_graph, report_name, directed, weighted,
             True, True, True, True, True, True, True, True, True)


# What do you want to do:

#full_analysis(file, name, False, True)

# OR

analysis(file, name, weighted=True, directed=False, 
            degreeCentrality = False,
             clusterCoefficient = False,
             apl = False,
             eigenvectorCentrality = False,
             katzCentrality = False,
             pagerankCentrality = False,
             betweennessCentrality = True,
             harmonicCentrality = True,
             scc = False
         )


exit(0)

