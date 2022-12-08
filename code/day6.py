import utils
from itertools import cycle

inputfile = utils.INPUT_DIR / "day6.txt"

with open(inputfile, "r") as fh:
    line = fh.readline()

count = 1
known_chars = []
for char in line:
    print(char)
    if char not in known_chars and len(known_chars) == 3:
        print("WIN! Count:", count, "Known:", known_chars, "Char:", char)
        known_chars.append(char)
        break
    elif char in known_chars:
        print("Char", char, "already in list! Known:", known_chars)
        char_idx = known_chars.index(char)
        known_chars.append(char)
        known_chars = known_chars[char_idx+1:]
        print("Index", char_idx, "New known:", known_chars)
    else:
        known_chars.append(char)
    
    count += 1

print("Marker position:", count)