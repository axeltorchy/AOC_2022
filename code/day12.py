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

elevation_a = []
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
        if value == 1:
            elevation_a.append((i,j))
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

class UpdatablePriorityQueue():
    def __init__(self):
        self.nodes = []
    
    def put(self, item):
        # Check if exists, update
        updated = False
        for i in range(len(self.nodes)):
            if self.nodes[i][1] == item[1]:
                self.nodes[i] = item
        # otherwise add to queue
        if not updated:
            self.nodes.append(item)
        self.nodes.sort()
        self.nodes.reverse()

    
    def exists(self, item):
        return item in self.nodes

    def get(self):
        return self.nodes.pop()

    def empty(self):
        return len(self.nodes) == 0

def shortest_path(neighbors, start, dest):
    ### DIJKSTRA SPF ALGORITHM
    visited = set()
    # Insert starting point with distance 0
    queue = UpdatablePriorityQueue()
    queue.put((0, start))
    #print(f"Added node {start}. Queue is: {queue.nodes}")
    min_distance = {}
    min_distance[start] = 0

    while not queue.empty():
        _, node = queue.get()
        #print(f"Adding node {node} to visited.")
        if node == dest:
            break
        if node not in visited:
            for successor in neighbors[node]:
                distance = min_distance[node] + 1
                if successor not in min_distance or distance < min_distance[successor]:
                    min_distance[successor] = distance
                    queue.put((distance, successor))
                    #print(f"Added node {node}. Queue is: {queue.nodes}")
        visited.add(node)
    
    if dest not in min_distance:
        #print(f"Destination not reachable from {start}.")
        return False
    return min_distance[dest]

# Part 1
print("Shortest path from S:", shortest_path(neighbors, starting_point, destination_point))

# Part 2
min_dist = N_lines * N_columns
for start in elevation_a:
    dist = shortest_path(neighbors, start, destination_point)
    if dist and dist < min_dist:
        min_dist = dist

print(destination_point)
print(f"Shortest path from any elevation 'a': {min_dist}")