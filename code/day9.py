import utils
import numpy as np

inputfile = utils.INPUT_DIR / "day9.txt"

with open(inputfile, "r") as fh:
    lines = fh.readlines()

# Initialization: tail begins at the origin
head_pos = [0, 0]
tail_pos = [0, 0]

def adjust_tail(head, tail):
    # head and tail are two (x,y) tuples indicating the
    # position of the head and tail respectively.
    # returns a boolean indicating if the tail moved, and the
    # new position of the tail
    moved = True
    if abs(head[0] - tail[0]) > 1 and abs(head[1] - tail[1]) > 1:
        tail[0] = head[0] + int((tail[0]-head[0])/abs(tail[0]-head[0]))
        tail[1] = head[1] + int((tail[1]-head[1])/abs(tail[1]-head[1]))
    elif abs(head[0] - tail[0]) > 1:
        tail[1] = head[1]
        tail[0] = head[0] + int((tail[0]-head[0])/abs(tail[0]-head[0]))
    elif abs(head[1] - tail[1]) > 1:
        tail[0] = head[0]
        tail[1] = head[1] + int((tail[1]-head[1])/abs(tail[1]-head[1]))
    else:
        # close enough, no move
        moved = False
    return moved, tail

directions = {"L": (0, -1), "R": (0, 1), "U": (1, 1), "D": (1, -1)}

# Part 1
tail_visited = {(0, 0): 1}
for line in lines:
    direction, steps = line.strip().split(" ")
    steps = int(steps)
    for i in range(steps):
        coord, value = directions[direction]
        head_pos[coord] += value
        moved, tail_pos = adjust_tail(head_pos, tail_pos)
        if moved:
            tail_pos_tuple = tuple(tail_pos)
            if tail_pos_tuple in tail_visited:
                tail_visited[tail_pos_tuple] += 1
            else:
                tail_visited[tail_pos_tuple] = 1

print(f"[Part 1] Positions visited by tail at least once: {len(tail_visited)}")

# Part 2
N_knots = 10
tail_visited = {(0, 0): 1}
positions = [[0, 0] for i in range(N_knots)] # 0 is head, all begin at origin
for line in lines:
    direction, steps = line.strip().split(" ")
    steps = int(steps)
    coord, value = directions[direction]
    for i in range(steps):
        # Adjust head position
        positions[0][coord] += value
        #print(positions)
        # Adjust each know from 1 to 9 (tail)
        for j in range(1, N_knots):
            moved, positions[j] = adjust_tail(positions[j-1], positions[j])
            if j == N_knots - 1 and moved:
                tail_pos_tuple = tuple(positions[j])
                if tail_pos_tuple in tail_visited:
                    tail_visited[tail_pos_tuple] += 1
                else:
                    tail_visited[tail_pos_tuple] = 1

print(f"[Part 2] Positions visited by tail at least once: {len(tail_visited)}")
