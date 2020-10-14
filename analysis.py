import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import statistics

from plots import plots

# read file
file = "data/business-projection.edges"
g = nx.read_edgelist(file, delimiter=' ', create_using=nx.Graph)


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
degree_centrality    = nx.degree_centrality(g)
stats['Degree']      = [v for k, v in degree_centrality.items()]

functions_todo = ['Degree']

if directed:
    in_degree_centrality    = nx.in_degree_centrality(g)
    out_degree_centrality   = nx.out_degree_centrality(g)
    stats['In-Degree']      = [v for k, v in in_degree_centrality.items()]
    stats['Out-Degree']     = [v for k, v in out_degree_centrality.items()]

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

    alpha = plots.create_plot("plots/businessProj_degree_distribution.pdf", function + " distribution",
                        function, distribution[function],
                        "Probability", distribution['Probability'],
                        yticks = [0, 0.001, 0.002, 0.003, 0.007],
                        also_log_scale = True, log_yticks = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
                        powerlaw_xmin=1e1, powerlaw_xmax=1e4)
    plt.show()
    print(function + ' distribution gamma= ', alpha)


# 4. Weighted Degree Centrality
if weighted:
    # TODO
    pass


# 5. Strongly connected components
if directed:
    scc = nx.strongly_connected_components(g)
    print("It has", len(scc), "strongly connected components")
    for c in scc:
        print(">>", c)

# 6. Clustering coefficient
edge_attribute_for_weight = None # it should be a string

clustering_coefficients = nx.clustering(g, weight=edge_attribute_for_weight)
stats['Clustering']     = [v for k, v in clustering_coefficients.items()]

# how many nodes with clustering 1?
max_clustering_nodes = [k for k,v in clustering_coefficients.items() if v == 1.0]
print("Nodes with clustering 1.0:", len(max_clustering_nodes))
print(max_clustering_nodes)

# how many nodes with clustering 0.5?
med_clustering_nodes = [k for k,v in clustering_coefficients.items() if 0.48 < v < 0.52]
print("Nodes with clustering 0.5:", len(med_clustering_nodes))
print(med_clustering_nodes)

# how many nodes with clustering 0?
min_clustering_nodes = [k for k,v in clustering_coefficients.items() if v == 0.0]
print("Nodes with clustering 0.0:", len(min_clustering_nodes))
print(min_clustering_nodes)


# Clustering distribution
distribution = stats.groupby(['Clustering']).size().reset_index(name='Frequency')
sum = distribution['Frequency'].sum()
distribution['Probability'] = distribution['Frequency'] / sum

plots.create_plot("plots/businessProj_clustering_distribution.pdf", "Clustering coefficient distribution",
                  "Clustering coefficient", distribution['Clustering'],
                  "Probability", distribution['Probability'])
plt.show()

# Average Clustering, <C>
average_clustering = statistics.mean(clustering_coefficients.items())
print("Average Clustering Coefficient, <C> =", average_clustering)






output = open("stats.txt", 'w')
print(stats, file=output)
