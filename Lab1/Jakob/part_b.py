# Spacial Epidemics

import argparse
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Infected = 1
Susceptible = 0

vals = [Infected, Susceptible]

def randomGrid(N):
    """returns an array of N random values"""
    return np.random.choice(vals, N*1, p=[0.01, 0.99]).reshape(N, 1)

def OneInfected(N):
    mid = N//2 + 1
    array = np.zeros((N,1))
    array[mid] = 1
    return array

def update(frameNum, img, grid, N, gamma):
 
    newGrid = grid.copy()
    for i in range(N):
        if grid[i] == 1:
            rndnr = random.random()

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,