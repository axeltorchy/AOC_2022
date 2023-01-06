import utils
import re
import numpy as np
from time import time

example = True
inputfile = utils.INPUT_DIR / "day19.txt"
if example:
    inputfile = utils.INPUT_DIR / "day19_example.txt"

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

# Initial states for each blueprint
blueprints = []

# Parsing input
for line in lines:
    regex = r"Blueprint (\d+): Each ore robot costs (\d+) ore. " \
        r"Each clay robot costs (\d+) ore. " \
        r"Each obsidian robot costs (\d+) ore and (\d+) clay. " \
        r"Each geode robot costs (\d+) ore and (\d+) obsidian."
    values = re.compile(regex).match(line)
    blueprint = values.group(1)
    ore_robot_cost_ore = values.group(2)
    clay_robot_cost_ore = values.group(3)
    obsd_robot_cost_ore = values.group(4)
    obsd_robot_cost_clay = values.group(5)
    geode_robot_cost_ore = values.group(6)
    geode_robot_cost_obsd = values.group(7)

    blueprints.append(tuple([int(values.group(i)) for i in range(1,8)]))


def max_geodes(max_geodes_memo, time_left, N_ore_robot, N_clay_robot, N_obsd_robot, N_geode_robot,
               N_ore, N_clay, N_obsd, costs):
    """Computes the maximum number of geodes that can be opened when
    starting at the provided state
    """
    if time_left == 0:
        # When no time left, no geode can be opened
        return N_geode_robot
    
    state = time_left, N_ore_robot, N_clay_robot, N_obsd_robot, N_geode_robot, N_ore, N_clay, N_obsd
    if state in max_geodes_memo:
        #print(f"State already visited! [{state}]")
        return max_geodes_memo[state]

    local_max = 0
    # Explore each possible choice and choose the best one
    # Only one robot can be built at a time 
    # - Build an ore robot
    if N_ore >= costs["ore"]["ore"]:
        local_max = max(local_max, max_geodes(max_geodes_memo, time_left - 1,
                                              N_ore_robot + 1, N_clay_robot, N_obsd_robot, N_geode_robot,
                                              N_ore - costs["ore"]["ore"] + N_ore_robot,
                                              N_clay + N_clay_robot, N_obsd + N_obsd_robot, costs) + N_geode_robot)
    # - Build a clay robot
    if N_ore >= costs["clay"]["ore"]:
        local_max = max(local_max, max_geodes(max_geodes_memo, time_left - 1,
                                              N_ore_robot, N_clay_robot + 1, N_obsd_robot, N_geode_robot,
                                              N_ore - costs["clay"]["ore"] + N_ore_robot,
                                              N_clay + N_clay_robot, N_obsd + N_obsd_robot, costs) + N_geode_robot)
    # - Build an obsidian
    if N_ore >= costs["obsidian"]["ore"] and N_clay >= costs["obsidian"]["clay"]:
        local_max = max(local_max, max_geodes(max_geodes_memo, time_left - 1,
                                              N_ore_robot, N_clay_robot, N_obsd_robot + 1, N_geode_robot,
                                              N_ore - costs["obsidian"]["ore"] + N_ore_robot,
                                              N_clay - costs["obsidian"]["clay"] + N_clay_robot,
                                              N_obsd + N_obsd_robot, costs) + N_geode_robot)
    # - Build a geode robot
    if N_ore >= costs["geode"]["ore"] and N_obsd >= costs["geode"]["obsidian"]:
        local_max = max(local_max, max_geodes(max_geodes_memo, time_left - 1,
                                              N_ore_robot, N_clay_robot, N_obsd_robot, N_geode_robot + 1,
                                              N_ore - costs["geode"]["ore"] + N_ore_robot,
                                              N_clay + N_clay_robot,
                                              N_obsd - costs["geode"]["obsidian"] + N_obsd_robot, costs) + N_geode_robot)
    
    # Or do nothing
    local_max = max(local_max, max_geodes(max_geodes_memo, time_left - 1,
                                          N_ore_robot, N_clay_robot, N_obsd_robot, N_geode_robot,
                                          N_ore + N_ore_robot,
                                          N_clay + N_clay_robot,
                                          N_obsd + N_obsd_robot, costs) + N_geode_robot)

    # Update memoization table
    max_geodes_memo[state] = local_max
    
    return local_max

if __name__ == "__main__":
    print("="*80)
    if example:
        print("Running example.")
        print("="*80)
    sum_quality_levels = 0
    print("Determining quality level for all blueprints.")
    for blueprint in blueprints:
        states = {}
        costs = {
            "ore": {"ore": blueprint[1]},
            "clay": {"ore": blueprint[2]},
            "obsidian": {"ore": blueprint[3], "clay": blueprint[4]},
            "geode": {"ore": blueprint[5], "obsidian": blueprint[6]}
        }
        number_geodes = max_geodes(states, 24, 1, 0, 0, 0, 0, 0, 0, costs)
        print(f"Blueprint {blueprint[0]}: quality level = {number_geodes * blueprint[0]} ; nb geodes = {number_geodes}")
        sum_quality_levels += number_geodes * blueprint[0]
        
    print(f"Sum of quality levels: {sum_quality_levels}")