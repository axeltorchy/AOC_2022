import utils
import re
import numpy as np
from time import time

example = False
inputfile = utils.INPUT_DIR / "day20.txt"
if example:
    inputfile = utils.INPUT_DIR / "day20_example.txt"

original_numbers = []
decryption_key = 1

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

for line in lines:
    original_numbers.append(int(line.strip()) * decryption_key)

N_nb = len(original_numbers)


# # references are the index in the original_numbers list
# neighbors = {}

# for i in range(N_nb):
#     neighbors[i] = {
#         "previous": (i - 1) % N_nb,
#         "next": (i + 1) % N_nb
#     }

# # print(neighbors)
# for i in range(N_nb):
#     print(f"{i} moves between ")

current_positions = [i for i in range(N_nb)]
current_list = [i for i in range(N_nb)] # contains the indices of numbers in original list

for i in range(N_nb):
    #print("i is", i)
    #print(f"Current positions are", current_positions)
    #print(f"Current list is: {current_list}")
    # makes shift between 0 and len(init_numbers) - 1
    shift = original_numbers[i]
    #print("Shift is", shift)
    new_position = (current_positions[i] + shift) % (N_nb - 1)

    #print(f"Moving number {original_numbers[i]} (currently at position {current_positions[i]}) to position {new_position}")

    # moving left, shifting the others right in the list
    if new_position > current_positions[i]:
        #print("Moving right")
        for n in range(current_positions[i] + 1, new_position + 1):
            #print(f"   n = {n}")
            index_to_move = current_list[n]
            current_positions[index_to_move] = (current_positions[index_to_move] - 1) % N_nb
            current_list[n-1] = current_list[n]
            #print(f"   Current positions are {current_positions}")
            #print(f"   Current list is: {current_list}")
    # moving right, shifting the others left in the list
    elif new_position < current_positions[i]:
        #print("Moving left")
        for n in range(current_positions[i]-1, new_position-1, -1):
            index_to_move = current_list[n]
            current_positions[index_to_move] = (current_positions[index_to_move] + 1) % N_nb
            current_list[n+1] = current_list[n]
            #print(f"   Current positions are {current_positions}")
            #print(f"   Current list is: {current_list}")

    else:
        print("Nothing changes!")

    current_positions[i] = new_position
    current_list[new_position] = i

    #print(f"Current positions are {current_positions}")
    #print(f"Current list is {current_list}")
    #print("------")


#print(current_positions)

#print(current_list)

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