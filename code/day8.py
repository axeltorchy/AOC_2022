import utils
import numpy as np

inputfile = utils.INPUT_DIR / "day8.txt"

with open(inputfile, "r") as fh:
    lines = fh.readlines()

N = len(lines[0].strip())

trees = np.zeros((N,N), dtype=np.int8)

for i in range(len(lines)):
    line = lines[i].strip()
    for j in range(len(line)):
        trees[i][j] = line[j]

visible = np.zeros((N, N), dtype=np.int8)
# From left (0)
for i in range(0,N):
    maximum = -1
    for j in range(0,N):
        if trees[i][j] > maximum:
            visible[i][j] += 1
            maximum = trees[i][j]

# From right (1)
for i in range(0,N):
    maximum = -1
    for j in range(N-1, -1, -1):
        if trees[i][j] > maximum:
            visible[i][j] += 1
            maximum = trees[i][j]

# From top (2)
for j in range(0,N):
    maximum = -1
    max_idx = 0
    for i in range(0,N):
        if trees[i][j] > maximum:
            visible[i][j] += 1
            maximum = trees[i][j]

# From bottom (3)
for j in range(0,N):
    maximum = -1
    max_idx = N-1
    for i in range(N-1, -1, -1):
        if trees[i][j] > maximum:
            visible[i][j] += 1
            maximum = trees[i][j]

total_visible = 0
for i in range(N):
    for j in range(N):
        if visible[i][j] > 0:
            total_visible += 1

print(f"Total visible trees: {total_visible}")

# Part 2
scenic_score = np.ones((N, N), dtype=np.int32)
for i in range(N):
    for j in range(N):
        # For each position, compute the scenic score
        # - LEFT
        if j == 0:
            scenic_score[i][j] = 0
        else:
            local_score = 0
            for k in range(j-1, -1, -1):
                local_score += 1
                if trees[i][k] >= trees[i][j]:
                    break
            scenic_score[i][j] *= local_score
                
        # - RIGHT
        if j == N-1:
            scenic_score[i][j] = 0
        else:
            local_score = 0
            for k in range(j+1, N, 1):
                local_score += 1
                if trees[i][k] >= trees[i][j]:
                    break
            scenic_score[i][j] *= local_score

        # - UP
        if i == 0:
            scenic_score[i][j] = 0
        else:
            local_score = 0
            for k in range(i-1, -1, -1):
                local_score += 1
                if trees[k][j] >= trees[i][j]:
                    break
            scenic_score[i][j] *= local_score

        # - DOWN
        if i == N-1:
            scenic_score[i][j] = 0
        else:
            local_score = 0
            for k in range(i+1, N, 1):
                local_score += 1
                if trees[k][j] >= trees[i][j]:
                    break
            scenic_score[i][j] *= local_score

print(f"Maximum scenic score: {np.amax(scenic_score)}")