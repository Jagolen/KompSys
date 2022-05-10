#! /usr/bin/python3

from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random 
rand = True


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


#parameters
n = num_vertices
m = real_G.size()
alpha_list = np.linspace(0,1,20)
c_global = np.zeros(np.size(alpha_list))
n_ave = 10
j = 0

#remove the smallest node
for alpha in alpha_list: 
    n_remove = int(alpha*n)
    for i in range(n_ave):
        if rand == True:
            G = nx.gnm_random_graph(n, m)
        else:
            G = real_G.copy()
        for nums in range(n_remove):
            deg_nodes = list(G.degree(list(range(n))))
            node = min(deg_nodes, key = lambda x: x[1])[0]
            G.remove_node(node)

        c_global[j] = nx.transitivity(G)
    print(f"Average global cluster coefficient for alpha = {alpha}: {c_global[j]}")
    j = j+1

#plots
plt.plot(alpha_list, c_global)
plt.ylabel("Global Clustering Coefficient")
plt.xlabel("Proportion of Low Degree Nodes Removed")
if rand == True:
    plt.title(f"Global Clustering Coefficient for random network with {n} nodes and {m} edges")
else:
    plt.title(f"Global Clustering Coefficient for real network with {n} nodes and {m} edges")
plt.show()