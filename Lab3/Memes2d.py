#! /usr/bin/python3

from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

G = nx.grid_2d_graph(4,4, [False, False])
nx.draw(G)
plt.show()

nodeslattice = G.number_of_nodes()
print(nodeslattice)

twodin = np.zeros(nodeslattice)
twodin[0] = 1
twodin[1] = 2
print(twodin)
twodout = np.zeros(nodeslattice)

p = 0.001
q = 0.01
r = 0.01

the_nodes = list(G.nodes)
print(the_nodes)

iter = 4000
for i in range(iter):
    for j in range(nodeslattice):
        if twodin[j] == 0:
            if random.random()>p:
                twodout[j] = 0
            else:
                twodout[j] = 1
        elif twodin[j] == 1:
            if random.random()>q:
                twodout[j] = 1
            else:
                pass
