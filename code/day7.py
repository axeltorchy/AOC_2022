import utils

inputfile = utils.INPUT_DIR / "day7.txt"

class Node:
    """Node of a tree = folder or file"""
    def __init__(self, name="/", children=None, parent=None, size=0):
        self.name = name
        self.children = {}
        self.size = size
        self.parent = parent
        if parent is not None:
            self.parent.add_child(self)
        
        if children is not None:
            for child in children:
                self.add_child(child)
    
    def __repr__(self):
        return self.name

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self.children) == 0
    
    def depth(self):
        if self.is_root():
            return 0
        else:
            return self.parent.depth() + 1

    def get_size(self):
        return self.size

    def add_size(self, size):
        self.size += size
        if self.parent is not None:
            self.parent.add_size(size)

    def substract_size(self, size):
        self.size -= size
        if self.parent is not None:
            self.parent.substract_size(size)

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def add_child(self, child):
        child.set_parent(self)
        self.children[child.name] = child
        self.add_size(child.get_size())
    

class Tree:
    """Tree = set of Nodes with a root"""
    def __init__(self):
        self.root = None
        self.nodes = []

    def insert(self, node, parent = None):
        if node.parent is None:
            print("Adding new root!", node)
            self.root = node
        self.nodes.append(node)

    def get_root(self):
        return self.root



with open(inputfile, "r") as fh:
    lines = fh.readlines()

filesystem = Tree()

count = 1
current_folder = None
list_files = False
for line in lines:
    #print(f"--- Line {count} - current folder: {current_folder}")
    line = line.strip()
    if line.startswith("$ cd /") and current_folder is None:
        print("Entering root folder.")
        root = Node("/", None, None, 0)
        filesystem.insert(root)
        current_folder = root

    elif line.startswith("$ cd .."):
        current_folder = current_folder.get_parent()
        #print(f"Entering parent folder '{current_folder.name}'")

    elif line.startswith("$ cd "):
        folder_name = line[5:]
        #print(f"Entering child folder '{folder_name}'")
        if folder_name in current_folder.children:
            #print("Already visited! Entering.")
            current_folder = current_folder.children[folder_name]
        else:
            #print(f"Not visited yet. Adding {folder_name} and entering.")
            new_folder = Node(folder_name, None, current_folder, 0)
            filesystem.insert(new_folder)
            current_folder.add_child(new_folder)
            current_folder = new_folder

    elif line.startswith("$ ls"):
        #print(f"Listing files.")
        pass

    elif line.startswith("dir"):
        folder_name = line[4:]
        #print(f"It's a dir: {folder_name}")
        new_folder = Node(folder_name, None, current_folder, 0)
        filesystem.insert(new_folder)
    else: # It's a file
        #print(f"It's a file: {line}")
        size, filename = line.split(" ")
        file = Node(filename, None, current_folder, int(size))
        filesystem.insert(file)

    count += 1

# Part 1
total_sizes = 0
for node in filesystem.nodes:
    # Add size is folder (has children) and size <= 100000
    if node.get_size() <= 100000 and len(node.children) > 0:
        total_sizes += node.get_size()

root_size = filesystem.nodes[0].get_size()
print(f"Total sizes of dirs <= 100000: {total_sizes}")
print(f"Size of root (used space): {root_size}")

total_disk_space = 70000000
update_size = 30000000
unused_space = total_disk_space - root_size
required_space = update_size - unused_space
print(f"Unused space: {unused_space}")
print(f"You need to free up: {required_space}")

# Part 2: find smallest directory that will free up enough space
min_size_qualified = total_disk_space
for node in filesystem.nodes:
    if len(node.children) == 0:
        continue
    size = node.get_size()
    if size >= required_space and size < min_size_qualified:
        print(f"Directory {node.name} qualifies with size {size}.")
        min_size_qualified = size

print(f"The size of the deleted folder is {min_size_qualified}.")