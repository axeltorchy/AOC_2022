import utils

inputfile = utils.INPUT_DIR / "day2.txt"

choice_scores = {'X': 1, 'Y': 2, 'Z': 3, 'A': 1, 'B': 2, 'C': 3}
outcome_scores = {'lost': 0, 'draw': 3, 'won': 6}

total_score = 0

with open(inputfile, "r") as fh:
    lines = fh.readlines()

# Part 1
for line in lines:
    opponent_choice, my_choice = line.strip().split(" ")
    status = "lost"
    if choice_scores[my_choice] - choice_scores[opponent_choice] == 0:
        status = "draw"
    elif (choice_scores[my_choice] - choice_scores[opponent_choice]) % 3 == 2:
        status = "lost"
    else: # %3 == 1
        status = "won"
    total_score += choice_scores[my_choice] + outcome_scores[status]

print(f"Total: {len(lines)} lines.")
print(f"Total score: {total_score}")


# Part 2
my_choices = {1: 'X', 2: 'Y', 0: 'Z'}
choices_to_make = {'X': 2, 'Y': 0, 'Z': 1}
outcomes = {'X': 'lost', 'Y': 'draw', 'Z': 'won'}
total_score_2 = 0

for line in lines:
    opponent_choice, outcome = line.strip().split(" ")
    my_choice = (choice_scores[opponent_choice] + choices_to_make[outcome]) % 3
    my_choice_letter = my_choices[my_choice]

    total_score_2 += outcome_scores[outcomes[outcome]] + choice_scores[my_choice_letter]

print(f"Total score 2: {total_score_2}")