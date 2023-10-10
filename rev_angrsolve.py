import angr
from IPython import embed

project = angr.project("./ctfd_plus", main_opts={base_addr: 0}, auto_load_libs=False)

initial_state = project.factory.entry_state()
print(initial_state)

# Start simulation
sm = project.factory.simgr(initial_state)

# Find way to reach good adresss
good_address = 0x0112E
bad_address = 0x01117
sm.explore(find=good_address, avoid=bad_address)
print(sm)
print(sm.found[0].posix.dumps(0))

embed()

