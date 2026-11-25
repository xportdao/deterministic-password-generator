import hashlib, base64, getpass

phrase = getpass.getpass("Secret phrase: ")
site = input("Service: ").strip().lower()
key = hashlib.scrypt(phrase.encode(), salt=site.encode(), n=2**17, r=8, p=1, dklen=15, maxmem=256*1024**2)
print(base64.urlsafe_b64encode(key).decode() + "aA1!")
