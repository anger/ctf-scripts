import angr

# Specify the binary file you want to analyze
binary_path = "./your_binary"

# Create an Angr project
proj = angr.Project(binary_path, auto_load_libs=False)

# Define the address to avoid
avoid_address = 0xdeadbeef

# Define the address to reach
target_address = 0xcafebabe

# Create an Angr state starting from the entry point of the binary
state = proj.factory.entry_state()

# Create an Angr path group to explore the binary
pg = proj.factory.path_group(state)

# Define a custom path filter to avoid the specific address
def avoid_specific_address(path):
    return avoid_address not in path.addr_trace

# Explore the binary while avoiding the specific address and reaching the target address
pg.explore(find=target_address, avoid=avoid_specific_address)

# Check if a path to the target address was found
if len(pg.found) > 0:
    print("Target address reached!")
    target_path = pg.found[0]
    print("Path to target:")
    print(target_path)
else:
    print("Target address not reached.")

# Cleanup resources
proj.close()
