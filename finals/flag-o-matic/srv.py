from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import asyncio
import random
from binascii import hexlify
from functools import partial
from hashlib import sha512
from concurrent.futures import ProcessPoolExecutor

srand = random.SystemRandom()

be = default_backend()
flag = "midnight{Egad! You found out my decryption key! I'm done for :( Oh well, anyways I never cared about them flags so enjoy mine.}"

#Make the flag an integer
flag = int(hexlify(flag.encode()).decode(),16)

async def doprint(w,s):
    w.write(s.encode())
    await w.drain()

async def proof(l,r,w):
    c1 = srand.getrandbits(128)
    c2 = srand.getrandbits(128)
    await w.print("Please give me a integer so that the sha512 of (%d||i||%d) contains RSA\n" % (c1,c2))
    p = await r.readline()
    if b"RSA" in sha512(b"%d%d%d"%(c1,int(p),c2)).digest():
        await w.print("Correct\n")
        return True
    else:
        await w.print("Fail\n")
        return False

def chall_vals():
    ex = srand.choice([5,7,13,17,19,23,29,37,43,47,53,59,67,73,79,83,89,97])
    pk = rsa.generate_private_key(public_exponent=ex, key_size=1024, backend=be)
    pn = pk.private_numbers().public_numbers
    c =  pow(flag,pn.e,pn.n)
    return (c,pn.e,pn.n)

async def chall(l,r,w):
    c,e,n = await l.run_in_executor(None,chall_vals)
    await w.print("Here is your flag: c=%d e=%d n=%d\n" % (c,e,n))

async def handle(l,r,w):
    w.transport.set_write_buffer_limits(0)
    w.print = partial(doprint,w)
    try:
        if await proof(l,r,w):
            await chall(l,r,w)
    except Exception as e:
        print(e)
        pass
    finally:
        w.write_eof()
        w.close()

with ProcessPoolExecutor() as executor:
    loop = asyncio.get_event_loop()
    loop.set_default_executor(executor)
    coro = asyncio.start_server(partial(handle,loop), '0.0.0.0', 1254, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
