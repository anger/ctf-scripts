#! /usr/bin/env python3

from z3 import *

flag_length = 22

F = [ BitVec("F_%s" % i, 32) for i in range(flag_length) ]
# print(F)

s = Solver()

s.add(F[18] * F[7] & F[12] ^ F[2] == 36)
s.add(F[1] % F[14] - F[21] % F[15] == -3)
s.add(F[10] + F[4] * F[11] - F[20] == 5141)
s.add(F[19] + F[12] * F[0] ^ F[16] == 8332)
s.add(F[9] ^ F[13] * F[8] & F[16] == 113)
s.add(F[3] * F[17] + F[5] + F[6] == 7090)
s.add(F[21] * F[2] ^ F[3] ^ F[19] == 10521)
s.add(F[11] ^ F[20] * F[1] + F[6] == 6787)
s.add(F[7] + F[5] - F[18] & F[9] == 96)
s.add(F[12] * F[8] - F[10] + F[4] == 8277)
s.add(F[16] ^ F[17] * F[13] + F[14] == 4986)
s.add(F[0] * F[15] + F[3] == 7008)
s.add(F[13] + F[18] * F[2] & F[5] ^ F[10] == 118)
s.add(F[0] % F[12] - F[19] % F[7] == 73)
s.add(F[14] + F[21] * F[16] - F[8] == 11228)
s.add(F[3] + F[17] * F[9] ^ F[11] == 11686)
s.add(F[15] ^ F[4] * F[20] & F[1] == 95)
s.add(F[6] * F[12] + F[19] + F[2] == 8490)
s.add(F[7] * F[5] ^ F[10] ^ F[0] == 6869)
s.add(F[21] ^ F[13] * F[15] + F[11] == 4936)
s.add(F[16] + F[20] - F[3] & F[9] == 104)
s.add(F[18] * F[1] - F[4] + F[14] == 5440)
s.add(F[8] ^ F[6] * F[17] + F[12] == 7104)
s.add(F[11] * F[2] + F[15] == 6143)

flag = 'INTIGRITI{...........}'

for k, v in zip(range(len(flag)), flag):
#    print(k, v)
    if v != '.':
        s.add(F[k] == ord(v))
# print(s)

if s.check() == sat:
    m = s.model()
#    print(m)
    for char in [m.evaluate(F[j]).as_long() for j in range(flag_length)]:
        print(chr(char), end='')
    print()
else:
    print ("failed to solve")

# INTIGRITI{tHr33_Z_FTW}
