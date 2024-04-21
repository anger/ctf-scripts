import angr
from IPython import embed
import logging
import claripy

logging.getLogger('angr').setLevel('WARN')


for i in range(11, 56):
    print(i)

    project = angr.Project("./app", main_opts={'base_addr': 0}, auto_load_libs=False)

    initial_state = project.factory.entry_state()

    flag = claripy.BVS("flag", 8*i)
    for c in flag.chop(8)[0:-1]:
        initial_state.solver.add(c >= 0x20)
        initial_state.solver.add(c <= 0x7f)

    # initial_state.solver.add(flag.chop(8)[-2] == ord('}'))
    initial_state.solver.add(flag.chop(8)[-1] == 0)

    @project.hook(0x1292, length=5)
    def scanf_username(state):
        print("scanf_username", state.regs.rsi)
        state.memory.store(state.regs.rsi, claripy.BVV("LosCapitan\x00"))

    @project.hook(0x12c1, length=5)
    def scanf_password(state):
        print("scanf_password", state.regs.rsi)
        state.memory.store(state.regs.rsi, flag)

    # Start simulation
    sm = project.factory.simgr(initial_state)

    # Find the way yo reach the good address
    good_address = 0x14a7
    avoid_address = 0x14b8
    sm.explore(find=good_address, avoid=avoid_address)

    if len(sm.found) > 0:
        found = sm.found[0]

        password = found.solver.eval(flag, cast_to=bytes).decode()
        print(f"gctf{{{password}}}")
        exit(0)