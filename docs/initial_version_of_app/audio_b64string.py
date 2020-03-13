from base64 import b64encode, b64decode

a = open("sample_5.wav", "rb").read()

#wav bytes 2 wav str
b = b64encode(a)
c = b.decode()
#wav str back 2 wav bytes
d = c.encode()
e = b64decode(d)

open("temp.wav", "wb").write(e)
