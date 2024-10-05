#!/usr/bin/python3

import angr
import sys
import claripy

def solve(elf_binary="./binary.elf"):
	project = angr.Project(elf_binary) #load up binary
	arg = claripy.BVS('arg',8*0x20) #set a bit vector for argv[1]

	initial_state = project.factory.entry_state(args=[elf_binary,arg]) #set entry state for execution
	simulation = project.factory.simgr(initial_state) #get a simulation manager object under entry state
	simulation.explore(find=is_successful) #confine search path using our "Jackpot" criteria defined below

	print("[i] >(%d)" % (len(simulation.found))) #some debug printing
	if len(simulation.found) > 0: #if we find that our 'found' array is not empty then we have a solution!
		for solution_state in simulation.found:	#loop over each solution just for interest sake
			print("[>>] {!r}".format(solution_state.solver.eval(arg,cast_to=bytes))) #print the goodness!

def is_successful(state):
	output = state.posix.dumps(sys.stdout.fileno()) #grab the screen output everytime Angr thinks we have a solution
	if b'tribe' in output:
		return True
	return False
if __name__=="__main__":
	if len(sys.argv) < 2:
		print("[*] need 2 arguments\nUsage: %s [binary path] [target address]")

	solve(sys.argv[1]) #pls work