import utils
import string

inputfile = utils.INPUT_DIR / "day4.txt"

with open(inputfile, "r") as fh:
    lines = fh.readlines()

# Part 1
count_fully_contained = 0
count_overlap = 0
for line in lines:
    line = line.strip()
    first_range, second_range = line.split(",")
    first_range, second_range = first_range.split("-"), second_range.split("-")
    ranges_bits = [0, 0]
    for i in range(int(first_range[0]), int(first_range[1])+1):
        ranges_bits[0] |= 1 << i
    for i in range(int(second_range[0]), int(second_range[1])+1):
        ranges_bits[1] |= 1 << i
    if ranges_bits[0] & ranges_bits[1] in [ranges_bits[0], ranges_bits[1]]:
        print(f"Fully contained! Line: '{line}'")
        count_fully_contained += 1
    if ranges_bits[0] & ranges_bits[1] != 0:
        print(f"Overlap! Line: '{line}'")
        count_overlap += 1

print(f"Number of fully contained pairs: {count_fully_contained}")
print(f"Number of overlapping pairs: {count_overlap}")
