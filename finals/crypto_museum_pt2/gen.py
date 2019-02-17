import itertools
import collections

n2l = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
l2n = {k: v for v,k in enumerate(n2l)}

def encrypt(msg,key):
    keyit = filter(lambda x: x in l2n, itertools.chain(key,msg))
    return ''.join(l if l not in l2n else n2l[(l2n[next(keyit)]+l2n[l]) % len(n2l)] for l in msg)

def decrypt(emsg,key):
    keyq = collections.deque(filter(lambda x: x in l2n, key))
    rv = collections.deque()
    for el in emsg:
        if el not in l2n:
            rv.append(el)
        else:
            nl = n2l[(l2n[el]-l2n[keyq.popleft()]) % len(n2l)]
            keyq.append(nl)
            rv.append(nl)
    return ''.join(rv)

with open("key.txt","r") as f:
    key = f.read()

with open("msg.txt","r") as f:
    msg = f.read()

emsg = encrypt(msg,key)

with open("emsg.txt","w") as f:
    f.write(emsg)

with open("emsg.txt","r") as f:
    emsg = f.read()

with open("key.txt","r") as f:
    key = f.read()

dmsg = decrypt(emsg,key)

if dmsg == msg and emsg != msg:
    print("Done!")
