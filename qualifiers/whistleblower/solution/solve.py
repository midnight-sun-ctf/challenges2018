#!/usr/bin/env python
import requests

ciphertext = '680a2f38d93aaf86e562ab01bb6f7ef9eaf50a2e393bb2262d5d0f32541a7543bf6361220aa7cc1ad1a94efd6ed2fa99aa80c26379316199e70b6c7fbb2d9f81272fce8abf1edf8facce85a8dc89a9eb9d16ca22845545e55460d99c8fe98e383c25b9acc108ea88c7f6cf6666ccc4f56db3886ce0524b185c58aea95e59659c'
keyid = 'e845799dc6bb731000221f5e20587814'


BLOCK_SIZE = 16
DATA_URL = 'http://web.midnightsunctf.se/data'

r = requests.post(DATA_URL, json={'ciphertext': ciphertext, 'keyid': keyid})
print(r.text)

"""
r = requests.post(DATA_URL, json={'ciphertext': ciphertext, 'keyid': keyid2})
print(r.text)

r = requests.post(DATA_URL, json={'ciphertext': ciphertext2, 'keyid': keyid})
print(r.text)
"""

def attempt_message(keyid, ciphertext):
    r = requests.post(DATA_URL, json={'ciphertext': ciphertext.encode('hex'), 'keyid': keyid})
    return r.status_code == 200

def xor(a, b):
    return ''.join([chr(ord(x[0])^ord(x[1])) for x in zip(a,b)])

def modify_block(block, pos, val):
    xor_val = '\x00'*(BLOCK_SIZE-pos-1) + chr(val) + '\x00'*(pos)
    assert(len(xor_val) == BLOCK_SIZE)
    assert(len(block) == BLOCK_SIZE)
    return xor(block, xor_val)

def decrypt_message(keyid, message):
    assert(len(message)%BLOCK_SIZE == 0)
    remaining = message
    flag = ''
    while len(remaining) > 2*BLOCK_SIZE:
        prefix = remaining[:-2*BLOCK_SIZE]
        mod_block = remaining[-2*BLOCK_SIZE:-1*BLOCK_SIZE]
        suffix = remaining[-1*BLOCK_SIZE:]
        
        plaintext_block = []
        for pos in range(BLOCK_SIZE):
            cand_block = mod_block
            for prepare_pos in range(pos):
                cand_block = modify_block(cand_block, prepare_pos, plaintext_block[prepare_pos]^(pos+1))
            for c in range(1, 256):
                if pos == 0 and c^1 == 0:
                    continue
                attempt_block = modify_block(cand_block, pos, c^(pos+1))
                attempt = prefix + attempt_block + suffix
                if attempt_message(keyid, attempt):
                    plaintext_block.append(c)
                    break
            print(plaintext_block)
            #break
        assert(len(plaintext_block) == BLOCK_SIZE)
        flag += ''.join([chr(x) for x in plaintext_block])
        remaining = remaining[:-BLOCK_SIZE]
                
    return flag[::-1]


remaining = ciphertext.decode('hex')
print(decrypt_message(keyid, remaining))