import utils
import numpy as np

# set part_2 to False to see results for part 1
part_2 = True
example = True
inputfile = utils.INPUT_DIR / "day20.txt"
if example:
    inputfile = utils.INPUT_DIR / "day20_example.txt"

original_numbers = []
# decryption key is 1 for part 1
decryption_key = 1
if part_2:
    decryption_key = 811589153

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

for line in lines:
    original_numbers.append(int(line.strip()) * decryption_key)

N_nb = len(original_numbers)

current_positions = [i for i in range(N_nb)]
current_list = [i for i in range(N_nb)] # contains the indices of numbers in original list

multiplier = 1
if part_2:
    multiplier = 10
for ii in range(multiplier * N_nb):
    
    i = ii % N_nb

    shift = original_numbers[i]
    new_position = (current_positions[i] + shift) % (N_nb - 1)

    # moving left, shifting the others right in the list
    if new_position > current_positions[i]:
        #print("Moving right")
        for n in range(current_positions[i] + 1, new_position + 1):
            index_to_move = current_list[n]
            current_positions[index_to_move] = (current_positions[index_to_move] - 1) % N_nb
            current_list[n-1] = current_list[n]
    elif new_position < current_positions[i]:
        for n in range(current_positions[i]-1, new_position-1, -1):
            index_to_move = current_list[n]
            current_positions[index_to_move] = (current_positions[index_to_move] + 1) % N_nb
            current_list[n+1] = current_list[n]

    else:
        print("Nothing changes!")

    current_positions[i] = new_position
    current_list[new_position] = i

print("="*80)

final_list = []
for i in current_list:
    final_list.append(original_numbers[i])

print(final_list)

zero_index = 0
for i in range(len(final_list)):
    if final_list[i] == 0:
        zero_index = i
        print(f"Zero is at index {i}")

print(f"The 1000th number after 0 is {final_list[(zero_index + 1000) % N_nb]}")
print(f"The 2000th number after 0 is {final_list[(zero_index + 2000) % N_nb]}")
print(f"The 3000th number after 0 is {final_list[(zero_index + 3000) % N_nb]}")

print(f"The result of the sum is {sum([final_list[(zero_index + i * 1000) % N_nb] for i in range(1,4)])}")