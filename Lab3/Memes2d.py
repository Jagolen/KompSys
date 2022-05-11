#! /usr/bin/python3

from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

gridsize = 4

G = nx.grid_2d_graph(gridsize,gridsize, [True, True])
nx.draw(G)
plt.show()

nodeslattice = G.number_of_nodes()
print(nodeslattice)

twodin = np.zeros([nodeslattice,nodeslattice])
twodin[2,2] = 2
twodin[1,1] = 1
print(twodin)
twodout = np.zeros([nodeslattice,nodeslattice])

p = 0.001
q = 0.01
r = 0.01

the_nodes = G.nodes
ne = G.edges((0,0))
neighbors = [ne[1] for ne in G.edges((0,0))]
iter = 4000
for k in range(iter):
    for i in range(gridsize):
        for j in range(gridsize):
            if twodin[i,j] == 0:
                if random.random()>p:
                    twodout[i,j] = 0
                else:
                    twodout[i,j] = 1
            elif twodin[i,j] == 1:
                if random.random()>q:
                    twodout[i,j] = 1
                else:
                    neighbors = [ne[1] for ne in G.edges((i,j))]
                    chosen_neighbor = neighbors[random.randint(0,len(neighbors)-1)]
                    if twodin[chosen_neighbor[0], chosen_neighbor[1]] == 0:
                        twodout[chosen_neighbor[0], chosen_neighbor[1]] = 0
                        twodout[i,j] = 1
                    elif twodin[chosen_neighbor[0], chosen_neighbor[1]] == 2:
                        twodout[i,j] = 2
                    else:
                        twodout[i,j] = 1
            else:
                if random.random()>r:
                    twodout[i,j] = 2
                else:
                    neighbors = [ne[1] for ne in G.edges((i,j))]
                    if twodin[chosen_neighbor[0], chosen_neighbor[1]] == 0:
                        twodout[i,j] = 0
                    else:
                        twodout[i,j] = 2
    twodin = np.copy(twodout)

print(twodout)

