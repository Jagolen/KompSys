#Simulated evacuation from a room for the Modelling Complex Systems course

#By Jakob Gölén, Oskar Ekstrand, Marcus Nises, Simon Persson

#Implementing model from: https://www.sciencedirect.com/science/article/pii/S0378437107003676

import numpy as np
import math
import argparse
import sys
import random

np.set_printoptions(suppress=True, linewidth=sys.maxsize, threshold=sys.maxsize)

def put_door(grid, gridval, N, M, nr_door):
    while nr_door > 0:
        print("Door location: ")
        x,y = input().split()
        x, y = int(x), int(y)
        if x>N or y>M or x<0 or y<0:
            print("Door is outside the room")
        else:
            grid[x,y] = 2
            gridval[x,y] = 1
            nr_door -= 1

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
        res = 0
        lambda_val = 1.5
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if ((i == x and j == y) or (i < 0 or j < 0 or i>(N-1) or j>(M-1))):
                    res += 0
                elif gridval[i,j] < gridval[x,y] and gridval[i,j] > 0:
                    res += 0
                elif gridval[i,j] == 500:
                    res += 0
                else:
                    if i == x or j == y:
                        temp = gridval[x,y] + 1
                        if temp < gridval[i,j] or gridval[i,j] == 0:
                            gridval[i,j] = temp
                            res += 1
                        else:
                            res += 0
                    else:
                        temp = gridval[x,y] + lambda_val
                        if temp < gridval[i,j] or gridval[i,j] == 0:
                            gridval[i,j] = temp
                            res += 1
                        else:
                            res += 0
        return res

def place_furniture(grid, gridval, N, M, type):
    #Classroom
    if type == 'classroom':
        xlist = [1, 2, 3, 6, 7, 8, 9, 12, 13, 14]
        ylist = [4, 7, 10, 13, 16]
        for x in xlist:
            for y in ylist:
                gridval[x,y] = 500
                grid[x,y] = 3
    elif type == 'single_obstacle':
        xlist = [5, 6, 7, 8, 9, 10, 11]
        ylist = [4]
        for x in xlist:
            for y in ylist:
                gridval[x,y] = 500
                grid[x,y] = 3
    
    elif type == 'dense_classroom':
        xlist = [1, 2, 3, 6, 7, 8, 9, 12, 13, 14]
        ylist = [4, 6, 8, 10, 12, 14, 16]
        for x in xlist:
            for y in ylist:
                gridval[x,y] = 500
                grid[x,y] = 3
                
    else:
        pass


def spawn_people(grid, N, M, num_people, people_pos, argument):
    if argument == 'std_empty':
        for i in range(num_people):
            valid_random_number = 0
            while valid_random_number == 0:
                x_rand = random.randint(1, N-2)
                y_rand = random.randint(1, M-2)
                if grid[x_rand, y_rand] == 0:
                    valid_random_number = 1
                else:
                    valid_random_number = 0
            grid[x_rand, y_rand] = 1

            # Person number, x & y start, x & y current 
            people_pos.append([i+1, x_rand, y_rand, x_rand, y_rand])





"""def randomGrid(N):
    returns a grid of NxN random values
    return np.random.choice(vals, N*N, p=[0.3, 0.7, 0]).reshape(N, N) """

def main():
    # Input parameters
    parser = argparse.ArgumentParser(description="Simulates evacuation from a room.")
    parser.add_argument('--manual-size', dest='msz', required=False)
    parser.add_argument('--doors', dest='door', required=False)
    parser.add_argument('--furniture', dest='furn',required=False)
    parser.add_argument('--type', dest='t', required=False)
    parser.add_argument('--people',dest='ppl', required=False)
    args = parser.parse_args()

    #Manual input
    if not args.msz:
        N,M = 16, 20
    else:
        print("Grid size: ")
        N,M = input().split()
        N,M = int(N), int(M)
    # Get size and create the grid

    # Grid of objects: 0 = empty, 1 = person, 2 = door, 3 = wall/furniture, 4 = fire
    grid = np.zeros([N,M])

    #Value of the squares
    gridval = np.zeros([N,M])

    #Put walls around the grid
    put_walls(grid, gridval, N, M)

    if args.t:
        if args.t == 'std_empty':
            grid[7,0] = 2
            gridval[7,0] = 1
            grid[8,0] = 2
            gridval[8,0] = 1
        
        elif args.t == 'classroom':
            grid[15, 2] = 2
            gridval[15, 2] = 1
            grid[2, 19] = 2
            gridval[2, 19] = 1
            place_furniture(grid,gridval, N, M, args.t)

        elif args.t == 'single_obstacle':
            grid[7,0] = 2
            gridval[7,0] = 1
            grid[8,0] = 2
            gridval[8,0] = 1
            place_furniture(grid,gridval, N, M, args.t)
        
        elif args.t == 'dense_classroom':
            grid[15, 2] = 2
            gridval[15, 2] = 1
            grid[2, 19] = 2
            gridval[2, 19] = 1
            place_furniture(grid,gridval, N, M, args.t)

    else:
        #Put a door
        if args.door:
            nr_door = int(args.door)
            put_door(grid, gridval, N, M, nr_door)
        
        #Place furniture
        if args.furn:
            place_furniture(grid,gridval, N, M, args.furn)



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
    print(gridval)

    people_pos = []
    num_people = 50

    if args.t == 'std_empty':
        num_people = 50
        spawn_people(grid, N, M, num_people, people_pos, args.t)
    else:
        if args.ppl:
            num_people = int(args.ppl)
    

    output_str = ""
    for row in range(N):
        for col in range(M):
            if grid[row,col] == 0:
                output_str += ".  "
            elif grid[row,col] == 1:
                for pers in people_pos:
                    if pers[3] == row and pers[4] == col:
                        output_str += f"{pers[0]} ".zfill(3)
            elif grid[row,col] == 3:
                output_str += "□  "
            else:
                output_str += "_  "
        output_str += "\n\r"
    print(output_str, end=" ")



main()
    




