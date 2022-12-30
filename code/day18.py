import utils
import numpy as np
from time import time
from scipy.spatial import Delaunay

example = False
inputfile = utils.INPUT_DIR / "day18.txt"
if example:
    inputfile = utils.INPUT_DIR / "day18_example.txt"

with open(inputfile, "r") as fh:
    lines = fh.readlines()

def distance(cube1, cube2):
    # cube1 and cube2 are 3-uples or lists of length 3.
    # cubes are directly adjacent if the distance is 1.
    return sum([abs(cube1[i] - cube2[i]) for i in range(3)])

cubes = []
cubes_hash = set()
surfaces = []

for line in lines:
    cube = tuple([int(n)+1 for n in line.strip().split(",")])
    cubes_hash.add(cube)
    surfaces.append(6)
    cubes.append(cube)

    for i in range(len(cubes)-1):
        if distance(cubes[i], cubes[len(cubes)-1]) == 1:
            surfaces[i] -= 1
            surfaces[len(cubes)-1] -= 1

total_surface = 0
for surface in surfaces:
    total_surface += surface

print("Total surface:", total_surface)

hull = Delaunay(cubes)
extreme_coord = [int(x) for x in hull.min_bound], [int(x) for x in hull.max_bound]
min_x, max_x = extreme_coord[0][0], extreme_coord[1][0]
min_y, max_y = extreme_coord[0][1], extreme_coord[1][1]
min_z, max_z = extreme_coord[0][2], extreme_coord[1][2]
#print(extreme_coord)
grid = np.zeros((max_x+1, max_y+1, max_z+1), dtype=int)

def color_grid(grid, starting_point):
    # starting point is a 3-uple
    # 0 = air inside or not processed yet
    # 1 = lava
    # 2 = air outside
    x, y, z = starting_point
    if starting_point in cubes_hash:
        grid[x][y][z] = 1
        return
    
    grid[x][y][z] = 2
    # color neighbors recursively
    if x > 0 and grid[x-1][y][z] == 0:
        color_grid(grid, (x-1, y, z))
    if x < max_x and grid[x+1][y][z] == 0:
        color_grid(grid, (x+1, y, z))
    if y > 0 and grid[x][y-1][z] == 0:
        color_grid(grid, (x, y-1, z))
    if y < max_y and grid[x][y+1][z] == 0:
        color_grid(grid, (x, y+1, z))
    if z > 0 and grid[x][y][z-1] == 0:
        color_grid(grid, (x, y, z-1))
    if z < max_z and grid[x][y][z+1] == 0:
        color_grid(grid, (x, y, z+1))
    
bubbles = []

import sys
sys.setrecursionlimit(10000)
print("Recursion limit:", sys.getrecursionlimit())

color_grid(grid, (0, 0, 0))

for x in range(max_x):
    for y in range(max_y):
        for z in range(max_z):
            if (x,y,z) not in cubes_hash and grid[x][y][z] == 0:
                bubbles.append((x,y,z))

# compute number of surface units to substract
bubble_surfaces = [6 for i in range(len(bubbles))]
for i in range(len(bubbles)):
    for j in range(i):
        if distance(bubbles[i], bubbles[j]) == 1:
            bubble_surfaces[i] -= 1
            bubble_surfaces[j] -= 1

total_surface_bubbles = 0
for surface in bubble_surfaces:
    total_surface_bubbles += surface

print("Bubble surface:", total_surface_bubbles)

print("Total exterior surface:", total_surface - total_surface_bubbles)
