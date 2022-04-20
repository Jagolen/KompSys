# https://www.geeksforgeeks.org/conways-game-life-python-implementation/


# Python code to implement Conway's Game Of Life
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
 
# setting up the values for the grid
Fire = 1
Ready = 0.5
Resting = 0
vals = [Fire, Ready, Resting]
 
def randomGrid(N):
 
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.3, 0.7, 0]).reshape(N, N)

def manualgrid(grid):
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
 
def update(frameNum, img, grid, N):
 
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
 
            # apply Conway's rules
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
 
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
 
    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--manual', action='store_true', required=False)
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
 
    # check if "manual" demo flag is specified
    
    if args.manual:
        grid = np.full((N,N),0.5)
        manualgrid(grid)


    else:   # populate grid with random on/off -
            # more off than on
        grid = randomGrid(N)
 
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, vmin=0, vmax=1, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = 10,
                                  interval=updateInterval,
                                  save_count=50)
 
    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()
 
# call main
if __name__ == '__main__':
    main()