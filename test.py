from metrics.EdgesAndNodes import EdgesAndNodes
from metrics.DegreeCentrality import DegreeCentrality
from metrics.SCC import SCC
from metrics.ClusteringCoefficient import ClusteringCoefficient
from metrics.AveragePathLength import AveragePathLength
from metrics.EigenvectorCentrality import EigenvectorCentrality
from metrics.KatzCentrality import KatzCentrality
from metrics.PageRankCentrality import PageRankCentrality

import networkx as nx
import pandas as pd

files = ["data/business-projection.edges", "data/user-projection.edges", "data/bipartite-user-business.edges"]
name = ["business_projection", "user_projection", "user_business_bipartite"]

g = nx.read_edgelist(files[0], delimiter=' ', create_using=nx.Graph)

stats = pd.DataFrame(g.nodes())
stats.columns = ['Node']

# OPTIONAL ARGUMENTS FOR ALL compute(): weighted, directed, edge_attribute_for_weight. Default is false false none.

# 1
nodes, edges = EdgesAndNodes(g).compute(stats=None, name=name[0])

# 2 - Edge weights frequency and distribution
# TODO

# 3
stats = DegreeCentrality(g, n_nodes=nodes).compute(stats=stats, name=name[0])

# 4 - Weighted Degree Centrality
# TODO

# 5
SCC(g).compute(stats=None, name=name[0])

# 6
#stats = ClusteringCoefficient(g).compute(stats=stats, name=name[0])

# 7
#AveragePathLength(g).compute(stats=None, name=name[0])

# 8
stats = EigenvectorCentrality(g).compute(stats=stats, name=name[0])

# 9
stats = KatzCentrality(g).compute(stats=stats, name=name[0])

# 10
stats = PageRankCentrality(g).compute(stats=stats, name=name[0])

output_path = "stats.csv"
stats.to_csv(output_path, sep=' ')
