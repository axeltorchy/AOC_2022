import utils
import re
import numpy as np
from time import time

example = False
inputfile = utils.INPUT_DIR / "day16.txt"
if example:
    inputfile = utils.INPUT_DIR / "day16_example.txt"

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

valve_id = {} # key = XX ; value = id
id_valve = {} # key = id ; value = XX
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
    flow_rates[count_valve] = flow_rate
    count_valve += 1


valves_neighbors_id = {}
for valve, neighbors in valves_neighbors.items():
    valves_neighbors_id[valve_id[valve]] = [valve_id[neighbor] for neighbor in neighbors]

print("Neighbors", valves_neighbors_id)
print("Flow rates", flow_rates)

# for valve, neighbors in valves_neighbors.items():
#     for neighbor in neighbors:
#             # Each direct neighbor is at distance 1 from the source valve
#             print("Valve:", valve, "Neighbor:", neighbor)
#             distances[valve_id[valve], valve_id[neighbor]] = 1
            
print(f"Found {len(valves_neighbors)} valves: {valves_neighbors.keys()}")


# Memoization hashtable for each state
max_pressures = {}
count_max_pressure_calls = 0

def max_pressure(current_valve, opened_valves, time_left, using_elephant=False, elephant=False):
    global count_max_pressure_calls
    count_max_pressure_calls += 1
    """
    Recursively computes the maximum pressure releasable starting from the
    provided state.
    Results are saved using memoization so that they are not computed twice.
    """
    # Computing current state, must be hashable
    if time_left == 0:
        #print("No time left. using_elephant:", using_elephant, "elephant:", elephant)
        # The principal human ran out of time, now the elephant can begin
        # starting at valve 0, with the same opened valves
        if using_elephant and not elephant:
            #print("Using elephant")
            return max_pressure(valve_id["AA"], opened_valves, 26, using_elephant=True, elephant=True)
        
        # no time left, no pressure to release
        return 0

    state = (current_valve, opened_valves, time_left, using_elephant, elephant)
    # If state already visited: return stored value for max pressure
    if state in max_pressures:
        #print(f"State {state} already visited.")
        return max_pressures[state]

    local_max = 0
    # If the current valve is *not* open yet and can release pressure:
    # (we won't open valves with a zero flow rate)
    current_is_open = opened_valves & (1 << current_valve) # > 0 if match
    if not current_is_open and flow_rates[current_valve] > 0:
        # open valve
        new_opened_valves = opened_valves | (1 << current_valve)
        local_max = max(local_max, (time_left - 1) * flow_rates[current_valve] + max_pressure(current_valve, new_opened_valves, time_left - 1, using_elephant, elephant))
    
    # For all tunnels, choose the maximum achievable pressure release
    for neighbor in valves_neighbors_id[current_valve]:
        local_max = max(local_max, max_pressure(neighbor, opened_valves, time_left - 1, using_elephant, elephant))

    # Update memoization table
    max_pressures[state] = local_max

    return local_max


if __name__ == "__main__":
    start_valve = "AA"
    opened_valves = 0 # using bitwise operations to store
    if example:
        print("#"*80)
        print(f"### Using example, with {len(valve_id)} valves.")
    print("#"*80)
    start_valve_id = valve_id[start_valve]
    print(f"Part 1: computing best pressure, starting from valve {start_valve}.")
    t = time()
    print(f"Maximum pressure: {max_pressure(start_valve_id, opened_valves, 30, using_elephant=False, elephant=False)}")
    print(f"Computed solution in {time() - t :.2f} seconds.")
    print(f"Called max_pressure function {count_max_pressure_calls} times.")
    print(f"Computed full result for only {len(max_pressures)} different states.")
    print("#"*80)
    print(f"Part 2: computing best pressure with elephant, starting from valve {start_valve}")
    t = time()
    print(f"Maximum pressure: {max_pressure(start_valve_id, opened_valves, 26, using_elephant=True, elephant=False)}")
    print(f"Computed solution in {time() - t :.2f} seconds.")
    print(f"Called max_pressure function {count_max_pressure_calls} times.")
    print(f"Computed full result for only {len(max_pressures)} different states.")