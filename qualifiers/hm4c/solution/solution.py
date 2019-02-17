import sys
import base64
from flag import *

from hashlib import sha256

def to_int(x):
    return int(x.encode("hex"), 16)

def h(x):
    return to_int(
        sha256(str(x)).digest()
    )

def hmac(x):
    val = to_int(x)
    key = to_int(FLAG)
    tmp = key ^ val
    return h(tmp + val)




GUESSED_LENGTH = 23
print "".join(
    chr(int(''.join(str(1*(hmac(chr(2**i) + "\x00"*j) == hmac("\x00"))) for i in xrange(8))[::-1], 2)) for j in range(GUESSED_LENGTH)
)[::-1]


from pwn import *

r = remote("34.249.127.77", 1337)
print r.recvline()
print r.recvline()
print r.recvline()
print r.recvline()
r.send("1\n")
print r.recvline()
print "r.send('AAAA')"
r.send("AAAA\n")
print r.recvline()