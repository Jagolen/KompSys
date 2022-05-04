#!/usr/bin/env python3

from locale import normalize
import time
import os
import random
import sys
import matplotlib.pyplot as plt
import numpy as np

#https://github.com/mwharrisjr/Game-of-Life/blob/master/script/main.py


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


def resize_console(rows, cols):
    """
    Re-sizes the console to the size of rows x columns
    :param rows: Int - The number of rows for the console to re-size to
    :param cols: Int - The number of columns for the console to re-size to
    """

    if cols < 32:
        cols = 32

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


def create_initial_grid(rows, cols, p, case):
    """
    Creates a random list of lists that contains 1s and 0s to represent the cells in A Firing Brain.
    :param rows: Int - The number of rows that the A Firing Brain grid will have
    :param cols: Int - The number of columns that the A Firing Brain grid will have
    :return: Int[][] - A list of lists containing 1s for firing cells and 0s for ready cells
    """
    if case == 1:
        grid = [[0]*cols]
        grid[0][int(cols/2)] = 1
    else:
        grid = []
        for row in range(rows):
            grid_rows = []
            for col in range(cols):
                # Generate a random number and based on that decide whether to add a live or dead cell to the grid
                if random.random() <= p:
                    grid_rows += [1]
                else:
                    grid_rows += [0]
            grid += [grid_rows]
    return grid


def print_grid(rows, cols, grid, generation):
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
    output_str += "Generation {0} - To exit the program press <Ctrl-C>\n\r".format(generation)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                output_str += ". "
            elif grid[row][col] == 1:
                output_str += "@ "
            elif grid[row][col] == 3:
                output_str += "X "
            else:
                output_str += "_ "
        output_str += "\n\r"
    print(output_str, end=" ")


def create_next_grid(rows, cols, grid, next_grid, gamma, case):
    """
    Analyzes the current generation of the A Firing Brain grid and determines what cells live and die in the next
    generation of the A Firing Brain grid.
    :param rows: Int - The number of rows that the A Firing Brain grid has
    :param cols: Int - The number of columns that the A Firing Brain grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
    grid
    """

    for row in range(rows):
        for col in range(cols):
            # Get the number of firing cells adjacent to the cell at grid[row][col]
            infected_neighbors = get_infected_neighbors(row, col, rows, cols, grid, case)

            #If suceptible 
            if grid[row][col] == 0:
                if infected_neighbors:
                    if random.random()<1-gamma: #If suceptible and has infected neigbours 1-gamma --> infected
                        next_grid[row][col] = 1
                    else:
                        next_grid[row][col] = 0
                else:
                    next_grid[row][col] = 0
                
            #If infected
            elif grid[row][col] == 1:
                if random.random()<gamma/2:#If infected gamma/2 --> recovered
                    if case == 3:
                        next_grid[row][col] = 2
                    else:
                        next_grid[row][col] = 0
                elif case == 3 and random.random()<beta:#If not recovered and case 3 beta --> dead
                    next_grid[row][col] = 3
                else:
                    next_grid[row][col] = 1
            #If immune
            elif grid[row][col] == 2:
                if random.random()<1-gamma:#If immune 1-gamma --> suceptible
                    next_grid[row][col] = 0
                else:
                    next_grid[row][col] = 2
            else:
                next_grid[row][col] = 3






def get_infected_neighbors(row, col, rows, cols, grid, case):
    """
    Counts the number of live cells surrounding a center cell at grid[row][cell].
    :param row: Int - The row of the center cell
    :param col: Int - The column of the center cell
    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
    :return: Int - The number of live cells surrounding the cell at grid[row][cell]
    """



    if case == 3:
        infected_sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Make sure to count the center cell located at grid[row][col]
                if not (i == 0 and j == 0):
                    # Using the modulo operator (%) the grid wraps around
                    infected_sum += 1 if (grid[((row + i) % rows)][((col + j) % cols)] == 1) else 0
    else:
        infected_sum = 0
        infected_sum += grid[row][(col-1) % cols]
        infected_sum += grid[row][(col+1) % cols]
    return infected_sum


def grid_changing(rows, cols, grid, next_grid):
    """
    Checks to see if the current generation Game of Life grid is the same as the next generation Game of Life grid.
    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
    grid
    :return: Boolean - Whether the current generation grid is the same as the next generation grid
    """

    for row in range(rows):
        for col in range(cols):
            # If the cell at grid[row][col] is not equal to next_grid[row][col]
            if not grid[row][col] == next_grid[row][col]:
                return True
    return False


def get_integer_value(prompt, low, high):
    """
    Asks the user for integer input and between given bounds low and high.
    :param prompt: String - The string to prompt the user for input with
    :param low: Int - The low bound that the user must stay within
    :param high: Int - The high bound that the user must stay within
    :return: The valid input value that the user entered
    """

    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Input was not a valid integer value.")
            continue
        if value < low or value > high:
            print("Input was not inside the bounds (value <= {0} or value >= {1}).".format(low, high))
        else:
            break
    return value

def firing_count(rows, cols, grid, num):
    sum = 0

    for i in range(rows):
        sum += grid[i].count(num)

    return sum



def plot_fig(rows, cols, grid):
    """
    Plots the specified grid
    """

    fig, ax = plt.subplots()
    npgrid = np.matrix(grid)
    a = np.where(0 < npgrid, 3 - npgrid, npgrid)
    plt.imshow(a, cmap="Greys", origin = 'lower')

beta = 0.01

def run_game():
    """
    Asks the user for input to setup the A Firing Brain to run for a given number of generations.
    """
    case = 3

    clear_console()
    print(f'Enter 0 for continous simulation, 1 for statistics, 2 for plots:\n')
    runtype = int(input())



    #set variables
    #gamma = [0.6, 0.5, 0.4, 0.3]
    p = 0.05
    gamma = [0.9, 0.88, 0.86, 0.84, 0.82, 0.8]
    # Get the number of rows and columns for the A Firing Brain grid
    rows = 40
    cols = rows

    clear_console()

    # Get the number of generations that the A Firing Brain should run for
    


    # Run A Firing Brain sequence
    if runtype == 0:
        resize_console(rows, cols)

        generations = 800
        # Create the initial random A Firing Brain grids
        current_generation = create_initial_grid(rows, cols, p, case)
        next_generation = create_initial_grid(rows, cols, p, case)
        gen = 1
        for gen in range(1, generations + 1):
            #if not grid_changing(rows, cols, current_generation, next_generation):
            #        break
            print_grid(rows, cols, current_generation, gen)    
            create_next_grid(rows, cols, current_generation, next_generation, gamma[2], case)

            time.sleep(1 / 5.0)
            current_generation, next_generation = next_generation, current_generation

        print_grid(rows, cols, current_generation, gen)
        return input("<Enter> to exit or r to run again: ")
    elif runtype == 1:
        generations = 800
        if case == 1:
            prob = [0]*len(gamma)

            for i in range(0, len(gamma)):
                print(f'iteration {i}')
                for j in range(100):
                    current_generation = create_initial_grid(rows, cols, p, case)
                    next_generation = create_initial_grid(rows, cols, p, case)
                    gen = 1
                    for gen in range(1, generations + 1):
                        create_next_grid(rows, cols, current_generation, next_generation, gamma[i], case)
                        current_generation, next_generation = next_generation, current_generation
                    prob[i] += 1 if firing_count(rows, cols, current_generation, 1) == 0 else 0 #probability of disease having died out
                prob[i] = 1 - prob[i]/100 #normalize

            plt.plot(gamma, prob)
            plt.xlabel("gamma")
            plt.ylabel("probability of dicease surviving")
            plt.title("Average probability of dicease surviving for 500 timesteps")
            plt.show()
            return input("<Enter> to exit or r to run again: ")
        else:
            iter = 10
            generations = 500
            for j in range(0, len(p)):
                print(f'iteration {j}')
                prob = [0]*len(gamma)
                for i in range(0, len(gamma)):
                    
                    for k in range(iter):
                        current_generation = create_initial_grid(rows, cols, p[j], case)
                        next_generation = create_initial_grid(rows, cols, p[j], case)
                        gen = 1
                        for gen in range(1, generations + 1):
                            create_next_grid(rows, cols, current_generation, next_generation, gamma[i], case)
                            current_generation, next_generation = next_generation, current_generation
                        prob[i] += 1 if firing_count(rows, cols, current_generation, 1) == 0 else 0 #probability of disease having died out
                    prob[i] = 1 - prob[i]/iter #normalize
                plt.plot(gamma, prob)
            plt.xlabel("gamma")
            plt.ylabel("probability of dicease surviving")
            plt.title("Average probability of dicease surviving for 500 timesteps")
            plt.legend(p)
            plt.show()
            return input("<Enter> to exit or r to run again: ")
    elif runtype == 2:
        generations = 500
        iter = 1
        for i in range(0, 1):
            #print(f'iteration {i}')
            sus = [0]*generations
            infected = [0]*generations
            immune = [0]*generations
            dead = [0]*generations
            for j in range(iter):
                print(f'iteration {j}')
                current_generation = create_initial_grid(rows, cols, p, case)
                next_generation = create_initial_grid(rows, cols, p, case)
                gen = 1
                for gen in range(1, generations + 1):
                    create_next_grid(rows, cols, current_generation, next_generation, 0.85, case)
                    current_generation, next_generation = next_generation, current_generation
                    sus[gen-1] += firing_count(rows, cols, current_generation, 0)
                    infected[gen-1] += firing_count(rows, cols, current_generation, 1) #number of infected cells for each timestep
                    immune[gen-1] += firing_count(rows, cols, current_generation, 2)
                    dead[gen-1] += firing_count(rows, cols, current_generation, 3)
            sus[:] = [x/iter for x in sus] #normalize
            infected[:] = [x/iter for x in infected] #normalize
            immune[:] = [x/iter for x in immune] #normalize
            dead[:] = [x/iter for x in dead] #normalize
            plt.plot(range(generations), sus)
            plt.plot(range(generations), infected)
            plt.plot(range(generations), immune)
            plt.plot(range(generations), dead)
        leg = ["suceptible", "infected", "immune", "dead"]
        plt.legend(leg)
        plt.xlabel("Time")
        plt.ylabel("Number of cells")
        plt.title("Average number of affected cells over 500 timesteps")
        plt.show()
        return input("<Enter> to exit or r to run again: ")


            

    


# Start the A Firing Brain
run = "r"
while run == "r":
    out = run_game()
    run = out