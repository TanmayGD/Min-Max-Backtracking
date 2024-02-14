
import re

class Node: # This is a data structure to emulate a node in our tree
    def __init__(self, name):
        self.name = name 
        self.value = float('-inf')  # Initialize value to negative infinity
        self.children = []

    def set_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def set_value(self, value):
        self.value = value

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

def play_minmax(max_flag, verbose_flag, alpha, beta, range_val, root, parent, original_root, optimization_flag, output): #Function to play/solve the game
    
    if not root.get_children(): # Base case of reaching leaf nodes
        return root.get_value()

    selected_node = None
    prune_flag = False
    selected_value = float('-inf') if max_flag else float('inf')

    for child in root.get_children():
        
        solved_value = play_minmax( not max_flag, verbose_flag, alpha, beta, range_val, child, root, original_root, optimization_flag, output) #recursive call to the next level of the game

        if max_flag: # If max level
            if solved_value > selected_value:
                selected_node = child
                selected_value = solved_value
            
            if optimization_flag: 
                alpha = max(alpha, solved_value)

            if solved_value >= range_val: # Ignoring nodes that are out of range
                break

        else: # If min level
            if solved_value < selected_value:
                selected_node = child
                selected_value = solved_value
            
            if optimization_flag: 
                beta = min(beta, solved_value)

            if solved_value <= -range_val: # Ignoring nodes that are out of range
                break

        if optimization_flag:
            if beta <= alpha: # Condition check for pruning
                prune_flag = True
                break

    if (not prune_flag and verbose_flag) or root == original_root: # Output creation
        player_type = "max" if max_flag else "min"
        output.append(f"{player_type}({root.get_name()}) chooses {selected_node.get_name()} for {selected_value}")

    return selected_value


def tree(leaf_nodes, root_key, mappings, parent, visited): # Function that initializes the data structure for our input
    
    if root_key in visited: # Maintianing visited list to track cycles in graph
        print("Cycle Detected")
        sys.exit(1)

    visited.append(root_key)
    
    root = Node(root_key)
    
    if root_key in leaf_nodes:
        root.set_value(int(leaf_nodes[root_key]))

    if root_key in mappings and mappings[root_key]:
        for child_key in mappings[root_key]:
            child = tree(leaf_nodes, child_key, mappings, root, visited) # Recursive call to initalize children
            root.set_child(child)

    if not root.get_children():
        if root.get_value() == float('-inf'):
            print(f"child node \"{root.get_name()}\" of \"{parent.get_name()}\" not found")
            sys.exit(0)

    visited.remove(root_key) # removing root_key to facilitate DAGs

    return root

def main():
    
    optimization_flag = False
    range_val = float('inf')
    i = 1
    leaf_nodes = {}
    mappings = {}
    output = []
    verbose_flag = False
    parents = []
    childrens = []
    root = []
    visited = []
    max_flag = None

    if len(sys.argv) < 3:
        print("Insufficient number of arguements provided.")
        sys.exit(1)

    while (i<len(sys.argv)): # Using flags to understand command line inputs
        if re.search("\.txt",sys.argv[i]):
            file_name = sys.argv[i]
        else:
            if sys.argv[i] == "-v":
                verbose_flag = True
            else:
                if sys.argv[i] == "max":
                        max_flag = True
                else:
                    if sys.argv[i] == "min":
                        max_flag = False
                    else:
                        if sys.argv[i] == "-range":
                            try:
                                int(sys.argv[i+1])
                            except:
                                print("Invalid type/value for range")
                                exit(1)
                            else:
                                range_val = int(sys.argv[i+1])
                                i = i + 1
                        else:
                            if sys.argv[i] == "-ab":
                                optimization_flag = True
                            else:
                                print(sys.argv[i]+" is not a recognized flag/command.")
                                sys.exit(1)
        i = i + 1 

    if max_flag == None:
        print("min/max player not specified")
        sys.exit(1)

    try: #Opening file
        with open(file_name, "r") as file:
            lines = file.readlines()
    except: 
        print("Error while opening file")
        sys.exit(1)


    for line in lines: # Traversing each line
        line = line.strip()
        
        if line.startswith("#") or not line: # Ignoring comments
            continue

        if ":" in line: # Handling internal nodes
            parent, children = [part.strip() for part in line.split(":")]
            
            children_list = [child.strip() for child in children.split(",")]
            parents.append(parent)
            
            for i in range(len(children_list)): 
                children_list[i] = re.sub(r'[\s\[\]\s]','',children_list[i])
            
            for child in children_list:
                childrens.append(child)

            mappings[parent] = children_list

        if "=" in line: # Handling leaf nodes
            variable_name, variable_value = [part.strip() for part in line.split("=")]
            value = int(variable_value)
            if value > abs(range_val) or value < -abs(range_val):
                print("Input values are out of range.")
                sys.exit(0)
            leaf_nodes[variable_name] = variable_value


    for parent in parents: # Traversing to find root node(s)
        if parent not in childrens:
            root.append(parent)

    if len(root) == 0: # Handling errors relating to root node(s)
        print("No Root node found")
        sys.exit(1)
    else:
        if len(root) > 1:
            print("Multiple roots detected")
            sys.exit(1)
        else:
            root = root[0]

    root_re = tree( leaf_nodes, root, mappings, Node("temp"), visited)
 
    play_minmax(max_flag, verbose_flag, float('-inf'), float('inf'), abs(range_val), root_re, Node("temp"), root_re, optimization_flag, output)

    for k in output:
        print(k)

if __name__ == "__main__":
    main()
