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


def create_initial_grid(rows, cols):
    """
    Creates a random list of lists that contains 1s and 0s to represent the cells in A Firing Brain.
    :param rows: Int - The number of rows that the A Firing Brain grid will have
    :param cols: Int - The number of columns that the A Firing Brain grid will have
    :return: Int[][] - A list of lists containing 1s for firing cells and 0s for ready cells
    """

    grid = []
    for row in range(rows):
        grid_rows = []
        for col in range(cols):
            # Generate a random number and based on that decide whether to add a live or dead cell to the grid
            grid_rows += [0]
        grid += [grid_rows]
    randboredx = random.randint(0,len(grid_rows)-1)
    randboredy = random.randint(0,len(grid)-1)
    randsharedx = random.randint(0,len(grid_rows)-1)
    randsharedy = random.randint(0,len(grid)-1)
    grid[randsharedx][randsharedy] = 1
    grid[randboredx][randboredy] = 2
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
            else:
                output_str += "_ "
        output_str += "\n\r"
    print(output_str, end=" ")


def create_next_grid(rows, cols, grid, next_grid, p, q, r):
    """
    Resting = 0
    Sharer = 1
    Bored = 2
    """

    for row in range(rows):
        for col in range(cols):
            #Resting
            if grid[row][col] == 0:
                if random.random()>p:
                    next_grid[row][col] = 0
                else:
                    next_grid[row][col] = 1
            #Sharer
            elif grid[row][col] == 1:
                if random.random()>q:
                    next_grid[row][col] = 1
                else:
                    randx = random.randint(-1,1)
                    randy = random.randint(-1,1)
                    p_col = (col+randx)%cols
                    p_row = (row+randy)%rows
                    if grid[p_row][p_col] == 0:
                        next_grid[p_row][p_col] = 1
                        next_grid[row][col] = 1
                    elif grid[p_row][p_col] == 2:
                        next_grid[row][col] = 2
                    else:
                        next_grid[row][col] = 1
            #Bored
            else:
                if random.random()>r:
                    next_grid[row][col] = 2
                else:
                    randx = random.randint(-1,1)
                    randy = random.randint(-1,1)
                    p_col = (col+randx)%cols
                    p_row = (row+randy)%rows
                    if grid[p_row][p_col] == 0:
                        next_grid[row][col] = 0
                    else:
                        next_grid[row][col] = 2



def get_firing_neighbors(row, col, rows, cols, grid):
    """
    Counts the number of live cells surrounding a center cell at grid[row][cell].
    :param row: Int - The row of the center cell
    :param col: Int - The column of the center cell
    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
    :return: Int - The number of live cells surrounding the cell at grid[row][cell]
    """

    life_sum = 0
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Make sure to count the center cell located at grid[row][col]
            if not (i == 0 and j == 0):
                # Using the modulo operator (%) the grid wraps around
                life_sum += 1 if (grid[((row + i) % rows)][((col + j) % cols)] == 1) else 0
    return life_sum


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

def state_count(rows, cols, grid, num):
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


def run_game():
    """
    Asks the user for input to setup the A Firing Brain to run for a given number of generations.
    """

    p = 0.007
    q = 0.07
    r = 0.04

    #p = 0.007
    #q = 0.07
    #r = 0.04

    #p = 0.005
    #q = 0.1
    #r = 0.03

    # Get the number of rows and columns for the A Firing Brain grid
    rows = 40
    cols = 40
    clear_console()

    # Get the number of generations that the A Firing Brain should run for
    
    resize_console(rows, cols)

    if 0 == 0:
        generations = 2500
        # Create the initial random A Firing Brain grids
        current_generation = create_initial_grid(rows, cols)
        next_generation = create_initial_grid(rows, cols)

        # Run A Firing Brain sequence
        gen = 1
        for gen in range(1, generations + 1):
            print_grid(rows, cols, current_generation, gen)
            create_next_grid(rows, cols, current_generation, next_generation,p,q,r)
            time.sleep(1 / 150.0)
            current_generation, next_generation = next_generation, current_generation

        print_grid(rows, cols, current_generation, gen)
        return input("<Enter> to exit or r to run again: ")
    """
    elif runtype == 2:
        generations =1000
        firing = [0]*generations
        iterations = 100
        for i in range(iterations):
            print(f"iteration {i}\n")
            current_generation = create_initial_grid(rows, cols)
            next_generation = create_initial_grid(rows, cols)
            # Run A Firing Brain sequence
            for gen in range(1, generations + 1):
                create_next_grid(rows, cols, current_generation, next_generation)
                current_generation, next_generation = next_generation, current_generation
                firing[gen-1] += firing_count(rows, cols, current_generation)
                #firing[gen-1] += current_generation.count(1)
                #print(f'current count = {current_generation.count(1)}\n')
        #firing /= 100
        firing = [i/iterations for i in firing]
        plt.plot(range(500), firing)
        plt.show()



        return input("<Enter> to exit or r to run again: ")"""

    


# Start the A Firing Brain
run = "r"
while run == "r":
    out = run_game()
    run = out