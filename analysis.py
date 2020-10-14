import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from plots import plots

# read file
file = "data/business-projection.edges"
g = nx.read_edgelist(file, delimiter=' ', create_using=nx.DiGraph)


# stats for each node
stats = pd.DataFrame(g.nodes())
stats.columns = ['Node']


print("ANALYSIS of", file)
weighted = False
directed = False


# 1. Number of nodes and edges
n_nodes, n_edges = nx.number_of_nodes(g), nx.number_of_edges(g)
print("Number of Nodes:", n_nodes)
print("Number of Edges:", n_edges)


# 2. Edge weights frequency and distribution
if weighted:
    # TODO
    pass


# 3. Degree Centrality
degree_centrality       = nx.degree_centrality(g)
stats['Degree']      = [v for k, v in degree_centrality.items()]
functions_todo = ['Degree']

if directed:
    in_degree_centrality = nx.in_degree_centrality(g)
    out_degree_centrality = nx.out_degree_centrality(g)
    stats['In-Degree']   = [v for k, v in in_degree_centrality.items()]
    stats['Out-Degree']  = [v for k, v in out_degree_centrality.items()]

    functions_todo = ['Degree', 'In-Degree', 'Out-Degree']

for function in functions_todo:
    # un-normalize
    stats[function] = round(stats[function] * (n_nodes-1))
    # top 10 nodes with highest degree
    print(stats.sort_values(by=function, ascending=False).head(10))

    # Degree distribution
    distribution = stats.groupby([function]).size().reset_index(name='Frequency')
    sum = distribution['Frequency'].sum()
    distribution['Probability'] = distribution['Frequency'] / sum
    distribution.head(10)

    alpha = plots.create_plot("plots/degree_distribution.pdf", function + " distribution",
                        function, distribution[function],
                        "Probability", distribution['Probability'],
                        yticks = [0, 0.001, 0.002, 0.003, 0.007],
                        also_log_scale = True, log_yticks = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
                        powerlaw_xmin=1e1, powerlaw_xmax=1e4)
    plt.show()
    print(function + ' distribution alpha= ', alpha)


# 3. Weighted Degree Centrality
if weighted:
    # TODO
    pass



