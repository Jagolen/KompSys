# https://www.geeksforgeeks.org/conways-game-life-python-implementation/

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
 
# setting up the values for the grid
Fire = 1
Ready = 0.5
Resting = 0
vals = [Fire, Ready, Resting]
 

# Different grid types
def randomGrid(N):
 
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.3, 0.7, 0]).reshape(N, N)

def stationarygrid(grid, N):
    mid = N//2
    grid[mid-1, mid] = grid[mid+1, mid-1] = grid[mid+2, mid+1] = grid[mid, mid+2] = 0
    grid[mid,mid-1] = grid[mid+2,mid] = grid[mid+1,mid+2] = grid[mid-1,mid+1] = 1

def snegrid(grid, N):
    mid = N//2
    grid[mid+1,mid+1] = grid[mid+3,mid+2] = grid[mid+3,mid+3] = 0
    grid[mid+2,mid+1] = grid[mid+2,mid+3] = grid[mid+4,mid+3] = 1

def spindel(grid):
    grid[1,6] = grid[1,10] = grid[2,7] = grid[2,10] = grid[3,1] = grid[3,5] = grid[3,6] = grid[3,9] = grid[4,3] = grid[4,7] = grid[5,5] = 0
    grid[4,2] = grid[3,4] = grid[5,6] = grid[1,7] = grid[2,8] = grid[4,8] = grid[3,10] = grid[1,11] = grid[2,11] = grid[5,0] = 1

def mur(grid):
    grid[1,1] = grid[2,1] = grid[3,2] = grid[4,3] = grid[5,4] = grid[6,5] = grid[7,6] = grid[2,4] = grid[3,5] = grid[4,6] = grid[5,7] = grid[3,6] = 1
    grid[1,2] = grid[2,2] = grid[3,3] = grid[4,4] = grid[5,5] = grid[6,6] = grid[7,7] = grid[2,5] = grid[4,7] = 0

def glas(grid):
    grid[5,2] = grid[4,2] = grid[3,3] = grid[2,4] = grid[4,5] = grid[1,6] = grid[3,6] = grid[2,7] = grid[3,7] = grid[1,9] = grid[3,9] = 0
    grid[5,1] = grid[4,1] = grid[3,2] = grid[2,3] = grid[4,4] = grid[1,5] = grid[4,7] = grid[1,8] = grid[4,8] = grid[2,10] = 1

def trakig(grid):
    grid[2,3] = grid[3,3] = 1
    grid[2,2] = grid[3,2] = 0

def manualgrid(grid):
    # Manual grid configuration: Choose position and if it should be firing or resting
    # All positions not defined are set to ready
    print("x and y: ")
    x,y = input().split()
    x,y = int(x), int(y)
    print("Firing (1) or resting (0)?")
    state = input()
    grid[x, y] = state
    print("more?(y/n): ")
    r = input()
    if r == 'y':
        manualgrid(grid)

#Function to take a time step

def update(frameNum, img, grid, N, pictime):
    
    # Freezes the plot after a certain amount of time steps
    if pictime == frameNum:
        time.sleep(99999)

    # copy grid since we require 8 neighbors
    # for calculation and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
 
            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulaton takes place on a toroidal surface.

            list = [grid[i, (j-1)%N], grid[i, (j+1)%N],
                         grid[(i-1)%N, j], grid[(i+1)%N, j],
                         grid[(i-1)%N, (j-1)%N], grid[(i-1)%N, (j+1)%N],
                         grid[(i+1)%N, (j-1)%N], grid[(i+1)%N, (j+1)%N]]
            
            tot = list.count(1)
 
            # apply the rules
            if grid[i, j]  == 0.5:
                if tot == 2:
                    newGrid[i, j] = 1
                else:
                    newGrid[i, j] = 0.5
            elif grid[i, j] == 1:
                newGrid[i, j] = 0
            else:
                newGrid[i, j] = 0.5
 
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,
 
# main() function
def main():
 
    # setting up arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
 
    # different arguments (grid size, starting configuration, runtime)
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--manual', action='store_true', required=False)
    parser.add_argument('--stationary', action='store_true', required=False)
    parser.add_argument('--sne', action='store_true', required=False) # Diagonally moving shape
    parser.add_argument('--spindel', action='store_true', required=False) # Moves sideways
    parser.add_argument('--motormur', action='store_true', required=False) # Moves sideways and shoots particles behind which quickly vanishes
    parser.add_argument('--glasogon', action='store_true', required=False) # Not very usefull
    parser.add_argument('--trakig', action='store_true', required=False) # Simple moving shape
    parser.add_argument('--pic', dest='pictime', required=False) # Chooses when the plot should be frozen so a picture can be taken
    args = parser.parse_args()
     
    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)
    
    # Freeze the plots after a defined number of time steps
    # No defined time steps means the plots will never freeze
    pictime = -1
    if args.pictime:
        pictime = int(args.pictime)
         
    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)
 
    # declare grid
    grid = np.array([])
 
    # check the different configurations
    
    if args.manual:
        grid = np.full((N,N),0.5)
        manualgrid(grid)

    elif args.stationary:
        grid = np.full((N,N),0.5)
        stationarygrid(grid, N)

    elif args.sne:
        grid = np.full((N,N),0.5)
        snegrid(grid, N)

    elif args.spindel:
        grid = np.full((N,N),0.5)
        spindel(grid)

    elif args.motormur:
        grid = np.full((N,N),0.5)
        mur(grid)

    elif args.glasogon:
        grid = np.full((N,N),0.5)
        glas(grid)
    
    elif args.trakig:
        grid = np.full((N,N),0.5)
        trakig(grid)

    else:   # No defined grid will give a random grid
        grid = randomGrid(N)
 
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, vmin=0, vmax=1, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, pictime, ),
                                  frames = 10,
                                  interval=updateInterval,
                                  save_count=50)
    plt.show()

# call main
if __name__ == '__main__':
    main()