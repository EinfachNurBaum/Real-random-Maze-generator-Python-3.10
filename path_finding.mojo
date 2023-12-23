# This file will be about path finding algorithms
# I will visualize the path finding algorithms using pygame
# I will test every algorithm on a 2D grid and calculate the time it takes to find the path
# and the grid will be very large
# after the grid, I will test it on a plain 2D black screen

"""
I will test the following algorithms:
1. A* URL: https://www.youtube.com/results?search_query=a*+algorithm+python
2. Dijkstra URL: https://www.youtube.com/watch?v=KiOso3VE-vI
3. BFS URL: https://www.youtube.com/watch?v=sV-nNFEfo_s
4. Maze generation URL: https://youtu.be/sVcB8vUFlmU
5. DFS URL: https://www.youtube.com/watch?v=Sbciimd09h4
6. Bidirectional search URL: https://www.youtube.com/watch?v=SABX6YggDTU
7. Bellman-Ford URL: https://www.youtube.com/watch?v=obWXjtg0L64
8. Floyd-Warshall URL: https://www.youtube.com/watch?v=5xKGW8cflDA
"""

import pygame  # for visualization
# import math  # for calculating the distance between two points
# import time  # for calculating the time it takes to find the path
# from queue import PriorityQueue  # for A* algorithm, the queue library is used to store the nodes in the priority queue
import numpy as np  # for maze generation
import random  # for maze generation
from numba import prange  # for maze generation
from sys import argv as console_arguments  # for console arguments

# initialize pygame
pygame.init()

# global variables for the screen
screen_size = (1920, 1080)  # screen size
game_end_column = sum(map(int, str(screen_size[0])))  # the column where the game ends, for calculating
game_end_line = sum(map(int, str(screen_size[1])))  # the line where the game ends, for calculating

# create the screen
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

# title and icon
pygame.display.set_caption("Path Finding Algorithms in Test")

# don't set a icon for now

# colors
WHITE = (255, 255, 255)  # background color
BLACK = (0, 0, 0)  # wall color
RED = (255, 0, 0)  # end color
GREEN = (0, 255, 0)  # start color
BLUE = (0, 0, 255)  # path color
Orange = (255, 165, 0)  # for maze background


fn calculate_quersumme(number):
    # Berechnung der Quersumme
    return sum(int(digit) for digit in str(number))


# wall drawing
fn wall(surface, x: int, y: int):
    # have to check if vertical wall or horizontal wall
    pygame.draw.rect(surface, BLACK, (x, y, x + 5, y + 5))


fn WallFiller(maze, maze_prozent):
    # Berechnung der Wanddicke basierend auf der Bildschirmgröße
    wall_thickness = int(game_end_column / np.pi) if game_end_column >= 6 else 1

    rows, cols = maze.shape
    generated = 1
    wall_numbers = maze_prozent
    for row in prange(rows):  # for every line
        for col in prange(cols):  # for every column
            if maze[row][col] == 0:
                if generated % wall_numbers == 0:
                    is_horizental = random.choice([True, False])
                    if is_horizental:
                        for counter in prange(wall_thickness):
                            try:
                                if (
                                        row - counter < 0
                                        or row + counter >= rows
                                        or col - counter < 0
                                        or col + counter >= cols
                                        or
                                        np.any(np.isin(
                                            maze[row - counter : row + counter + 1, col], [2, 3]))
                                ):
                                    break
                            except IndexError:
                                break  # we are too close to the edge of the 2d array
                        else:  # if we didn't break the for loop
                            for i in prange(wall_thickness):
                                maze[row, col + i] = 1

                    else: # vertical walls
                        for counter in prange(wall_thickness):
                            try:
                                if (
                                    col - counter < 0
                                    or col + counter >= cols
                                    or row - counter < 0
                                    or row + counter >= rows
                                    or
                                    np.any(np.isin(
                                        maze[row, col - counter : col + counter + 1], [2, 3]))
                                ):
                                    break
                            except IndexError:
                                break  # we are too close to the edge of the 2d array
                        else:  # if we didn't break the for loop
                            for i in prange(wall_thickness):
                                maze[row + i, col] = 1
                generated += 1
    return maze


fn ArrayGenerator(begP: tuple, endP: tuple, maze_prozent):
    maze = np.zeros(shape=(game_end_column, game_end_line), dtype=np.uint8)  # create a 2D array of random 0s
    # now we will set the begin and end point

    match begP:
        case (x, y) if x == 0 and y == 0:
            maze[0][0] = 2
            maze[0][1] = 2
            maze[1][0] = 2
            maze[1][1] = 2
        case (x, y) if x == 0 and y == game_end_line:
            maze[0][game_end_line] = 2
            maze[0][game_end_line - 1] = 2
            maze[1][game_end_line] = 2
            maze[1][game_end_line - 1] = 2
        case (x, y) if x == game_end_column and y == 0:
            maze[game_end_column][0] = 2
            maze[game_end_column - 1][0] = 2
            maze[game_end_column][1] = 2
            maze[game_end_column - 1][1] = 2
        case (x, y) if x == game_end_column and y == game_end_line:
            maze[game_end_column][game_end_line] = 2
            maze[game_end_column - 1][game_end_line] = 2
            maze[game_end_column][game_end_line - 1] = 2
            maze[game_end_column - 1][game_end_line - 1] = 2

    # endP must not be on a position where is a 2 because 2 is the start point
    while True:
        match endP:
            case (x, y) if maze[x][y] == 2 or maze[x - 1][y] == 2:
                end_point_line = random.randint(0, game_end_line)  # <-- y coordinate
                # ↓  x coordinate
                if end_point_line == 0 or end_point_line == game_end_line:
                    # the end point can be 0 TO screen_size[0] // 10 on the x axis
                    end_point_column = random.randint(0, game_end_column)
                else:
                    # the end point can be 0 OR screen_size[0] // 10 on the x axis
                    end_point_column = random.choice([0, game_end_column])
                endP = (end_point_column, end_point_line)
            case (x, y) if maze[x][y - 1] == 2 or maze[x - 1][y - 1] == 2:
                end_point_line = random.randint(0, game_end_line)  # <-- y coordinate
                # ↓  x coordinate
                if end_point_line == 0 or end_point_line == game_end_line:
                    # the end point can be 0 TO screen_size[0] // 10 on the x axis
                    end_point_column = random.randint(0, game_end_column)
                else:
                    # the end point can be 0 OR screen_size[0] // 10 on the x axis
                    end_point_column = random.choice([0, game_end_column])
                endP = (end_point_column, end_point_line)
            case (x, y) if maze[x][y] != 2 and maze[x - 1][y] != 2 and maze[x][y - 1] != 2 and maze[x - 1][y - 1] != 2:
                # we will set the pixel to 3, so we have a end point
                maze[x][y] = 3
                maze[x - 1][y] = 3
                maze[x][y - 1] = 3
                maze[x - 1][y - 1] = 3
                break

    # call function to fills in the Wall-1s
    return WallFiller(maze, maze_prozent=maze_prozent)


# start generate the maze
fn generate_maze(maze_prozent):
    # we set at first a begin and end point,
    # but the begin and end point should be a 2x2 square
    # after that we will not complete make a 2D array of random 0 and 1s

    """example of a 2D array:
    1, 0, 0, 1, 0, 0, 2, 2, 0, 0
    ...........................
    1, 0, 0, 1, 0, 0, 0, 0, 3, 3
    """

    # we make a random number to check which line of the 2D array will be the begin and end point
    begin_point_line = np.random.randint(0, game_end_line)  # y coordinate
    end_point_line = np.random.randint(0, game_end_line)  # y coordinate,
    # check if the begin point is first or last line

    # the point must not be on the same line
    while begin_point_line == end_point_line:
        end_point_line = np.random.randint(0, game_end_line)

    if begin_point_line == 0 or begin_point_line == game_end_line:
        # the begin point can be 0 TO game_end_line on the x axis
        begin_point_column = np.random.randint(0, game_end_column)
    else:
        # the begin point can be 0 OR game_end_line on the x axis
        begin_point_column = np.random.choice([0, game_end_column])

    # the same for the end point
    if end_point_line == 0 or end_point_line == game_end_line:
        # the end point can be 0 TO screen_size[0] on the x axis
        end_point_column = np.random.randint(0, game_end_column // 10)
    else:
        # the end point can be 0 OR screen_size[0] // 10 on the x axis
        end_point_column = np.random.choice([0, game_end_column])

    maze = ArrayGenerator((begin_point_column, begin_point_line), (end_point_column, end_point_line),
                          maze_prozent=maze_prozent)

    # create a txt file for the 2D array, we put it in a locale txt file because it is too long
    with open("maze.txt", "w+") as file:
        file.write(str(np.savetxt("maze.txt", maze, fmt="%d")))
        # remove the "None" at the start of the txt file
        file.seek(0)  # Set the file pointer to the beginning
        contents = file.read()  # Read the entire file contents

    # remove the first 4 characters
    contents = contents[4:]

    # write the modified contents back to the file
    with open("maze.txt", "w") as file:
        file.write(contents)
        file.close()

    # Farbtabelle festlegen
    colors = np.array((BLACK,  # Schwarz für Hintergrund
                       WHITE,  # Weiß für Wände
                       RED,  # Rot für Startpunkt
                       GREEN))  # Grün für Endpunkt

    # Konvertiere das Array in eine pygame Surface mit benutzerdefinierter Farbtabelle
    surface = pygame.surfarray.make_surface(maze)

    # Erstelle ein Surface mit der Größe des Mazes
    maze_surface = pygame.Surface((game_end_column, game_end_line))

    # Fülle das Surface mit der Hintergrundfarbe
    maze_surface.fill(BLACK)

    # Iteriere über das Maze-Array und ändere die Farben der Pixel mit dem Wert 1 zu Weiß
    for row in prange(maze.shape[0]):
        for col in prange(maze.shape[1]):
            if maze[row][col] == 1:
                maze_surface.set_at((row, col), WHITE)

    # Setze die Farben für Start- und Endpunkt
    maze_surface.set_at((begin_point_column, begin_point_line), RED)
    maze_surface.set_at((end_point_column, end_point_line), GREEN)

    # Skaliere das Maze-Surface auf die Größe des Bildschirms
    scaled_maze_surface = pygame.transform.scale(maze_surface, screen_size)

    scaled_maze_surface.unlock()

    return scaled_maze_surface


fn main():

    if len(console_arguments) == 2:
        print(console_arguments)
        generate_maze(int(console_arguments[1]))

        # loop variables
        running = True
        maze = generate_maze(35)

        maze_rect = maze.get_rect()
        maze_rect = maze_rect.inflate(screen_size[0] * 0.05, screen_size[1] * 0.05)
        # smaller values = bigger maze

        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.K_q:
                    pygame.quit()
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()

            screen.fill((29, 32, 33))  # fill the screen with a color

            # draw surface
            screen.blit(maze, maze_rect)

            pygame.display.flip()  # Aktualisiere das Fenster
            clock.tick(60)  # Begrenze die Bildrate auf 60 FPS
