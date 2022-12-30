import utils
import numpy as np
from time import time

example = True
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

for line in lines:
    cube = [int(n) for n in line.strip().split(",")]
    cube.append(6)
    cubes.append(cube)

    for i in range(len(cubes)-1):
        if distance(cubes[i][:3], cubes[len(cubes)-1][:3]) == 1:
            cubes[i][3] -= 1
            cubes[len(cubes)-1][3] -= 1

total_surface = 0
for cube in cubes:
    total_surface += cube[3]

print("Total surface:", total_surface)