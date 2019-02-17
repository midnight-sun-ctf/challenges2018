#!/usr/bin/env python
import struct
from PIL import Image

"""
convert -alpha off -size 500x500 caption:"Some text here" infile.bmp

itoa
b *0x00000000004018ED

itoa->cpy
b *0x000000000040191B

encrypt???
b *0x0000000000400F20


AAAA BBBB CCCC
 1     2     3

A1BBBB2CCCC3
"""

#im = Image.open('Leak.bmp')

with open('Leak.bmp', 'rb') as fin:
    data = fin.read()

def get_msb(b):
    return (b>>7)&1

def bits2byte(bits):
    res = 0
    for i in range(len(bits)):
        #res |= bits[i] << (len(bits)-i-1)
        res |= (bits[i] << i)
    return res

def decode_data(data, state):
    data = [get_msb(ord(c)) for c in data]
    #print(data)

    bits = []
    i = 0
    if state == 0:
        bits.append(data[i])
        i += 4
    elif state == 1:
        bits.append(data[i+1])
        bits.append(data[i+4+2])
        bits.append(data[i+4+4+3])
        i += 3*4
    elif state == 2:
        bits.append(data[i+2])
        bits.append(data[i+4+3])
        i += 2*4

    while i+12 < len(data):
        bits.append(data[i+1])
        bits.append(data[i+4+2])
        bits.append(data[i+4+4+3])
        i+=4*3
    data = bits

    print(data)
    data = [data[i:i+8] for i in range(0, len(data), 8)]
    print(data)
    data = [bits2byte(b) for b in data]
    print(data)
    data = [chr(b) for b in data]
    
    return ''.join(data)


m1 = decode_data(data[137:137+4*8*6], 0)
m1 = int(m1[:m1.find('\x00')])
print(m1)

offset = 133 + 4*m1
length = 100
print('Offset: %x' % offset)
m2 = decode_data(data[offset:offset+4*8*length], 0)
print(repr(m2))

m2 = decode_data(data[offset:offset+4*8*length], 1)
print(repr(m2))

m2 = decode_data(data[offset:offset+4*8*length], 2)
print(repr(m2))