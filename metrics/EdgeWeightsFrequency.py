from metrics.Metric import Metric
import matplotlib.pyplot as plt
from plots import plots
import pandas as pd


class EdgeWeightsFrequency(Metric):
    def __init__(self, graph, edge_attribute_for_weight='weight'):
        super().__init__(graph, weighted=True, directed=True, edge_attribute_for_weight=edge_attribute_for_weight)

    def compute(self, path_to_graph, name, pr=True):
        # Distribution

        data = pd.read_csv(path_to_graph, delim_whitespace=True, header=None)
        distribution = data.groupby([2]).size().reset_index(name='Frequency')

        sum = distribution['Frequency'].sum()
        distribution['Probability'] = distribution['Frequency'] / sum

        plots.create_bar("plots/" + name + "_rating_distribution.pdf", "",
                                  'Ratings', distribution[2],
                                  "Probability", distribution['Probability'],
                                  xbins=[1,2,3,4,5],
                                  yticks=[0, 0.1, 0.2, 0.3, 0.4])

        if pr:
            plt.show()

        return distribution
