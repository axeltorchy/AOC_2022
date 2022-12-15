import utils
import matplotlib.pyplot as plt
import re
from time import time
example = False
inputfile = utils.INPUT_DIR / "day15.txt"
row_y = 2000000
max_coord = 4000000
multiplier = 4000000
if example:
    inputfile = utils.INPUT_DIR / "day15_example.txt"
    row_y = 10
    max_coord = 20


with open(inputfile, 'r') as fh:
    lines = fh.readlines()

# Maps closest beacon to each sensor
sensors = {}
beacons = set()
sensors_dist_nearest = {}

def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

count = 1
for line in lines:
    #print(f"Line {count}")
    x1, y1, x2, y2 = map(int, re.findall(r'-?\d+', line))
    #print(f"  Sensor is at {x1} , {y1}")
    #print(f"  Beacon is at {x2} , {y2}")
    sensors[(x1, y1)] = (x2, y2)
    beacons.add((x2, y2))
    sensors_dist_nearest[(x1,y1)] = dist(x1, y1, x2, y2)
    count += 1

print(f"Found {len(beacons)} beacons.")
print(f"Found {len(sensors)} sensors.")

# Part 1
# Find how many positions cannot contain a beacon on row
def get_no_beacon_y(y, sensors, beacons):
    no_beacon = set() # x coordinates that don't have a sensor
    for sensor in sensors:
        x_bc, y_bc = sensors[sensor]
        x_ss, y_ss = sensor
        distance = dist(x_bc, y_bc, x_ss, y_ss) # dist between sensor and closests beacon
        remain_dist = distance - abs(y_ss - row_y) # remaining dist on x axis
        # If the remaining distance is negative, no iteration of the for loop will occur

        # all x positions between x_ss - remain_dist
        # and x_ss + remain_dist cannot have a beacon
        for x in range(x_ss - remain_dist, x_ss + remain_dist + 1):
            if (x,row_y) not in beacons and (x, row_y) not in sensors:
                no_beacon.add(x)
                #print(f"No beacon at {x},{row_y}")
            else:
                #print(f"Beacon at {x},{row_y}")
                pass
    return no_beacon

# Result is higher than 2887169
no_beacon = get_no_beacon_y(row_y, sensors, beacons)
print(len(no_beacon))
if example:
    print(no_beacon)

# Part 2
# Brute force
def find_free_pos(sensors, max_coord):
    for y in range(max_coord+1):
        print("Line", y)
        line = [True] * (max_coord + 1)
        for sensor in sensors:
            x_bc, y_bc = sensors[sensor]
            x_ss, y_ss = sensor
            distance = dist(x_bc, y_bc, x_ss, y_ss) # dist between sensor and closests beacon
            
            remain_dist = distance - abs(y_ss - y)
            if remain_dist < 0:
                continue
            from_x = max(0, x_ss - remain_dist)
            to_x = min(x_ss + remain_dist + 1, max_coord + 1)

            for x in range(from_x, to_x):
                # print(x,y,"because of sensor", sensor, "beacon", sensors[sensor], \
                #     "distance", distance, "remain", remain_dist, "from", from_x, "to", to_x)
                line[x] = False
        
        # print(line)
        for x in range(max_coord):
            if line[x]:
                return (x,y)
        
def get_points_at_dist(source_x, source_y, dist_from_source):
    points = []
    for i in range(dist_from_source):
        p1 = (source_x + dist_from_source - i, source_y - i)
        p2 = (source_x - i, source_y - dist_from_source + i)
        p3 = (source_x - dist_from_source + i, source_y + i)
        p4 = (source_x + i, source_y + dist_from_source - i)
        points.extend([p1, p2, p3, p4])
    return points

def find_free_pos2(sensors, max_coord):
    sensors_edges = []
    for sensor in sensors:
        # Distance of edge pos = dist nearest anchor + 1
        distance = sensors_dist_nearest[sensor] + 1
        # There are 4*xxxx possible edge positions
        points = get_points_at_dist(sensor[0], sensor[1], distance)
        for point in points:
            if point not in beacons and point[0] >= 0 and \
                point[0] <= max_coord and point[1] >= 0 and \
                point[1] <= max_coord:
                sensors_edges.append(point)
    
    for position in sensors_edges:
        for sensor in sensors:
            distance = dist(position[0], position[1], sensor[0], sensor[1])
            if distance <= sensors_dist_nearest[sensor]:
                break
        else:
            break
        
    return position
                
start_time = time()
print(f"Looking for free position, max coordinates: {max_coord}")
# The free position must be on one of the edges!
free_position = find_free_pos2(sensors, max_coord)

print(f"Found free position at {free_position}")

def frequency(position):
    return position[0] * multiplier + position[1]

print(f"Tuning frequency is {frequency(free_position)}")
stop_time = time()
print(f"Executed in {stop_time - start_time} seconds")
            