#! /usr/bin/python3

from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random 

rand = True


### Create a real graph
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
alpha_list = np.linspace(0,1,20)
c_global = np.zeros(np.size(alpha_list))
n_ave = 30

j=0

#remove a random edge from a node of max degree
for alpha in alpha_list: 
    n_remove = int(alpha*m)
    for i in range(n_ave):
        if rand == True:
            G = nx.gnm_random_graph(n, m)
        else:
            G = real_G.copy()

        for nums in range(n_remove):
            deg_nodes = list(G.degree(list(range(n))))
            deg_max = max(deg_nodes, key = lambda x: x[1])[1]
            hits = [y[0] for y in deg_nodes if y[1] == deg_max]
            node = random.choice(hits)

            n_node = list(G.neighbors(node))
            neigh = random.choice(n_node)
            G.remove_edge(node,neigh)

        c_global[j] = nx.transitivity(G)
    print(f"Average global clust for alpha = {alpha}: {c_global[j]}")
    j += 1

#Plots
plt.plot(alpha_list, c_global)
plt.ylabel("Global Clustering Coefficient")
plt.xlabel("Proportion of Edges belonging to High Degree Nodes Removed")
if rand == True:
    plt.title(f"Global Clustering Coefficient for random network with {n} nodes and {m} edges")
else:
    plt.title(f"Global Clustering Coefficient for real network with {n} nodes and {m} edges")
plt.show()