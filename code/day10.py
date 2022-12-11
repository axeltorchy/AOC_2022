import utils

inputfile = utils.INPUT_DIR / "day10.txt"
#inputfile = utils.INPUT_DIR / "day10_example_part1.txt"


cycle = 1
register = 1 # sprite position
pending_addx = 0
signal_strength = []
two_cycles = False
pixels = []

with open(inputfile, "r") as fh:
    line = fh.readline()
    while line:
        if not two_cycles:
            register += pending_addx
            pending_addx = 0
            instruction = line.strip().split(" ")[0]
            
            if instruction == "addx":
                value = int(line.strip().split(" ")[1])
                #print(f"Addx value: {value}")
                pending_addx = value
                two_cycles = True
            line = fh.readline()
        else:
            two_cycles = False
        
        print(f"Cycle: {cycle}, register = {register}")
        if abs(register - ((cycle - 1) % 40)) <= 1:
            pixels.append("#")
        else:
            pixels.append(".")
        signal_strength.append(cycle * register)
        cycle += 1

print(signal_strength[19::40])
print(f"Sum of signal strengths: {sum(signal_strength[19::40])}")

print("Eight capital letters:")
for i in range(6):
    print("".join(pixels[40*i:40*(i+1)]))