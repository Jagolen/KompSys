#! /usr/bin/python3

from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


### Create a real mf graph
df = open("airlines.txt", 'r')
num_vertices = 0

for line in df:
    line_list = line.strip().split()
    if line_list[0] == '*Vertices':
        num_vertices = int(line_list[1])
        break
real_G = nx.empty_graph(num_vertices)

#add the edges
reading_edges = False
for line in df:
    line_list = line.strip().split()
    if not reading_edges:
        if line_list[0] != "*Edges":
            continue
        else:
            reading_edges = True
            continue
    else:
        real_G.add_edge(int(line_list[0]), int(line_list[1]))


#Parameters
n = num_vertices
m = real_G.size()
runs = 30
c_global = np.zeros(runs)

#Find the clustering coefficients of the airline model
air_clustering = nx.transitivity(real_G)

#Find the clustering coefficients of the random graph
for i in range(runs):
    erdos = nx.gnm_random_graph(n,m)
    c_global[i] = nx.transitivity(erdos)

#plot the boxplots
plt.boxplot(c_global)
plt.plot(1,air_clustering,'*')
plt.xlabel("Erdos-Renyi and real network")
plt.ylabel('Clustering coefficient')

plt.show()

plt.boxplot(c_global)
plt.xlabel("Erdos-Renyi only")
plt.ylabel('Clustering coefficient')
plt.show()

print(c_global)
