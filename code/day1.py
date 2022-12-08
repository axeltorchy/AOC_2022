import utils

inputfile = utils.INPUT_DIR / "day1.txt"

N = 3
count = 0
max_calories = 0
maxlist = [0] * N

with open(inputfile, "r") as fh:
    line = fh.readline()
    current_sum = 0
    while line:
        count += 1
        if line.strip() != "":
            current_sum += int(line.strip())
        else:
            if current_sum > max_calories:
                max_calories = current_sum
                print(f"New max: {current_sum} (count = {count})")

            minlist = min(maxlist)
            if minlist < current_sum:
                indexminlist = maxlist.index(minlist)
                maxlist[indexminlist] = current_sum

            current_sum = 0

        line = fh.readline()

print(maxlist)
print(f"The maximum of calories is: {max_calories}.")
print(f"The sum of top three is: {sum(maxlist)}")
print(f"Count = {count}")