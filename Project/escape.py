#Simulated evacuation from a room for the Modelling Complex Systems course

#By Jakob Gölén, Oskar Ekstrand, Marcus Nises, Simon Persson

#Implementing model from: https://www.sciencedirect.com/science/article/pii/S0378437107003676

#Usage: python escape.py --mode x --type y
#Mode can be: 
#single: a single run, with graphics
#scared_factor: measure how escape time changes with scared factor
#people: measure how escape time changes with number of people
#door_pos: measure how escape time changes with door position
#single_data: measure how the number of people in the room changes over time for both an empty room and the class room, ignores type

#Type can be:

#std_empty: an empty room
#classroom: a classroom with 50 people
#dense_classroom: a classroom with 70 people (unused in report)
#single object: a room where people has to walk around a wall in the middle of an empty room (unused in report)






from asyncio.windows_events import NULL
from distutils.spawn import spawn
from operator import index
from turtle import left
import numpy as np
import math
import argparse
import sys
import random
import time
import sys
import os
import matplotlib.pyplot as plt

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

def move_people(grid, gridval, N, M, people_pos, escape_time, time_step, scared_factor):
    intended_move = []
    next_grid = np.zeros([N,M])
    for i in range(N):
        for j in range(M):
            if gridval[i,j] == 500:
                next_grid[i,j] = 3
            elif gridval[i,j] == 1:
                next_grid[i,j] = 2
    for k in people_pos:
        if random.random() < scared_factor:
            continue
        elif k[3] == -1 and k[4] == -1:
            continue
        elif gridval[k[3], k[4]] == 1:
            k[3] = -1
            k[4] = -1
            escape_time.append([k[0], time_step])
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
        if i[3] != -1 and i[4] != -1:
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

    clear_console()

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
            else:
                output_str += "_  "
        output_str += "\n\r"
    print(output_str, end=" ")
    time.sleep(0.5)


def main():
    # Input parameters
    parser = argparse.ArgumentParser(description="Simulates evacuation from a room.")
    parser.add_argument('--manual-size', dest='msz', required=False) #Unused
    parser.add_argument('--doors', dest='door', required=False) #Unused
    parser.add_argument('--furniture', dest='furn',required=False) #Unused
    parser.add_argument('--type', dest='t', required=False)
    parser.add_argument('--people',dest='ppl', required=False)
    parser.add_argument('--mode', dest='mode_mode', required=False)
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
    escape_time = []
    x = []
    y = []
    num_people = 50

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
    
    if args.mode_mode == 'single':
        #Starting grid
        scared_factor = 0.05
        print_grid(N, M, grid, 0, people_pos)
        i = 0
        while True:
            i+=1
            grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, i+1, scared_factor)
            print_grid(N, M, grid, i+1, people_pos)
            x.append(i)
            y.append(left_in_room)
            if left_in_room == 0:
                break
        print(escape_time)
        print(f'All people has left the room after {i} timesteps.')
        print(gridval)
        plt.plot(x,y)
        plt.show()
    
    elif args.mode_mode == 'scared_factor':
        scared_factor_list = [x/100 for x in range(0,91,1)]
        for scared_factor in scared_factor_list:
            time_partial = 0
            nr_means = 20
            for k in range(nr_means):
                people_pos = []
                escape_time = []
                print(scared_factor)
                if args.t == 'std_empty':
                    spawn_people(grid, N, M, num_people, people_pos, args.t)
                
                elif args.t == 'classroom':
                    num_people = 50
                    spawn_people(grid, N, M, num_people, people_pos, args.t)
                i = 0
                while True:
                    i+=1
                    grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, i+1, scared_factor)
                    #print_grid(N, M, grid, 0, people_pos)
                    if left_in_room == 0:
                        break
                time_partial += i/nr_means
            x.append(scared_factor)        
            y.append(time_partial)
        plt.plot(x,y)
        plt.xlabel('Scared Factor')
        plt.ylabel('Time when everyone has left the room')
        plt.show()  
    
    elif args.mode_mode == 'people':
        xx = []
        yy = []
        parts = 30
        scared_factor = 0.05
        num_p_list = [x for x in range(1,253)]
        for p in num_p_list:
            time_partial = 0
            for k in range(parts):
                people_pos = []
                escape_time = []
                print(p)
                spawn_people(grid, N, M, p, people_pos, args.t)
                
                i = 0
                while True:
                    i+=1
                    grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, i+1, scared_factor)
                    #print_grid(N, M, grid, 0, people_pos)
                    if left_in_room == 0:
                        break
                time_partial += i/parts
            x.append(p)        
            y.append(time_partial)
        plt.plot(x,y)
        plt.xlabel('Number of people')
        plt.ylabel('Time when everyone has left the room')
        plt.show()  

    elif args.mode_mode == 'single_data':
        xx = []
        xx2 = []
        yy = []
        yy2 = []

        #Empty

        grid = np.zeros([N,M])

        #Value of the squares
        gridval = np.zeros([N,M])

        #Put walls around the grid
        put_walls(grid, gridval, N, M)
        grid[7,0] = 2
        gridval[7,0] = 1
        grid[8,0] = 2
        gridval[8,0] = 1

        place_furniture(grid,gridval, N, M, 'std_empty')

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
        num_people = 50
        scared_factor = 0.05
        spawn_people(grid, N, M, num_people, people_pos, 'std_empty')
        i = 0
        while True:
            i+=1
            grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, i+1, scared_factor)
            xx.append(i)
            yy.append(left_in_room)
            if left_in_room == 0:
                break




        #Empty
        grid = np.zeros([N,M])

        #Value of the squares
        gridval = np.zeros([N,M])



        #Put walls around the grid
        put_walls(grid, gridval, N, M)

        grid[15, 2] = 2
        gridval[15, 2] = 1
        grid[2, 19] = 2
        gridval[2, 19] = 1 

        place_furniture(grid,gridval, N, M, 'classroom')

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
        num_people = 50
        scared_factor = 0.05
        spawn_people(grid, N, M, num_people, people_pos, 'classroom')
        i = 0
        while True:
            i+=1
            grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, i+1, scared_factor)
            xx2.append(i)
            yy2.append(left_in_room)
            if left_in_room == 0:
                break

        plt.plot(xx,yy)
        plt.plot(xx2,yy2)
        plt.legend(['Empty', 'Classroom'])
        plt.xlabel('Time step')
        plt.ylabel('Number of people in room')
        plt.show()



    #Without furniture


    elif args.mode_mode == 'door_pos':


        door_pos = []
        for i in range(1,15):
            door_pos.append([i,0])
        door_pos.append([15,1])
        door_pos.append([15,2])
        door_pos.append([15,3])
        door_pos.append([15,6])
        door_pos.append([15,9])
        door_pos.append([15,12])
        door_pos.append([15,15])
        door_pos.append([15,18])
        for i in range(14,0,-1):
            door_pos.append([i,19])
        door_pos.append([0,18])
        door_pos.append([0,15])
        door_pos.append([0,12])
        door_pos.append([0,9])
        door_pos.append([0,6])
        door_pos.append([0,3])
        door_pos.append([0,2])
        door_pos.append([0,1])
  
        xx = []
        xx2 = []
        yy = []
        yy2 = []
        parts = 30
        for k in range(8, 30):
            print(k)
            partial_time = 0
            for partial in range(parts):

                chosen_door_pos = door_pos[k]
                # Grid of objects: 0 = empty, 1 = person, 2 = door, 3 = wall/furniture, 4 = fire
                grid = np.zeros([N,M])

                #Value of the squares
                gridval = np.zeros([N,M])

                #Put walls around the grid
                put_walls(grid, gridval, N, M)

                grid[chosen_door_pos[0], chosen_door_pos[1]] = 2
                gridval[chosen_door_pos[0], chosen_door_pos[1]] = 1  

                place_furniture(grid,gridval, N, M, args.t)

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
                #print(gridval)

                people_pos = []
                escape_time = []
                num_people = 50
                scared_factor = 0.05
                spawn_people(grid, N, M, num_people, people_pos, args.t)
                i = 0
                while True:
                    i+=1
                    grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, i+1, scared_factor)
                    #print_grid(N, M, grid, i, people_pos)
                    if left_in_room == 0:
                        break
                partial_time += i
            xx.append(door_pos.index(chosen_door_pos))        
            yy.append(partial_time/parts)

        #Without furniture
        for k in range(8, 30):
            print(k)
            partial_time = 0
            for partial in range(parts):

                chosen_door_pos = door_pos[k]
                # Grid of objects: 0 = empty, 1 = person, 2 = door, 3 = wall/furniture, 4 = fire
                grid = np.zeros([N,M])

                #Value of the squares
                gridval = np.zeros([N,M])

                #Put walls around the grid
                put_walls(grid, gridval, N, M)

                grid[chosen_door_pos[0], chosen_door_pos[1]] = 2
                gridval[chosen_door_pos[0], chosen_door_pos[1]] = 1  

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
                num_people = 50
                scared_factor = 0.05
                spawn_people(grid, N, M, num_people, people_pos, args.t)
                i = 0
                while True:
                    i+=1
                    grid, left_in_room = move_people(grid, gridval, N, M, people_pos, escape_time, i+1, scared_factor)
                    #print_grid(N, M, grid, i, people_pos)
                    if left_in_room == 0:
                        break
                partial_time += i
            xx2.append(door_pos.index(chosen_door_pos))        
            yy2.append(partial_time/parts)
        plt.plot(xx,yy,'-o')
        plt.plot(xx2,yy2,'-^')
        plt.legend(['With furniture', 'Without furniture'])
        plt.xlabel('Door Position')
        plt.ylabel('Time when everyone has left the room')
        plt.show()  


main()
    




