
from collections import deque
import utils

inputfile = utils.INPUT_DIR / "day5.txt"

with open(inputfile, "r") as fh:
    lines = fh.readlines()

# Initialization
first_index_moves = 0
count = 0
nb_stacks = 0
for line in lines:
    line = line.strip()
    
    if line[0] == "[":
        count += 1
        continue
    nb_stacks = int(line.split()[-1])
    first_index_moves = count + 2
    break

print(f"Found {nb_stacks} stacks, beginning moves " \
    f"on row {first_index_moves}.")

stacks = [deque() for i in range(nb_stacks)]
for i in range(first_index_moves - 2):
    line_nb = first_index_moves - 3 - i
    for j in range(nb_stacks):
        char_pos = 4*j + 1
        char = lines[line_nb][char_pos]
        if char != " ":
            stacks[j].append(char)

# Processing moves
def process_moves(stacks, lines, keep_order=False):
    for move in lines[first_index_moves:]:
        move = move.split(" ")
        nb_moves = int(move[1])
        src, dst = int(move[3]) -1, int(move[5]) - 1
        crates_to_move = []
        for i in range(nb_moves):
            crate = stacks[src].pop()
            crates_to_move.append(crate)
        my_iter = range(nb_moves)
        if keep_order:
            my_iter = reversed(my_iter)
        for i in my_iter:
            stacks[dst].append(crates_to_move[i])

# False for part 1, True for part 2
process_moves(stacks, lines, keep_order=True)
final_result = "".join([stacks[i][-1] for i in range(nb_stacks)])

print(final_result)