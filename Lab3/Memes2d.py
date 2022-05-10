#! /usr/bin/python3

from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

G = nx.grid_2d_graph(4,4, [False, False])
nx.draw(G)
plt.show()