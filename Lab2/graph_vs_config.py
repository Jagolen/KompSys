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

print("num_vertices =", num_vertices)
real_G = nx.empty_graph(num_vertices)

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



n = num_vertices
m = real_G.size()
degree_seq = [val for (node, val) in sorted(real_G.degree(), key=lambda pair: pair[0])]
print(degree_seq)
runs = 30
c_global = np.zeros(runs)
print(c_global)

air_clustering = nx.transitivity(real_G)
print(air_clustering)

for i in range(runs):
    H = nx.configuration_model(degree_seq, nx.Graph)
    c_global[i] = nx.transitivity(H)

plt.boxplot(c_global)
plt.plot(1,air_clustering,'*')
plt.xlabel("Configuration Model and real network")
plt.ylabel('Clustering coefficient')

plt.show()

plt.boxplot(c_global)
plt.xlabel("Configuration Model only")
plt.ylabel('Clustering coefficient')
plt.show()

print(c_global)
