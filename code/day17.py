import utils
import re
import numpy as np
from time import time

example = True
inputfile = utils.INPUT_DIR / "day17.txt"
if example:
    inputfile = utils.INPUT_DIR / "day17_example.txt"

with open(inputfile, "r") as fh:
    moves = fh.readline()
N_moves = len(moves)

print(moves, N_moves)

# Rock are given line by line, from bottom to top.
# Horizontally, they are represented on 7 bits, in their initial state
# i.e. two blocks away from the left wall. 
rock_shapes = [
    [0b0011110],
    [0b0001000, 0b0011100, 0b0001000],
    [0b0011100, 0b0000100, 0b0000100],
    [0b0010000, 0b0010000, 0b0010000, 0b0010000],
    [0b0011000, 0b0011000]
]

# TOWER = set of rocks from bottom to top, each element is a row of
# 7-bit numbers
tower = []
tower_size = 0
count_moves = 0
count_rocks = 0
while True:
    # A new rock begins falling
    rock = rock_shapes[count_rocks % len(rock_shapes)]
    highest_rock = len(tower)
    # Current height of the lowest row of the rock
    current_height = highest_rock + 3
    
    while True:
        # The rock is falling
        # 1. A jet of hot gas pushes the rock
        move = moves[count_moves % N_moves]
        if move == "<":
            # tries to move left if no left wall and if no rock
            for i in range(len(rock)):
                if rock[i] & 0b1000000 > 0: # left wall
                    break
                # If there is a rock left
                elif len(tower) > current_height + i and tower[current_height + i] & (rock[i] << 1) > 0:
                    # rock on left
                    break
            else:
                # did not break: no obstacle at all on left
                rock = [row << 1 for row in rock]

        elif move == ">":
            # tries to move right if no right wall and if no rock on right
            for i in range(len(rock)):
                if rock[i] & 0b0000001 > 0: # right wall
                    break
                # If there is a rock right
                elif len(tower) > current_height + i and tower[current_height + i] & (rock[i] >> 1) > 0:
                    # rock on right
                    break
            else:
                # did not break: no obstacle at all on right
                rock = [row >> 1 for row in rock]
        
        count_moves += 1
        # 2. Check if rock may fall 1 unit
        ## first case: tower is small enough, no more check: fall
        if len(tower) < current_height:
            current_height -= 1
            continue
        ## otherwise, check if there is a rock below
        else:
            for i in range(len(rock)):
                if current_height == 0: # floor below
                    print("Rock reached floor")
                    break
                elif len(tower) >= current_height + i and tower[current_height + i -1] & rock[i] > 0:
                    # rock below i-th row of rock
                    break
            else:
                # did not break: no rock below
                current_height -= 1
                continue
            
            # otherwise, rock (or floor) below: rock comes to rest
            # and a new rock begins falling
            for i in range(len(rock)):
                if len(tower) > current_height + i:
                    tower[current_height + i] |= rock[i]
                else:
                    tower.append(rock[i])
                    tower_size += 1

            break
    
    count_rocks += 1

    if count_rocks == 2022:
        break

print(f"{count_rocks} have fallen, current size: {len(tower)}")
# for i in range(len(tower)):
#     print(format(tower[-i-1], '07b'))