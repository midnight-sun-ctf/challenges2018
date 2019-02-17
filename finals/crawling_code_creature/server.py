from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder
from flask import Flask

import hashlib

BLOCK_SIZE = 16
FLAG = 'midnight{c4n_you_r3v1ve_4_d34d_snek}'.encode('ascii')
encoder = PKCS7Encoder()
m = encoder.encode(FLAG)
KEY = hashlib.sha256('THE_SUPER_SECRET_KEY'.encode('ascii')).digest()

aes = AES.new(KEY)
cipher = aes.encrypt(m)

app = Flask(__name__)

@app.route("/message")
def message():
    return cipher.encode('hex')

@app.route("/key")
def key():
    return KEY.encode('hex')
