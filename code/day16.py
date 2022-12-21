import utils
import re
import numpy as np

example = True
inputfile = utils.INPUT_DIR / "day16.txt"
if example:
    inputfile = utils.INPUT_DIR / "day16_example.txt"

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

valve_id = {}
id_valve = {}
valves_neighbors = {}
N_valves = len(lines)
flow_rates = np.zeros(N_valves, dtype=int)

# Initializing distances between valves as "infinite"
distances = N_valves * ( np.ones((N_valves, N_valves), dtype=int) - np.identity(N_valves, dtype=int) )

count_valve = 0
# Parsing input
for line in lines:
    if len(line) < 2:
        print("Empty line.")
        break

    values = re.compile(r"Valve ([A-Z]+) has flow rate=(\d+); [a-z ]* ((([A-Z]+)(, )?)*)").match(line)
    valve = values.group(1) # "AA"
    flow_rate = int(values.group(2)) # int
    valves_neighbors[valve] = values.group(3).split(", ") # ["AA", "BB", "CC"]

    valve_id[valve] = count_valve
    id_valve[count_valve] = valve
    count_valve += 1
    #print(f"Valve {valve}, flow_rate {flow_rate} leading to valves {leading_to_valves}")
    
print(valves_neighbors)

for valve, neighbors in valves_neighbors.items():
    for neighbor in neighbors:
            # Each direct neighbor is at distance 1 from the source valve
            print("Valve:", valve, "Neighbor:", neighbor)
            distances[valve_id[valve], valve_id[neighbor]] = 1
            
print(f"Found {len(valves_neighbors)} valves: {valves_neighbors.keys()}")

# Computing distances

print(distances)