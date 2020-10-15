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

    # Average Degree, <k>, <k_in>, <k_out>
    average = statistics.mean(stats[function])
    print("Average", function, "=", average)


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



# 7. Average Path Length
edge_attribute_for_weight = None # it should be a string

average_shortest_path_length = nx.average_shortest_path_length(g, weight=edge_attribute_for_weight)
print("Average Shortest Path Length, <L> =", average_shortest_path_length)


# 8. Eigenvector Centrality
edge_attribute_for_weight = None # it should be a string

eigenvector_centrality  = nx.eigenvector_centrality(g, weight=edge_attribute_for_weight)
stats['Eigenvector']    = [v for k, v in eigenvector_centrality.items()]

# top 20 nodes with highest eigenvector rating
print(stats.sort_values(by='Eigenvector', ascending=False).head(20))

# Distribution
distribution = stats.groupby(['Eigenvector']).size().reset_index(name='Frequency')
sum = distribution['Frequency'].sum()
distribution['Probability'] = distribution['Frequency'] / sum

# TODO aqui ficava melhor um histograma para ter noção da "classe alta"
plots.create_plot("plots/businessProj_eigenvector_distribution.pdf", "Eigenvector centrality distribution",
                  'Eigenvector', distribution['Eigenvector'],
                   "Probability", distribution['Probability'],
                  xticks = [0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks = [0, 0.001], discrete=False)
plt.show()


# 9. Katz Centrality
edge_attribute_for_weight = None # it should be a string

katz_centrality  = nx.katz_centrality(g, alpha=0.1, beta=1.0, weight=edge_attribute_for_weight) # FIXME alpha, beta
stats['Katz']    = [v for k, v in katz_centrality.items()]

# top 20 nodes with highest katz rating
print(stats.sort_values(by='Katz', ascending=False).head(20))

# Distribution
distribution = stats.groupby(['Katz']).size().reset_index(name='Frequency')
sum = distribution['Frequency'].sum()
distribution['Probability'] = distribution['Frequency'] / sum

plots.create_plot("plots/businessProj_katz_distribution.pdf", "Katz centrality distribution",
                  'Katz', distribution['Katz'],
                   "Probability", distribution['Probability'],
                  xticks = [0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks = [0, 0.001], discrete=False) # FIXME boundaries
plt.show()


# 10. Page Rank
edge_attribute_for_weight = None # it should be a string

if directed:
    pageRank_centrality = nx.pagerank(g, alpha=0.85, weight=edge_attribute_for_weight)
    stats['Page Rank']  = [v for k, v in pageRank_centrality.items()]

    # top 20 nodes with highest page rank
    print(stats.sort_values(by='Page Rank', ascending=False).head(20))

    # Distribution
    distribution = stats.groupby(['Page Rank']).size().reset_index(name='Frequency')
    sum = distribution['Frequency'].sum()
    distribution['Probability'] = distribution['Frequency'] / sum

    plots.create_plot("plots/businessProj_pageRank_distribution.pdf", "Page Rank distribution",
                      'Page Rank value', distribution['Page Rank'],
                       "Probability", distribution['Probability'],
                      xticks = [0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks = [0, 0.001], discrete=False) # FIXME boundaries
    plt.show()


# 11. Betweeness Centrality
edge_attribute_for_weight = None # it should be a string

if directed:
    betweeness_centrality = nx.betweenness_centrality(g, weight=edge_attribute_for_weight)
    stats['Betweeness']  = [v for k, v in betweeness_centrality.items()]

    # top 20 nodes with highest betweeness ranking
    print(stats.sort_values(by='Betweeness', ascending=False).head(20))

    # Distribution
    distribution = stats.groupby(['Betweeness']).size().reset_index(name='Frequency')
    sum = distribution['Frequency'].sum()
    distribution['Probability'] = distribution['Frequency'] / sum

    plots.create_plot("plots/businessProj_betweeness_distribution.pdf", "Betweenss centrality distribution",
                      'Betweeness centrality value', distribution['Betweeness'],
                       "Probability", distribution['Probability'],
                      xticks = [0, 0.01, 0.02, 0.03, 0.04, 0.042], yticks = [0, 0.001], discrete=False) # FIXME boundaries
    plt.show()



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

