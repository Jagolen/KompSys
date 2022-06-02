#Simulated evacuation from a room for the Modelling Complex Systems course

#By Jakob Gölén, Oskar Ekstrand, Marcus Nises, Simon Persson

#Implementing model from: https://www.sciencedirect.com/science/article/pii/S0378437107003676

import numpy as np
import math
import argparse
import sys
import random
import time
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()

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
    if gridval[x,y] == 500 or gridval[x,y] == 100:
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
                elif gridval[i,j] == 500 or gridval[i,j] == 100:
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

def update_val(grid, gridval,N,M):
    res = 0
    for x in range(N):
        for y in range(M):
            if grid[x,y] == 3 or grid[x,y] == 4 or gridval[x,y] == 0:
                pass
            else:
                lambda_val = 1.5
                for i in range(x-1,x+2):
                    for j in range(y-1,y+2):
                        if ((i == x and j == y) or (i <= 0 or j <= 0 or i>=(N-1) or j>=(M-1))):
                            res += 0
                        elif gridval[i,j] < gridval[x,y] and gridval[i,j] > 0:
                            res += 0
                        elif gridval[i,j] == 500 or gridval[i,j] == 100:
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
    if res:
        update_val(grid, gridval, N, M)


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
            people_pos.append([i, x_rand, y_rand, x_rand, y_rand])
    
    elif argument == 'classroom':
        xlist = [1, 2, 3, 6, 7, 8, 9, 12, 13, 14]
        ylist = [5, 8, 11, 14, 17]
        i = 0
        for y in ylist:
            for x in xlist:
                grid[x,y] = 1
                people_pos.append([i, x, y, x, y])
                i += 1
    
    elif argument == 'dense_classroom':
        xlist = [1, 2, 3, 6, 7, 8, 9, 12, 13, 14]
        ylist = [5, 7, 9, 11, 13, 15, 17]        
        i = 0
        for y in ylist:
            for x in xlist:
                grid[x,y] = 1
                people_pos.append([i, x, y, x, y])
                i += 1

    elif argument == 'single_obstacle':
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
            people_pos.append([i, x_rand, y_rand, x_rand, y_rand])

def place_fire(grid, gridval, N, M):
    xlist = [7]
    ylist = [4]
    for x in xlist:
        for y in ylist:
            gridval[x,y] = 100
            grid[x,y] = 4

def fire_spread(grid, gridval, N, M, fire_factor):
    next_grid = np.zeros([N,M])
    
    for i in range(N):
        for j in range(M):
            if gridval[i,j] == 500:
                next_grid[i,j] = 3
            elif gridval[i,j] == 1:
                next_grid[i,j] = 2
            elif gridval[i,j] == 100:
                next_grid[i,j] = 4

    spread_rate = fire_factor
    #Iterate over fire cells and create new fire
    for i in range(N):
        for j in range(M):
            if grid[i,j] == 4:
                for l in range(i-1, i+2):
                    for m in range(j-1, j+2):
                        if l < 0 or m < 0 or l > N-1 or m > M-1:
                            pass
                        elif grid[l,m] !=4 and random.random() < spread_rate:
                            next_grid[l,m] = 4
                            gridval[l,m] = 100
                            
    #Determine new gridval
    for i in range(N):
        for j in range(M):
            if next_grid[i,j] == 4:
                for l in range(i-1, i+2):
                    for m in range(j-1, j+2):
                        if l < 0 or m < 0 or l > N-1 or m > M-1:
                            pass
                        elif next_grid[l,m] == 0 or next_grid[l,m] == 1:
                            gridval[l,m] += 0.6

    grid = next_grid
    return grid, gridval


def move_people(grid, gridval, N, M, people_pos, escape_time, dead_time, time_step, scared_factor,fire_factor):

    fire_spread(grid,gridval,N,M,fire_factor)
    intended_move = []
    next_grid = np.zeros([N,M])
    for i in range(N):
        for j in range(M):
            if gridval[i,j] == 500:
                next_grid[i,j] = 3
            elif gridval[i,j] == 1:
                next_grid[i,j] = 2
            elif gridval[i,j] == 100:
                next_grid[i,j] = 4
    for k in people_pos:
        if random.random() < scared_factor:
            continue
        elif (k[3] == -1 and k[4] == -1) or (k[3] == -1 and k[4] == -1):
            continue
        elif gridval[k[3], k[4]] == 1:
            k[3] = -1
            k[4] = -1
            escape_time.append([k[0], time_step])
        elif gridval[k[3], k[4]] == 100 and k[3] != -2 and k[3] != -1:
            k[3] = -2
            k[4] = -2
            dead_time.append([k[0], time_step])

        else:
            current_pos = [k[3], k[4]]
            score = gridval[k[3], k[4]]
            possible_pos = [[k[3], k[4]]]
            for i in range(current_pos[0]-1, current_pos[0]+2):
                for j in range(current_pos[1]-1, current_pos[1]+2):
                    if i < 0 or j < 0 or i > N-1 or j > M-1:
                        pass
                    elif gridval[i,j] < score and grid[i,j] != 1:
                        possible_pos = [[i,j]]
                        score = gridval[i,j]
                    elif gridval[i,j] == score and grid[i,j] != 1:
                        possible_pos.append([i,j])
            
            if len(possible_pos) == 1:
                intended_move.append([k[0], possible_pos[0][0], possible_pos[0][1]])
            else:
                random_nr = random.randint(0, len(possible_pos)-1)
                intended_move.append([k[0], possible_pos[random_nr][0], possible_pos[random_nr][1]])
    while len(intended_move) != 0:
        int_moves = intended_move[0]
        conflicts = []
        conflicts.append(int_moves[0])
        for z in intended_move:
            if (z[1] == int_moves[1] and z[2] == int_moves[2] and z != int_moves):
                conflicts.append(z[0])
        if len(conflicts) == 1:
            people_pos[int_moves[0]][3] = int_moves[1]
            people_pos[int_moves[0]][4] = int_moves[2]
            intended_move.pop(0)
        else:
            nr_conflicts = len(conflicts)
            chosen_person = random.randint(0,nr_conflicts-1)
            chosen_person = conflicts[chosen_person]
            for z in intended_move:
                if z[0] == chosen_person:
                    people_pos[chosen_person][3] = z[1]
                    people_pos[chosen_person][4] = z[2]
            while conflicts:
                z_index = 0
                z = intended_move[z_index]
                while True:
                    if z[0] == conflicts[0]:
                        intended_move.remove(z)
                        conflicts.remove(conflicts[0])
                        break
                    else:
                        z_index+=1
                        z = intended_move[z_index]
    
    
    left_in_room = 0
    for i in people_pos:
        if (i[3] != -1 and i[4] != -1) and (i[3] != -2 and i[4] != -2):
            next_grid[i[3], i[4]] = 1
            left_in_room += 1
    grid = next_grid
    return grid, left_in_room


def resize_console(rows, cols):
    """
    Re-sizes the console to the size of rows x columns
    :param rows: Int - The number of rows for the console to re-size to
    :param cols: Int - The number of columns for the console to re-size to
    """

    if sys.platform.startswith('win'):
        command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
        os.system(command)
    elif sys.platform.startswith('linux'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        sys.stdout.write(command)
    elif sys.platform.startswith('darwin'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        sys.stdout.write(command)
    else:
        print("Unable to resize terminal. Your operating system is not supported.\n\r")

def clear_console():
    """
    Clears the console using a system command based on the user's operating system.
    """

    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    elif sys.platform.startswith('darwin'):
        os.system("clear")
    else:
        print("Unable to clear terminal. Your operating system is not supported.\n\r")


def print_grid(N, M, grid, time_step, people_pos):
    """
    Prints to console the A Firing Brain grid
    :param rows: Int - The number of rows that the A Firing Brain grid has
    :param cols: Int - The number of columns that the A Firing Brain grid has
    :param grid: Int[][] - The list of lists that will be used to represent the A Firing Brain grid
    :param generation: Int - The current generation of the A Firing Brain grid
    """

    #clear_console()

    # A single output string is used to help reduce the flickering caused by printing multiple lines
    output_str = ""

    # Compile the output string together and then print it to console
    output_str += "Time step {0} - To exit the program press <Ctrl-C>\n\r".format(time_step)
    for row in range(N):
        for col in range(M):
            if grid[row,col] == 0:
                output_str += ".  "
            elif grid[row,col] == 1:
                #output_str += "@  "
                for pers in people_pos:
                    if pers[3] == row and pers[4] == col:
                        output_str += f"{pers[0]} ".zfill(3)
            elif grid[row,col] == 3:
                output_str += "□  "
            elif grid[row,col] == 4:
                output_str += "X  "
            else:
                output_str += "_  "
        output_str += "\n\r"
    print(output_str, end=" ")
    time.sleep(0.01)

def print_anything(something):
    print(something)






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
    parser.add_argument('--mode', dest='mode_mode', required=False)
    parser.add_argument('--fire', dest='fire', required=False)
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
            #grid[15, 2] = 2
            #gridval[15, 2] = 1
            #grid[2, 19] = 2
            #gridval[2, 19] = 1

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
    

    people_pos = []
    escape_time = []
    dead_time = []
    x = []
    y = []
    num_people = 30

    if args.t == 'std_empty':
        spawn_people(grid, N, M, num_people, people_pos, args.t)
    
    elif args.t == 'classroom':
        num_people = 50
        spawn_people(grid, N, M, num_people, people_pos, args.t)
    
    elif args.t == 'dense_classroom':
        num_people = 70
        spawn_people(grid, N, M, num_people, people_pos, args.t)
    
    elif args.t == 'single_obstacle':
        spawn_people(grid, N, M, num_people, people_pos, args.t)
    else:
        if args.ppl:
            num_people = int(args.ppl)

    if args.fire:
        place_fire(grid, gridval, N, M)

    if args.mode_mode == 'single':
        #Starting grid
        scared_factor = 0.05
        print_grid(N, M, grid, 0, people_pos)
        i = 0
        print(gridval)
        while True:
            next_gridval = np.zeros([16,20])
            for n in range(N):
                for m in range(M):
                    if grid[n,m] == 3 or grid[n,m] == 4 or gridval[n,m] == 1:
                        next_gridval[n,m] = gridval[n,m]
            update_val(grid,next_gridval,N,M)
            gridval = next_gridval
            i+=1
            grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, dead_time, i+1, scared_factor)
            print_grid(N, M, grid, i+1, people_pos)
            x.append(i)
            y.append(left_in_room)
            print(len(escape_time) + len(dead_time))
            print(escape_time)
            print(dead_time)
            if len(escape_time) + len(dead_time) == num_people:
                break

        print(f'All people has left the room after {i} timesteps.')
        print(gridval)
        plt.plot(x,y)
        plt.show()
    


    elif args.mode_mode == 'scared_factor':
        matrix_n = 11
        matrix_m = 11
        scared_factor_list = np.linspace(0,0.3,matrix_m)
        fire_factor_list = np.linspace(0,0.3,matrix_n)
        heatmap_matrix = np.zeros((matrix_n,matrix_n))
        for scared_index, scared_factor in enumerate(scared_factor_list):
            for fire_index, fire_factor in enumerate(fire_factor_list):
                print_anything([scared_index,fire_index])
                # Grid of objects: 0 = empty, 1 = person, 2 = door, 3 = wall/furniture, 4 = fire
                grid = np.zeros([N,M])

                #Value of the squares
                gridval = np.zeros([N,M])

                #Put walls around the grid
                put_walls(grid, gridval, N, M)
                
                # doors
                grid[15, 2] = 2
                gridval[15, 2] = 1
                grid[2, 19] = 2
                gridval[2, 19] = 1
                # benches
                place_furniture(grid,gridval, N, M, args.t)

                people_pos = []
                escape_time = []
                dead_time = []
                xlist = [1, 2, 3, 6, 7, 8, 9, 12, 13, 14]
                ylist = [5, 8, 11, 14, 17]
                i = 0
                for y in ylist:
                    for x in xlist:
                        grid[x,y] = 1
                        people_pos.append([i, x, y, x, y])
                        i += 1
                x = []
                y = []
                i = 0
                
                if args.fire:
                    place_fire(grid, gridval, N, M)
                #print_grid(N, M, grid, 0, people_pos)
                while True:
                    #print_grid(N, M, grid, 0, people_pos)
                    next_gridval = np.zeros([16,20])
                    for n in range(N):
                        for m in range(M):
                            if grid[n,m] == 3 or grid[n,m] == 4 or gridval[n,m] == 1:
                                next_gridval[n,m] = gridval[n,m]
                    update_val(grid,next_gridval,N,M)
                    gridval = next_gridval
                    i+=1
                    grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, dead_time, i+1, scared_factor, fire_factor)
                    if len(escape_time) + len(dead_time) == num_people:
                        heatmap_matrix[fire_index,scared_index]=float(len(dead_time))/num_people
                        break
        ax = sns.heatmap(heatmap_matrix)
        ax.set_xlabel("scared_index")
        ax.set_ylabel("fire_factor")
        ax.set_xticklabels([str(round(a,2)) for a in scared_factor_list])
        ax.set_yticklabels([str(round(a,2)) for a in fire_factor_list])
        plt.show()

          
    
    


main()
    




