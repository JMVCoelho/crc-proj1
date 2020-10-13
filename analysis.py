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


# read file
file = "data/business-projection.edges"
g = nx.read_edgelist(file, delimiter=' ', create_using=nx.DiGraph)


# stats for each node
stats = pd.DataFrame(g.nodes())
stats.columns = ['Node']


print("ANALYSIS of", file)
weighted = False


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
in_degree_centrality    = nx.in_degree_centrality(g)
out_degree_centrality   = nx.out_degree_centrality(g)

stats['Degree']      = [v for k, v in degree_centrality.items()]
stats['In-Degree']   = [v for k, v in in_degree_centrality.items()]
stats['Out-Degree']  = [v for k, v in out_degree_centrality.items()]

# un-normalize
stats['Degree'] = round(stats['Degree'] * (n_nodes-1))
stats['In-Degree'] = round(stats['In-Degree']  * (n_nodes-1))
stats['Out-Degree'] = round(stats['Out-Degree'] * (n_nodes-1))

# Top 10 nodes with highest DC
print(stats.sort_values(by='Degree', ascending=False).head(10))

# Degree distribution
distribution = stats.groupby(['Degree']).size().reset_index(name='Frequency')
sum = distribution['Degree'].sum()
distribution['Probability'] = distribution['Degree'] / sum
distribution.head(10)

fig = plt.figure()
fig.set_size_inches(14.0, 14.0)

# Plot in linear scale
ax = plt.subplot(2, 1, 1)
plt.scatter(distribution['Degree'], distribution['Probability'])
plt.title('Degree distribution (linear scale)')
plt.xlabel('Degree')
plt.ylabel('Probability')
plt.grid()

# Plot in log scale
ax = plt.subplot(2, 1, 2)
plt.scatter(distribution['Degree'], distribution['Probability'])
plt.title('Degree distribution (log scale)')
plt.xlabel('log(Degree)')
plt.ylabel('log(Probability)')
ax.set_xscale('log')
ax.set_ylim(ymin=0.0001)

ax.set_yscale('log')
ticks = [1,1e-01, 1e-02, 1e-03, 1e-04]
ax.set_yticks(ticks)
ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
plt.grid()
data = np.array(stats['Degree']) # data can be list or numpy array

# Power law
#fit = powerlaw.Fit(np.array(stats['Degree'])+1, discrete=True)
# OR WE CAN DEFINE XMIN PARAMETER TO ADJUST BETTER POWER LAW
#The data value beyond which distributions should be fitted. If None an optimal one will be calculated.
fit = powerlaw.Fit(np.array(stats['Degree'])+1, xmin=1.7, discrete=True)
fit.power_law.plot_pdf( color= 'b',linestyle='--',label='fit ccdf')
#fit.plot_pdf( color= 'r')

fig.savefig("plots/degree_distribution.pdf")

plt.show()

print('alpha= ',fit.power_law.alpha)