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
    Creates a random list of lists that contains 1s and 0s to represent the cells in Epedemic NN.
    :param rows: Int - The number of rows that the Epedemic NN grid will have
    :param cols: Int - The number of columns that the Epedemic NN grid will have
    :return: Int[][] - A list of lists containing 1s for firing cells and 0s for ready cells
    """

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
    Prints to console the Epedemic NN grid
    :param rows: Int - The number of rows that the Epedemic NN grid has
    :param cols: Int - The number of columns that the Epedemic NN grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Epedemic NN grid
    :param generation: Int - The current generation of the Epedemic NN grid
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
    Analyzes the current generation of the Epedemic NN grid and determines what cells live and die in the next
    generation of the Epedemic NN grid.
    :param rows: Int - The number of rows that the Epedemic NN grid has
    :param cols: Int - The number of columns that the Epedemic NN grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Epedemic NN grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Epedemic NN
    grid
    """

    for row in range(rows):
        for col in range(cols):
            # Get the number of infected cells adjacent to the cell at grid[row][col]
            infected_neighbors = get_infected_neighbors(row, col, rows, cols, grid, case)

            #If suceptible 
            if grid[row][col] == 0:
                if infected_neighbors:
                    if random.random()<1-gamma: #if cell has infected neighbours it will be infected with chance 1-gamma
                        next_grid[row][col] = 1
                    else: #otherwise stay suceptible
                        next_grid[row][col] = 0
                else:#otherwise stay suceptible
                    next_grid[row][col] = 0
            #If infected
            elif grid[row][col] == 1:
                if random.random()<gamma/2:#If infected recover with chance gamma/2 and become immune
                    next_grid[row][col] = 2
                elif random.random()<beta:#If not recovered cell will die with chance beta
                    next_grid[row][col] = 3
                else: #otherwise stay infected
                    next_grid[row][col] = 1
            #If immune
            elif grid[row][col] == 2:
                if random.random()<1-gamma:#If immune cell will become suceptible with chance 1-gamma
                    next_grid[row][col] = 0
                else: #otherwise stay immune
                    next_grid[row][col] = 2
            #If dead
            else:
                next_grid[row][col] = 3 #stay dead


def get_infected_neighbors(row, col, rows, cols, grid, case):
    """
    Counts the number of infected cells surrounding a center cell at grid[row][cell].
    :param row: Int - The row of the center cell
    :param col: Int - The column of the center cell
    :param rows: Int - The number of rows that the Epedemic NN grid has
    :param cols: Int - The number of columns that the Epedemic NN grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Epedemic NN grid
    :return: Int - The number of infected cells surrounding the cell at grid[row][cell]
    """

    infected_sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Make sure to count the center cell located at grid[row][col]
            if not (i == 0 and j == 0):
                # Using the modulo operator (%) the grid wraps around
                infected_sum += 1 if (grid[((row + i) % rows)][((col + j) % cols)] == 1) else 0
    return infected_sum


def grid_changing(rows, cols, grid, next_grid):
    """
    Checks to see if the current generation Epedemic NN grid is the same as the next generation Epedemic NN grid.
    :param rows: Int - The number of rows that the Epedemic NN grid has
    :param cols: Int - The number of columns that the Epedemic NN grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Epedemic NN grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Epedemic NN
    grid
    :return: Boolean - Whether the current generation grid is the same as the next generation grid
    """

    for row in range(rows):
        for col in range(cols):
            # If the cell at grid[row][col] is not equal to next_grid[row][col]
            if not grid[row][col] == next_grid[row][col]:
                return True
    return False


def firing_count(rows, cols, grid, num):
    """
    counts number of cells in grid with value num
    """
    sum = 0

    for i in range(rows):
        sum += grid[i].count(num)

    return sum


beta = 0.01 #beta set as global value for no reason what so ever

def run_game():
    """
    Asks the user for input to setup the Epedemic NN to run for a given number of generations.
    """
    case = 3 #remnant from earlier used code

    clear_console()
    print(f'Enter 0 for continous simulation, 1 for statistics, 2 for plots:\n')
    runtype = int(input())

    #set variables
    p = 0.05 #p is set to 0.05 as base for this assignment
    gamma = [0.9, 0.88, 0.86, 0.84, 0.82, 0.8, 0.75] #interesting values for gamma
    # Get the number of rows and columns for the Epedemic NN grid
    rows = 40
    cols = rows #N*N grid

    clear_console()
    
    # Run Epedemic NN sequence
    if runtype == 0:
        resize_console(rows, cols)

        generations = 500 #visual simulation is capped at this number of generations, can be changed

        # Create the initial random Epedemic NN grids
        current_generation = create_initial_grid(rows, cols, p, case)
        next_generation = create_initial_grid(rows, cols, p, case)

        gen = 1
        for gen in range(1, generations + 1):
            print_grid(rows, cols, current_generation, gen)#print grid 
            create_next_grid(rows, cols, current_generation, next_generation, gamma[2], case) #create next grid

            time.sleep(1 / 5.0)
            current_generation, next_generation = next_generation, current_generation #assign current gen as next gen

        print_grid(rows, cols, current_generation, gen)
        return input("<Enter> to exit or r to run again: ")
    elif runtype == 1:
        iter = 5 #number of iterations for results to be averaged over
        generations = 2000 #generations
        gamma = [0.5, 0.6, 0.7, 0.77, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.87, 0.9] #interesting values of gamma
        beta1 = [0, 0.005, 0.01, 0.015, 0.02, 0.035, 0.05, 0.075, 0.1 ,0.3] #interesting values of beta
        alive = [0]*len(beta1) #list for which generation disease dies on
        for j in range(0, len(beta1)): #iterate over length of beta1 list
            print(f'iteration {j}') #print for the sake of my sanity

            #since beta is otherwise applied globally. gamma is now fixed. should be commented away if gamma is to be examined instead
            global beta 
            beta = beta1[j]
            for k in range(iter): #run simulations iter times and average results
                current_generation = create_initial_grid(rows, cols, p, case)
                next_generation = create_initial_grid(rows, cols, p, case)
                gen = 1
                for gen in range(1, generations + 1):
                    create_next_grid(rows, cols, current_generation, next_generation, gamma[4], case)
                    current_generation, next_generation = next_generation, current_generation
                    if not firing_count(rows, cols, current_generation, 1): #if no cells are infected for loop stops
                        break
                print(f'gen is {gen}')
                alive[j] += gen #generation of disease dying out if it has done so
            alive[j] /= iter #normalize
            print(f'alive is {alive[j]}')
        #plt.plot(gamma, alive) #plots for gamma
        plt.plot(beta1, alive) #plots for beta
        #plt.xlabel("Gamma")
        plt.xlabel("Beta")
        plt.ylabel("Generation")
        plt.title("Generations to which disease has survived with gamma = 0.8")
        plt.show()
        return input("<Enter> to exit or r to run again: ")

    elif runtype == 2:
        generations = 1000
        iter = 3
        for i in range(0, 1):
            #create lists tracking the evolution of states over generations
            sus = [0]*generations 
            infected = [0]*generations
            immune = [0]*generations
            dead = [0]*generations
            for j in range(iter):
                print(f'iteration {j}') #prints for the sake of my sanity
                current_generation = create_initial_grid(rows, cols, p, case)
                next_generation = create_initial_grid(rows, cols, p, case)
                gen = 1
                for gen in range(1, generations + 1):
                    create_next_grid(rows, cols, current_generation, next_generation, 0.7, case) #gamma is changed here as you with
                    current_generation, next_generation = next_generation, current_generation
                    sus[gen-1] += firing_count(rows, cols, current_generation, 0) #number of suceptible cells for each timestep
                    infected[gen-1] += firing_count(rows, cols, current_generation, 1) #number of infected cells for each timestep
                    immune[gen-1] += firing_count(rows, cols, current_generation, 2) #number of immune cells for each timestep
                    dead[gen-1] += firing_count(rows, cols, current_generation, 3)#number of dead cells for each timestep
            sus[:] = [x/iter for x in sus] #normalize
            infected[:] = [x/iter for x in infected] #normalize
            immune[:] = [x/iter for x in immune] #normalize
            dead[:] = [x/iter for x in dead] #normalize

            #plots
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


# Start the Epedemic NN
run = "r"
while run == "r":
    out = run_game()
    run = out