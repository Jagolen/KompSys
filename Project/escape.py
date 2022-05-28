#Simulated evacuation from a room for the Modelling Complex Systems course

#By Jakob Gölén, Oskar Ekstrand, Marcus Nises, Simon Persson

#Implementing model from: https://www.sciencedirect.com/science/article/pii/S0378437107003676

import numpy as np
import math
import argparse


def put_door(grid, gridval, N, M):
    print("Door location: ")
    x,y = input().split()
    x, y = int(x), int(y)
    if x>N or y>M or x<0 or y<0:
        print("Door is outside the room")
        put_door(grid, gridval, N, M)
    else:
        grid[x,y] = 2
        gridval[x,y] = 1
        print("Another door? y/n: ")
        again = input()
        if again == 'y':
            put_door(grid, gridval, N, M)

def put_walls(grid, gridval, N, M):
    for i in range(N):
        grid[i,M-1] = 3
        gridval[i,M-1] = 500
        grid[i,0] = 3
        gridval[i,0] = 500
    for i in range(1,M-1):
        grid[N-1,i] = 3
        gridval[N-1,i] = 500
        grid[0,i] = 3
        gridval[0,i] = 500

def set_neighbor_val(gridval,x,y,N,M):
    if gridval[x,y] == 500:
        return 0
    else:
        lambda_val = 1.5
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if ((i == x and j == y) or (i < 0 or j < 0 or i>N-1 or j>M-1)):
                    res = 0
                elif gridval[i,j] < gridval[x,y] and gridval[i,j] > 0:
                    res = 0
                elif gridval[i,j] == 500:
                    res = 0
                else:
                    if i == x or j == y:
                        temp = gridval[x,y] + 1
                        if temp < gridval[i,j] or gridval[i,j] == 0:
                            gridval[i,j] = temp
                            res = 1
                        else:
                            res = 0
                    else:
                        temp = gridval[x,y] + lambda_val
                        if temp < gridval[i,j] or gridval[i,j] == 0:
                            gridval[i,j] = temp
                            res = 1
                        else:
                            res = 0
        return res


"""def randomGrid(N):
    returns a grid of NxN random values
    return np.random.choice(vals, N*N, p=[0.3, 0.7, 0]).reshape(N, N) """

def main():
    # Input parameters
    parser = argparse.ArgumentParser(description="Simulates evacuation from a room.")
    parser.add_argument('--N', dest='N', required=False)
    parser.add_argument('--M', dest='M', required=False)

    #Manual input
    print("Grid size: ")
    N,M = input().split()

    # Get size and create the grid
    N,M = int(N), int(M)
    grid = np.zeros([N,M])
    gridval = np.zeros([N,M])

    #Put walls around the grid
    put_walls(grid, gridval, N, M)

    #Put a door
    put_door(grid, gridval, N, M)

    # Get the values of every square
    counter_end = 1
    while counter_end !=0:
        counter_end = 0
        for x in range(N):
            for y in range(M):
                if gridval[x,y] != 0:
                    counter_end += set_neighbor_val(gridval,x,y,N,M)
                else:
                    counter_end += 1
    print("Done")
    print(gridval)



main()
    




