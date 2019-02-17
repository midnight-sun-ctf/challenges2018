from Crypto.Cipher import AES
import requests
r1 = requests.get('http://localhost:5000/message')
m = r1.text.strip().decode('hex')
r2 = requests.get('http://localhost:5000/key')
k = r2.text.strip().decode('hex')
aes = AES.new(k)
ae.decrypt(m)
