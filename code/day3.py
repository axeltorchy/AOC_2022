import utils
import string

inputfile = utils.INPUT_DIR / "day3.txt"

# Set priorities
priorities = {}
reverse_priorities = {}
for index, letter in enumerate(string.ascii_lowercase):
   priorities[letter] = index + 1
   reverse_priorities[index + 1] = letter
for index, letter in enumerate(string.ascii_uppercase):
   priorities[letter] = index + 27
   reverse_priorities[index + 1] = letter

with open(inputfile, "r") as fh:
    lines = fh.readlines()

# Part 1
total_priorities = 0
for line in lines:
    line = line.strip()
    nb_items = len(line)
    first_half, second_half = line[:nb_items//2], line[nb_items//2:]
    
    for item in first_half:
        if item in second_half:
            total_priorities += priorities[item]
            break

print(f"(Part 1 - method 1) Total priorities: {total_priorities}")

# Alternative part 1
total_priorities = 0
for line in lines:
    line = line.strip()
    nb_items = len(line)
    first_half, second_half = line[:nb_items//2], line[nb_items//2:]

    items_first_half, items_second_half = 0, 0
    for char in first_half:
        items_first_half |= 1 << priorities[char]
    for char in second_half:
        items_second_half |= 1 << priorities[char]
    
    common_item = items_first_half & items_second_half
    for i in range(len(priorities)):
        letter_pos = 1 << (i+1)
        if common_item == letter_pos:
            total_priorities += i+1
            break

print(f"(Part 1 - method 2) Total priorities: {total_priorities}")

# Part 2
total_priorities_badges = 0
for i in range(len(lines)//3):
    group = [
        lines[3*i].strip(),
        lines[3*i + 1].strip(),
        lines[3*i+2].strip()
        ]
    letters = {}
    # for each bag
    for j in range(len(group)):
        for char in group[j]:
            mask = 1 << j
            if char not in letters:
                letters[char] = mask
            else:
                letters[char] = letters[char] | mask

            if letters[char] == 7:
                total_priorities_badges += priorities[char]
                #print(f"Found badge: {char}, priority {priorities[char]}")
                break


print(f"Total priorities badges: {total_priorities_badges}")
