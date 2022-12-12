import utils

inputfile = utils.INPUT_DIR / "day11.txt"
#inputfile = utils.INPUT_DIR / "day11_example_part1.txt"

class Monkey():

    monkeys_list = {}
    N_monkeys = 0

    def __init__(self, id, items, operation, divisibleby, true_id, false_id):
        self.id = id
        self.items = []
        for item in items:
            self.add_item(int(item))
        self.operation = lambda old : eval(operation) # lambda function
        self.divisibleby = divisibleby
        self.true_id = true_id
        self.false_id = false_id
        self.items_inspected = 0
        Monkey.monkeys_list[id] = self
        Monkey.N_monkeys += 1

    def __repr__(self):
        return f"Monkey {self.id}"

    def describe(self):
        print(self)
        print(f"  Carries items: {self.items}")
        print(f"  Operation: {self.operation}")
        print(f"  Test: {self.divisibleby}")
        print(f"  If true, throw to monkey {self.true_id}")
        print(f"  If false, throw to monkey {self.false_id}")
        print(f"  Example lambda with 10: {self.operation(10)}")

    def process_items(self):
        #if len(self.items) == 0:
        #    print(f"No item to process for {self}.")
        for item in self.items:
            # process operation
            #print(f"{self} inspecting item {item}")
            item = self.operation(item)
            # relief
            #print(f"Before bored, worry level is {item}")
            item = int(item * 1.0 / 3)
            # inspection
            #print(f"After bored, worry level is {item}")
            self.items_inspected += 1
            if item % self.divisibleby == 0:
                #print(f"Sending item {item} to monkey {self.true_id}")
                Monkey.monkeys_list[self.true_id].add_item(item)
            else:
                #print(f"Sending item {item} to monkey {self.false_id}")
                Monkey.monkeys_list[self.false_id].add_item(item)
        # remove all items
        self.items = []

    def add_item(self, item):
        self.items.append(item)


# Initialize Monkeys list
with open(inputfile, "r") as fh:
    line = True
    id = 0
    while line:
        line = fh.readline().strip()
        monkey_id = int(line.split(" ")[1][:-1])
        if monkey_id != id:
            print("Something went wrong: ID mismatch.")

        starting_items = fh.readline().strip().split("Starting items: ", 1)[1]
        operation = fh.readline().strip().split("Operation: new = ", 1)[1]
        test = int(fh.readline().strip().split("Test: divisible by ", 1)[1])
        if_true = int(fh.readline().strip().split("If true: throw to monkey ", 1)[1])
        if_false = int(fh.readline().strip().split("If false: throw to monkey ", 1)[1])
        line = fh.readline()
        items = [int(item) for item in starting_items.split(", ")]
        # processing operation
        monkey = Monkey(id, items, operation, test, if_true, if_false)

        id += 1

# Part 1
max_round = 20

for i in range(max_round):
    print(f"---- Round {i+1} ----")
    for j in range(len(Monkey.monkeys_list)):
        monkey = Monkey.monkeys_list[j]
        monkey.process_items()

max_inspected = [0, 0]
idx_max_inspected = [-1, -1]
for i in range(Monkey.N_monkeys):
    items_inspected = Monkey.monkeys_list[i].items_inspected
    if max_inspected[0] < items_inspected:
        max_inspected[0] = items_inspected
        idx_max_inspected[0] = i
for i in range(Monkey.N_monkeys):
    items_inspected = Monkey.monkeys_list[i].items_inspected
    if items_inspected != max_inspected[0] and max_inspected[1] < items_inspected:
        max_inspected[1] = items_inspected
        idx_max_inspected[1] = i

print("Level of monkey business:", max_inspected[0]*max_inspected[1])
    