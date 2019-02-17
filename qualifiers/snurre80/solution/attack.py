from pwn import *
from hashlib import sha256

def parity_check(z):
    """
        Let connection polynomial P(x) be

            x^40+x^38+x^33+x^32+x^29+x^27+x^25+x^21+x^19+x^17+x^12+x^11+x^9+x^5+x^3+x+1

        There exists q_i(x) such that

            q_i(x) * P(x) = u_i(x)

        We have u_1, u_2, u_3, u_4 s.t.

            x^17399+x^13567+x^4098+1
            x^18695+x^17227+x^15407+1
            x^23961+x^12632+x^7304+1
            x^26004+x^16925+x^14176+1

        If u_1 is a parity, then (u_1)^2 is one too.

    """
    parities = [
        [17399, 13567,  4098],
        [18695, 17227, 15407],
        [23961, 12632,  7304],
        [26004, 16925, 14176],
        [32137, 27193, 13288],
        [22905, 22020, 7301],
        [16044, 34273, 34213],
        [15418, 52279, 34769],
        [33850, 28352, 52008],
        [8196, 34798, 27134],
        [8423, 6051, 31347],
        [50534, 40967, 28239],
        [851, 17212, 59395],
        [19534, 7245, 28522],
        [36256, 52379, 21882],
        [62070, 11078, 16515],
        [41194, 57613, 35660]
    ]

    p = parities[0]
    S = sum(z[i + 2*p[0]] ^ z[i + 2*p[1]] ^ z[i + 2*p[2]] ^ z[i] for i in range(0, 1000))
    return  S < 430


def solve_proof_of_work(prefix):
    i = 0
    while True:
        if sha256(prefix+str(i)).digest()[:3] == "\x00\x00\x00":
            return str(i)
        i += 1

# Solve proof of work
print("[ ] Solving proof of work...")
r = remote("localhost", 31337)
r.recvline()
prefix = r.recvline().split(":")[1].strip()
r.recvline()
suffix = solve_proof_of_work(prefix)
r.send(suffix + "\n")
print("[+] Found suffix {}".format(suffix))

# Attack cipher
print("[ ] Running attack")
r.recvline()
for i in range(0, 32):
    stream = r.recvline().strip()
    try:
        stream = [int(x) for x in stream]
    except:
        print stream
    print r.recvline()
    print r.recvline()
    print r.recvline()
    if parity_check(stream):
        r.send("1\n")
    else:
        r.send("2\n")
    print r.recvline()
