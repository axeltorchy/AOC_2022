import utils
import string
from itertools import cycle

inputfile = utils.INPUT_DIR / "day6.txt"

with open(inputfile, "r") as fh:
    line = fh.readline()

N = 14
current_pos = 1
last_position = {}
current_seq = 0

for char in line:
    if char in last_position and last_position[char] < current_pos - N + 1:
        last_position[char] = current_pos
        current_seq += 1
    elif char in last_position and last_position[char] >= current_pos - N + 1:
        current_seq = min(current_seq +1, current_pos - last_position[char])
        last_position[char] = current_pos
    else: # char not in last_position
        last_position[char] = current_pos
        current_seq += 1
    
    if current_seq == N:
        break

    current_pos += 1

print("Marker position:", current_pos)