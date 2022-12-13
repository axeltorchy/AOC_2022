import utils
import string
import math
from queue import PriorityQueue

inputfile = utils.INPUT_DIR / "day12_example.txt"
inputfile = utils.INPUT_DIR / "day12.txt"

# Set letter values
letters = {}
for index, letter in enumerate(string.ascii_lowercase):
   letters[letter] = index + 1
letters['S'] = letters['a']
letters['E'] = letters['z']

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

N_lines = len(lines)
N_columns = len(lines[0]) - 1
starting_point = None
destination_point = None
x = 0

# Initialize graph
neighbors = {}
for i in range(N_lines):
    for j in range(N_columns):
        #print(f"[{i},{j}] Letter: {lines[i][j]}")
        letter = lines[i][j]
        if letter == 'S':
            print(f"Found starting point S: ({i}, {j})")
            starting_point = (i, j)
        elif letter == 'E':
            print(f"Found destination point E: ({i}, {j})")
            destination_point = (i, j)

        value = letters.get(letter)
        reachable = []
        if i > 0 and letters.get(lines[i-1][j]) <= value + 1:
            reachable.append((i-1, j))
        if i < N_lines - 1 and letters.get(lines[i+1][j]) <= value + 1:
            reachable.append((i+1, j))
        if j > 0 and letters.get(lines[i][j-1]) <= value + 1:
            reachable.append((i, j-1))
        if j < N_columns - 1 and letters.get(lines[i][j+1]) <= value + 1:
            reachable.append((i, j+1))

        neighbors[(i, j)] = reachable

def shortest_path(neighbors, start, dest):
    ### DIJKSTRA SPF ALGORITHM
    visited = set()
    # Insert starting point with distance 0
    queue = PriorityQueue()
    queue.put((0, start))
    min_distance = {}
    min_distance[start] = 0

    while not queue.empty():
        dist, node = queue.get()
        if node == dest:
            break
        if node not in visited:
            for successor in neighbors[node]:
                distance = min_distance[node] + 1
                if successor not in min_distance or distance < min_distance[successor]:
                    min_distance[successor] = distance
                    queue.put((distance, successor))
        visited.add(node)
    return min_distance[dest]
    
print(shortest_path(neighbors, starting_point, destination_point))