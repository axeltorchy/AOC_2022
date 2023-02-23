import utils
import numpy as np
import re

example = False
inputfile = utils.INPUT_DIR / "day22.txt"
if example:
    print("Playing example.")
    inputfile = utils.INPUT_DIR / "day22_example.txt"

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

line_nb = 1
instructions = None

extremities = {
    'line_left': {},
    'column_up': {}
}

tiles = {}
current_position = None

for line in lines:
    # print(f"Processing line {line_nb}: '{line.rstrip()}'")
    if len(line) == 1:
        # empty line between map and instructions
        continue
    elif line[0] in [" ", ".", "#"]:
        col_nb = 1
        for tile in line.rstrip():
            if tile != " ":
                if current_position is None:
                    # Setting initial position
                    current_position = (line_nb, col_nb)

                if line_nb not in extremities['line_left']:
                    extremities['line_left'][line_nb] = col_nb
                if col_nb not in extremities['column_up']:
                    extremities['column_up'][col_nb] = line_nb
                tiles[(line_nb, col_nb)] = {
                    'blocked': True if tile == "#" else False,
                    'up': None,
                    'down': None,
                    'left': None,
                    'right': None
                }
                if (line_nb - 1, col_nb) in tiles:
                    tiles[(line_nb - 1, col_nb)]['down'] = (line_nb, col_nb)
                    tiles[(line_nb, col_nb)]['up'] = (line_nb - 1, col_nb)
                if (line_nb, col_nb - 1) in tiles:
                    tiles[(line_nb, col_nb - 1)]['right'] = (line_nb, col_nb)
                    tiles[(line_nb, col_nb)]['left'] = (line_nb, col_nb - 1)
            elif tile == " ":
                pass
            else:
                print(f"Should not happen, line {line_nb}, col. {col_nb}: '{tile}'")
            col_nb += 1

        # map tiles
    else:
        instructions = line.strip()
    line_nb += 1

# Completing tiles neighbors
for tile in tiles:
    line_nb, col_nb = tile
    if tiles[tile]['right'] is None:
        left_extremity = extremities['line_left'][line_nb]
        tiles[tile]['right'] = (line_nb, left_extremity)
        tiles[(line_nb, left_extremity)]['left'] = (line_nb, col_nb)

    if tiles[tile]['down'] is None:
        up_extremity = extremities['column_up'][col_nb]
        tiles[tile]['down'] = (up_extremity, col_nb)
        tiles[(up_extremity, col_nb)]['up'] = (line_nb, col_nb)

print(f"Processed {len(tiles)} tiles.")
print(instructions)
instructions_list = re.split('(\d+)', instructions)[1:-1]
print("Instructions:", instructions_list)

# Tracing the path
orientations = {
    0: 'right',
    1: 'down',
    2: 'left',
    3: 'up'}

# Initial orientation is facing right
orientation = 0

for instruction in instructions_list:
    print("Processing instruction", instruction)
    if instruction == "R":
        # turn clockwise
        orientation = (orientation + 1) % 4
    elif instruction == "L":
        # turn counter-clockwise
        orientation = (orientation - 1) % 4
    else:
        # (try to) move in the current direction
        # 'instruction' is the number of steps
        for i in range(int(instruction)):
            neighbor = tiles[current_position][orientations[orientation]]
            if tiles[neighbor]['blocked']:
                break
            else:
                current_position = neighbor

print("Final position:", current_position)
print("Final orientation:", orientation)
print("Password is:", 1000 * current_position[0] + 4 * current_position[1] + orientation)