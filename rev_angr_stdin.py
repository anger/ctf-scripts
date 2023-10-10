import angr
from IPython import embed

project = angr.Project("./angry", main_opts={'base_addr': 0}, auto_load_libs=False)

# Start in main()
initial_state = project.factory.entry_state()
print(initial_state)

# Start simulation
sm = project.factory.simgr(initial_state)

# Find the way to reach the good address
good_address = 0x000013BA

# Avoiding this address
avoid_address = 0x000013C8
sm.explore(find=good_address, avoid=avoid_address)
print(sm)

embed()

# found = sm.found[0]
# found.posix.dumps(0)
