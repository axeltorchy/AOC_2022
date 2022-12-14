import utils
import functools

inputfile = utils.INPUT_DIR / "day13_example.txt"
inputfile = utils.INPUT_DIR / "day13.txt"

pair_nb = 1
sum_indices = 0

def compare(left, right, indent=""):
    print(f"{indent}Compare {left} vs {right}")
    if type(left) == list and type(right) == int:
        print(f"{indent}Mixed types: convert right to [{right}] and retry comparison")
        return compare(left, [right], indent)
    elif type(left) == int and type(right) == list:
        print(f"{indent}Mixed types: convert left to [{left}] and retry comparison")
        return compare([left], right, indent)
    elif type(left) == list and type(right) == list:
        for i in range(len(left)):
            if i >= len(right):
                print(f"{indent} - Right side ran out of items, so inputs are not in the right order")
                return False
            result = compare(left[i], right[i], indent+"  ")
            if result == False:
                return False
            elif result == True:
                return True

        if len(left) < len(right):
            print(f"{indent} - Left side ran out of items, so inputs are in the right order.")
            return True

    elif type(left) == int and type(right) == int:
        if left < right:
            print(f"{indent} - Left side is smaller, so inputs are in the right order.")
            return True
        elif left > right:
            print(f"{indent} - Right side is smaller, so inputs are not the right order.")
            return False

def comparator(left, right):
    result = compare(left, right)
    return -1 if result else 1 # could not return 0, no equality

# List of packets for part two
packets = []

with open(inputfile, 'r') as fh:
    line = True
    while line:
        print(f"== Pair {pair_nb} ==")
        left = eval(fh.readline().strip())
        if line == "":
            break
        right = eval(fh.readline().strip())
        print(left, right)
        #print(type(left), type(right))
        line = fh.readline()

        right_order = compare(left, right)

        if right_order:
            sum_indices += pair_nb

        pair_nb += 1

        packets.extend([left, right])

# Part 1
print(f"Sum of indices for pairs in right order: {sum_indices}")

# Part 2
# Add divider packets
start = [[2]]
stop = [[6]]
packets.extend([start, stop])
sorted_packets = sorted(packets, key=functools.cmp_to_key(comparator))
decoder_key = 1
for i in range(len(sorted_packets)):
    if sorted_packets[i] == start:
        decoder_key *= i+1
    if sorted_packets[i] == stop:
        decoder_key *= i+1
        break

print(f"Decoder key is: {decoder_key}")
