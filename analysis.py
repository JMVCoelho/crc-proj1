import collections
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import powerlaw
import operator

register_matplotlib_converters()


def create_plot(path_to_save: str, title: str, xlabel: str, xdata: list, ylabel: str, ydata: list, yticks: list = None,
                also_log_scale: bool = False, log_yticks: list = None, powerlaw_xmin=None, powerlaw_xmax=None):
    fig = plt.figure()
    fig.set_size_inches(14.0, 14.0)

    # Plot in linear scale
    ax = plt.subplot(2 if also_log_scale else 1, 1, 1)
    plt.scatter(xdata, ydata)
    plt.title(title + ' (linear scale)' if also_log_scale else '')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if yticks:
        ax.set_ylim(ymin=yticks[0], ymax=yticks[len(yticks) - 1])
        ax.set_yticks(yticks)
    plt.grid()

    # Plot in log scale
    if also_log_scale:
        ax = plt.subplot(2, 1, 2)
        plt.scatter(xdata, ydata)
        plt.title(title + ' (log scale)')
        plt.xlabel('log(' + xlabel + ')')
        plt.ylabel('log(' + ylabel + ')')
        ax.set_xscale('log')
        ax.set_yscale('log')
        if log_yticks:
            ax.set_ylim(ymin=log_yticks[0], ymax=log_yticks[len(log_yticks)-1])
            ax.set_yticks(log_yticks)
        ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
        plt.grid()

    # Plot power law
    if powerlaw_xmin and powerlaw_xmax:
        fit = powerlaw.Fit(xdata + 1, xmin=powerlaw_xmin, xmax=powerlaw_xmax, discrete=True)
    else:
        fit = powerlaw.Fit(xdata + 1, discrete=True)

    fit.power_law.plot_pdf(color='r', linestyle='--', label='fit pdf')

    fig.savefig(path_to_save)

    if also_log_scale:
        return fit.power_law.alpha
    return


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

    alpha = create_plot("plots/degree_distribution.pdf", function + " distribution",
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
    passK



