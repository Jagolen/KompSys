#! /usr/bin/python3

from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import igraph

G = nx.grid_2d_graph(4,4, [False, False])
nx.draw(G)
plt.show()


G2 = nx.read_pajek("Roget.net")
G3 = nx.Graph(G2)

nx.draw(G3)
plt.show()