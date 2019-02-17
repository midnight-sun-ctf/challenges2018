import itertools

n2l = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
l2n = {k: v for v,k in enumerate(n2l)}

def encrypt(msg,key):
    keyit = filter(lambda x: x in l2n, itertools.chain(key,msg))
    return ''.join(l if l not in l2n else n2l[(l2n[next(keyit)]+l2n[l]) % len(n2l)] for l in msg)
