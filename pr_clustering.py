import pandas as pd
import statistics
import pickle
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


stats = "stats.csv"
clustering = "business_projectionnot-weighted_clustering_coefficient.pickle"

stats = pd.read_csv(stats, header=0, sep=" ", usecols=[1,4])


with open(clustering, "rb") as handle:
    cls = pickle.load(handle)

stats['clustering'] = 0

stats['clustering'] = stats['Node'].map(cls)

X = np.array(stats['clustering'].to_list()).reshape(len(stats['clustering'].to_list()), 1)
Y = np.array(stats["Page Rank"].to_list()).reshape(len(stats["Page Rank"].to_list()), 1)


x = np.array(stats['clustering'].to_list())
y = np.array(stats["Page Rank"].to_list())


regr = linear_model.LinearRegression()
regr.fit(X, Y)

plt.scatter(X, Y,  color='blue')
#plt.plot(X, regr.predict(X), color='blue', linewidth=3)
#plt.yscale("log")
#plt.xscale("log")
plt.xticks(np.arange(min(x), max(x)+0.1, 0.1))
plt.yticks((min(y), max(y)-0.001, max(y)))
plt.xlabel("Clustering Coefficient")
plt.ylabel("PageRank Score")
plt.grid(True)
plt.show()