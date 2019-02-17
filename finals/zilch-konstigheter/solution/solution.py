from pwn import *

PRIME = 108184472840883904401020943518889334424878184717481619406452244785674996533934208874652037233292160135768553190793236167491422557465153941960562983148794682347029641594333936771181300450187692240242131636882060421822576482126965380361049161093445808830044584918661458510768736305779715445518716495639157769783

def search(s, m):
    z = int(str(s) + str(2**1025)) % (m - 1)
    x = 2**1025 - z + 1
    return x

def get_bit(i):
    r.recvline()
    r.recvline()
    r.recvline()
    r.send("1\n")
    c = r.recvline()#int()
    r.recvline()
    payload = str(search(int(c), PRIME)) + "," + str(i) + "\n"
    r.send(payload)
    return r.recvline().strip()

r = remote("52.210.10.146", 1337)
r.recvline()

bb = ""
for i in range(0, 1024):

    bb = get_bit(i) + bb
    try:
        print i, hex(int(bb, 2))[2:].decode("hex")
    except:
        pass
