from hashlib import sha256
from pwn import *


alphanumerics = "abcdefghijklmnopqrstuvwxyz1234567890{}_-"
hashes = ["""all the hashes found in accessLog. There were a lot."""]

flag = b''


for hash in hashes:
	for c in alphanumerics:
		m = sha256()
		m.update(flag + c.encode("utf-8"))
		testhash = enhex(m.digest())
		if (testhash == hash):
			flag += c.encode("utf-8")
			print (flag)
			continue