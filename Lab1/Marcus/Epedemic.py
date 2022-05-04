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
    Creates a random list of lists that contains 1s and 0s to represent the cells in Epedemic spread.
    :param rows: Int - The number of rows that the Epedemic spread grid will have
    :param cols: Int - The number of columns that the Epedemic spread grid will have
    :return: Int[][] - A list of lists containing 1s for firing cells and 0s for ready cells
    """
    if case == 1: #case 1 is only one infected cell in middle
        grid = [[0]*cols]
        grid[0][int(cols/2)] = 1
    else: #otherwise randomly spread, row will be set to one
        grid = []
        for row in range(rows):
            grid_rows = []
            for col in range(cols):
                # Generate a random number and based on that decide whether to add an infected cell to the grid
                if random.random() <= p:
                    grid_rows += [1]
                else:
                    grid_rows += [0]
            grid += [grid_rows]
    return grid


def print_grid(rows, cols, grid, generation):
    """
    Prints to console the Epedemic spread grid
    :param rows: Int - The number of rows that the Epedemic spread grid has
    :param cols: Int - The number of columns that the Epedemic spread grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Epedemic spread grid
    :param generation: Int - The current generation of the Epedemic spread grid
    """

    clear_console()

    # A single output string is used to help reduce the flickering caused by printing multiple lines
    output_str = ""

    # Compile the output string together and then print it to console
    output_str += "Generation {0} - To exit the program press <Ctrl-C>\n\r".format(generation)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                output_str += ". " #suceptible
            else:
                output_str += "@ " #infected
        output_str += "\n\r"
    print(output_str, end=" ")


def create_next_grid(rows, cols, grid, next_grid, gamma, case):
    """
    Analyzes the current generation of the Epedemic spread grid and determines what cells live and die in the next
    generation of the Epedemic spread grid.
    :param rows: Int - The number of rows that the Epedemic spread grid has
    :param cols: Int - The number of columns that the Epedemic spread grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Epedemic spread grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Epedemic spread
    grid
    """

    for row in range(rows):
        for col in range(cols):
            # Get the number of infected adjacent to the cell at grid[row][col]
            infected_neighbors = get_infected_neighbors(row, col, rows, cols, grid, case)

            #If suceptible 
            if grid[row][col] == 0:
                if infected_neighbors: #if cell has infected neighbours it will be infected with chance 1-gamma
                    if random.random()<1-gamma:
                        next_grid[row][col] = 1
                    else: #otherwise stay suceptible
                        next_grid[row][col] = 0
                else: #otherwise stay suceptible
                    next_grid[row][col] = 0
            #If infected        
            else: 
                if random.random()<gamma: #recover with chance gamma
                    next_grid[row][col] = 0
                else: #stay infected
                    next_grid[row][col] = 1



def get_infected_neighbors(row, col, rows, cols, grid, case):
    """
    Counts the number of infected cells surrounding a center cell at grid[row][cell].
    :param row: Int - The row of the center cell
    :param col: Int - The column of the center cell
    :param rows: Int - The number of rows that the Epedemic spread grid has
    :param cols: Int - The number of columns that the Epedemic spread grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Epedemic spread grid
    :return: Int - The number of infected cells surrounding the cell at grid[row][cell]
    """

    #neighbours are only left and right
    infected_sum = 0
    infected_sum += grid[row][(col-1) % cols]
    infected_sum += grid[row][(col+1) % cols] 
    return infected_sum


def grid_changing(rows, cols, grid, next_grid):
    """
    Checks to see if the current generation Epedemic spread grid is the same as the next generation Epedemic spread grid.
    :param rows: Int - The number of rows that the Epedemic spread grid has
    :param cols: Int - The number of columns that the Epedemic spread grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Epedemic spread grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Epedemic spread
    grid
    :return: Boolean - Whether the current generation grid is the same as the next generation grid
    """

    for row in range(rows):
        for col in range(cols):
            # If the cell at grid[row][col] is not equal to next_grid[row][col]
            if not grid[row][col] == next_grid[row][col]:
                return True
    return False


def firing_count(rows, cols, grid): 
    """
    counts number of cells in grid with value 1
    """
    sum = 0

    for i in range(rows):
        sum += grid[i].count(1)

    return sum


def plot_fig(rows, cols, grid):
    """
    Plots the specified grid
    """

    fig, ax = plt.subplots()
    npgrid = np.matrix(grid)
    a = np.where(0 < npgrid, 3 - npgrid, npgrid)
    plt.imshow(a, cmap="Greys", origin = 'lower')


def run_game():
    """
    Asks the user for input to setup the Epedemic spread to run for a given number of generations.
    """
    clear_console()
    print(f'Enter 1 for case 1, 2 for case 2:\n')
    case = int(input())

    clear_console()
    print(f'Enter 0 for continous simulation, 1 for statistics, 2 for plots:\n')
    runtype = int(input())



    #set variables
    #gamma = [0.6, 0.5, 0.4, 0.3]
    gamma = [0.55, 0.5, 0.48, 0.47, 0.46, 0.45, 0.4] #chosen values for gamma
    p = [0.02, 0.05, 0.1, 0.2, 0.8] #chosen values for p
    
    # Get the number of rows and columns for the Epedemic spread grid

    rows = 1
    cols = 100
    clear_console()

    # Get the number of generations that the Epedemic spread should run for

    # Run Epedemic spread sequence
    if runtype == 0:
        resize_console(rows, cols)

        generations = 500 #simulation is capped at this number of generations, can be changed

        # Create the initial random Epedemic spread grids
        current_generation = create_initial_grid(rows, cols, p[0], case)
        next_generation = create_initial_grid(rows, cols, p[0], case)

        gen = 1
        for gen in range(1, generations + 1):
            print_grid(rows, cols, current_generation, gen) #print grid
            create_next_grid(rows, cols, current_generation, next_generation, gamma[2], case) #create next grid

            time.sleep(1 / 5.0)
            current_generation, next_generation = next_generation, current_generation #assign current gen as next gen

        print_grid(rows, cols, current_generation, gen)
        return input("<Enter> to exit or r to run again: ")

    elif runtype == 1: #for aquiring relative statistics
        generations = 500
        if case == 1:
            prob = [0]*len(gamma) #probability list
            iter = 100 #number of iterations for statistics to be averaged over
            for i in range(0, len(gamma)): #iterate over gammas
                print(f'iteration {i}')
                for j in range(iter): #run for iter times
                    #initial grid
                    current_generation = create_initial_grid(rows, cols, p, case)
                    next_generation = create_initial_grid(rows, cols, p, case)
                    gen = 1
                    for gen in range(1, generations + 1):
                        create_next_grid(rows, cols, current_generation, next_generation, gamma[i], case)
                        current_generation, next_generation = next_generation, current_generation
                    prob[i] += 1 if firing_count(rows, cols, current_generation) == 0 else 0 #probability of disease having died out
                prob[i] = 1 - prob[i]/iter #normalize

            #plots
            plt.plot(gamma, prob)
            plt.xlabel("gamma")
            plt.ylabel("probability of dicease surviving")
            plt.title("Average probability of dicease surviving for 500 timesteps")
            plt.show()
            return input("<Enter> to exit or r to run again: ")
        else:
            iter = 1000 #number of iterations for statistics to be aquired over
            for j in range(0, len(p)): #iterate over length of p
                print(f'iteration {j}') #print for the sake of my sanity
                prob = [0]*len(gamma)
                for i in range(0, len(gamma)): #iterate over gammas length
                    for k in range(iter): #iter times
                        current_generation = create_initial_grid(rows, cols, p[j], case)
                        next_generation = create_initial_grid(rows, cols, p[j], case)
                        gen = 1
                        for gen in range(1, generations + 1):
                            create_next_grid(rows, cols, current_generation, next_generation, gamma[i], case)
                            current_generation, next_generation = next_generation, current_generation
                        prob[i] += 1 if firing_count(rows, cols, current_generation) == 0 else 0 #probability of disease having died out
                    prob[i] = 1 - prob[i]/iter #normalize
                    #plots
                plt.plot(gamma, prob)
            plt.xlabel("gamma")
            plt.ylabel("probability of disease surviving")
            plt.title("Average probability of disease surviving for 500 timesteps")
            plt.legend(p)
            plt.show()
            return input("<Enter> to exit or r to run again: ")

    elif runtype == 2: #for aquiring another set of statistics
        generations = 500
        if case == 1:
            for i in range(0, len(gamma)):
                print(f'iteration {i}')
                infected = [0]*generations
                for j in range(100):
                    current_generation = create_initial_grid(rows, cols, p, case)
                    next_generation = create_initial_grid(rows, cols, p, case)
                    gen = 1
                    for gen in range(1, generations + 1):
                        create_next_grid(rows, cols, current_generation, next_generation, gamma[i], case)
                        current_generation, next_generation = next_generation, current_generation
                        infected[gen-1] += firing_count(rows, cols, current_generation) #number of infected cells for each timestep
                infected[:] = [x/100 for x in infected] #normalize
                plt.plot(range(generations), infected)
            plt.legend(gamma)
            plt.xlabel("time")
            plt.ylabel("number of infected cells")
            plt.title("Average number of infected cells over 500 timesteps for different gamma")
            plt.show()
            return input("<Enter> to exit or r to run again: ")
        else:
            print("runtype 2 does not exist for case 2")
            return input("<Enter> to exit or r to run again: ")
    

# Start the Epedemic spread
run = "r"
while run == "r":
    out = run_game()
    run = out