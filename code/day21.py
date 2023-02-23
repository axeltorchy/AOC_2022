import utils
import numpy as np

example = False
inputfile = utils.INPUT_DIR / "day21.txt"
if example:
    print("Playing example.")
    inputfile = utils.INPUT_DIR / "day21_example.txt"

with open(inputfile, 'r') as fh:
    lines = fh.readlines()

class Monkey():

    monkeys = {}

    def __init__(self, name=None, child1_name=None, child2_name=None, operation=None, value=None):
        if value is None and (child1 is None or child2 is None or operation is None):
            raise Exception("Either a value or a complete operation with two children must be specified.")
        
        if name is None:
            raise Exception("The Monkey must have a name.")
        self.name = name
        self.parent_of_humn = False
        self.remainder_to_human = None
        
        if value is not None:
            self.value = value
            self.child1 = None
            self.child2 = None
            self.operation = None
        else:
            self.value = None
            self.child1 = child1
            self.child2 = child2
            self.operation = operation

    def get_value(self):
        if self.value is None:
            #print(f"  {self.name} getting result of {self.operation} from {self.child1} and {self.child2}")
            monkey1 = Monkey.monkeys[self.child1]
            monkey2 = Monkey.monkeys[self.child2]
            if self.operation == "+":
                self.value = monkey1.get_value() + monkey2.get_value()
            elif self.operation == "-":
                self.value = monkey1.get_value() - monkey2.get_value()
            elif self.operation == "*":
                self.value = monkey1.get_value() * monkey2.get_value()
            elif self.operation == "/":
                self.value = monkey1.get_value() // monkey2.get_value()
        
        #print(f"Monkey {self.name} value is {self.value}")
        return self.value

    def set_children_parents(self, parent=None):
        self.parent = parent
        if self.child1 is not None:
            Monkey.monkeys[self.child1].set_children_parents(self)
        if self.child2 is not None:
            Monkey.monkeys[self.child2].set_children_parents(self)

    def get_parent(self):
        return self.parent

    def get_humn(self, should_be_value=None):
        if self.name == "humn":
            return should_be_value
        if not self.parent_of_humn:
            raise Exception(f"Monkey {self.name} is not a parent of humn.")
        
        if self.child1 is None or self.child2 is None:
            raise Exception(f"Monkey {self.name} should have children.")
        
        
        monkey1 = Monkey.monkeys[self.child1]
        monkey2 = Monkey.monkeys[self.child2]
        if monkey1.parent_of_humn:
            humn_parent_child = monkey1
            other_child = monkey2
        else:
            humn_parent_child = monkey2
            other_child = monkey1

        if self.name == "root":
            should_be_value = other_child.get_value()
            return humn_parent_child.get_humn(should_be_value)

        # the other value (not parent of humn) is fixed.
        other_value = other_child.get_value()
        
        # compute the value of the first child (parent of human)
        # First case: the parent of human is the left child
        if humn_parent_child == monkey1:
            if self.operation == "+":
                return monkey1.get_humn(should_be_value - other_value)
            elif self.operation == "-":
                return monkey1.get_humn(should_be_value + other_value)
            elif self.operation == "*":
                return monkey1.get_humn(should_be_value / other_value)
            elif self.operation == "/":
                return monkey1.get_humn(should_be_value * other_value)


        # Second case: the parent of human is the right child
        else:
            if self.operation == "+":
                return monkey2.get_humn(should_be_value - other_value)
            elif self.operation == "-":
                return monkey2.get_humn(other_value - should_be_value)
            elif self.operation == "*":
                return monkey2.get_humn(should_be_value // other_value)
            elif self.operation == "/":
                return monkey2.get_humn(other_value // should_be_value)


for line in lines:
    if len(line.split()) == 2:
        # monkey yells integer
        monkey_name = line.split()[0].strip(":")
        value = int(line.split()[1])
        monkey = Monkey(name=monkey_name, value=value)
    else:
        monkey_name, child1, operation, child2 = line.split()
        monkey_name = monkey_name.strip(":")
        monkey = Monkey(name=monkey_name, child1_name=child1, child2_name=child2, operation=operation)

    Monkey.monkeys[monkey_name] = monkey


print("======")
print("Part 1 solution: root value is", Monkey.monkeys["root"].get_value())

# Part 2
Monkey.monkeys["root"].set_children_parents()

monkey = Monkey.monkeys["humn"]
while True:
    parent = monkey.get_parent()
    if parent is None:
        break
    #print(f"Parent of {monkey.name} = {parent.name}")
    monkey.parent_of_humn = True
    monkey = parent
Monkey.monkeys["root"].parent_of_humn = True

print("======")
print("Part 2 solution:", int(Monkey.monkeys["root"].get_humn()))
print("======")