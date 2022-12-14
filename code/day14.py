import utils
import matplotlib.pyplot as plt

inputfile = utils.INPUT_DIR / "day14_example.txt"
inputfile = utils.INPUT_DIR / "day14.txt"

rocks = set()
pouring_source = (500, 0)

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

min_y_rock = 0

# Initialization: adding rocks
for line in lines:
    coords = line.strip().split(" -> ")
    if len(coords) == 1:
        print("Only one rock on line, should not happen")
    for i in range(1, len(coords)):
        path = eval(coords[i-1]), eval(coords[i])
        # print(path[0], path[1])
        rocks.add(path[0])
        if path[0][0] == path[1][0]:
            # horizontal line
            diff_y = path[1][1] - path[0][1]
            sign = int(diff_y / abs(diff_y))
            for j in range(1, abs(diff_y) + 1):
                rock = (path[0][0], path[0][1] + j*sign)
                rocks.add(rock)
                if rock[1] > min_y_rock:
                    min_y_rock = rock[1]

        elif path[0][1] == path[1][1]:
            # vertical line
            # horizontal line
            diff_x = path[1][0] - path[0][0]
            sign = int(diff_x / abs(diff_x))
            for j in range(1, abs(diff_x) + 1):
                rock = (path[0][0] + j*sign, path[0][1])
                rocks.add(rock)
                if rock[1] > min_y_rock:
                    min_y_rock = rock[1]
        else:
            print("Path is not horizontal nor vertical.")

print(f"Found {len(rocks)} rocks.")


# Part 1
# Let sand fall from source!
print("Abyss starting below y =", min_y_rock)
#print("Rocks:", rocks)
def make_sand_fall(source, rocks, sands, infinite_floor = False):
    # Returns the number of units of sand that have come
    # to rest
    y_floor = min_y_rock + 2
    if infinite_floor:
        print(f"No sand below floor at y = {y_floor}")
    abyss = False
    count_sand_rest = 0
    while not abyss:
        # New unit of sand
        #print("New sand")
        sand_x, sand_y = pouring_source
        while True:
            #print("Sand position:", sand_x, sand_y)
            if not infinite_floor and sand_y > min_y_rock:
                abyss = True
                print("Abyss reached.")
                break
            down_pos = (sand_x, sand_y + 1)
            if infinite_floor and sand_y + 1 == y_floor:
                #print("Reached flood, cannot move.")
                sand_pos.add((sand_x, sand_y))
                count_sand_rest += 1
                break
            if down_pos not in rocks and down_pos not in sand_pos:
                #print("Moving_down")
                sand_y += 1
            else: # the square below is full
                down_left = (sand_x - 1, sand_y + 1)
                down_right = (sand_x + 1, sand_y + 1)
                if down_left not in rocks and down_left not in sand_pos:
                    #print("Moving down left")
                    sand_x -= 1
                    sand_y += 1
                elif down_right not in rocks and down_right not in sand_pos:
                    #print("Moving down right")
                    sand_x += 1
                    sand_y += 1
                else:
                    # cannot move
                    #print("Adding sand:", sand_x, sand_y)
                    sand_pos.add((sand_x, sand_y))
                    count_sand_rest += 1
                    break
        if (sand_x, sand_y) == source:
            print("The source has been blocked.")
            break
    return count_sand_rest

sand_pos = set()
print(f"Units of sand at rest: {make_sand_fall(pouring_source, rocks, sand_pos)}")

# PLOT result
plot = False
if plot:
    rocks_x = [rock[0] for rock in rocks]
    rocks_y = [rock[1] for rock in rocks]
    sand_x = [sand[0] for sand in sand_pos]
    sand_y = [sand[1] for sand in sand_pos]
    plt.scatter(rocks_x, rocks_y, color="b", marker="s", s=10)
    plt.scatter(sand_x, sand_y, color="r", marker="s", s=2)
    plt.gca().invert_yaxis()
    plt.show()

# Part 2
sand_pos = set()
print(f"Units of sand at rest until source blocked: \
    {make_sand_fall(pouring_source, rocks, sand_pos, infinite_floor=True)}")
