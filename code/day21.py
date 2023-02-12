import utils
import numpy as np

example = False
inputfile = utils.INPUT_DIR / "day21.txt"
if example:
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


print("Root value is", Monkey.monkeys["root"].get_value())
