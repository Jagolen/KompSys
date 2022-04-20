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
        rndnr = random.random()
        if grid[i] == 1:
            if rndnr <= gamma:
                newGrid[i] = 0
        else:
            sum = grid[(i-1)%N] + grid[(i+1)%N]
            if sum >= 1:
                if rndnr > gamma:
                    newGrid[i] = 1
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def main():
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--one', action='store_true', required=False)
    parser.add_argument('--interval', dest='interval', required=False)


    args = parser.parse_args()
    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])

    if args.one:
        grid = np.zeros(N*N).reshape(N,N)
        OneInfected(grid)
# call main
if __name__ == '__main__':
    main()