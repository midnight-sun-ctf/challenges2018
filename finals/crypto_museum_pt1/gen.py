import random
srand = random.SystemRandom()


dict1 = "abcdefghijklmnopqrstuvwxyz"
dict2 = list(dict1)
srand.shuffle(dict2)
dict2 = "".join(dict2)

dict1 = dict1 + dict1.upper()
dict2 = dict2 + dict2.upper()


with open("key.txt","w") as f:
    f.write(dict2)

lmap = dict(zip(dict1,dict2))

with open("msg.txt","r") as f:
    msg = f.read()

emsg = "".join(map(lambda x: lmap.get(x,x),msg))

with open("emsg.txt","w") as f:
    f.write(emsg)

ilmap = {v: k for k, v in lmap.items()}

with open("emsg.txt","r") as f:
    emsg = f.read()

dmsg = "".join(map(lambda x: ilmap.get(x,x),emsg))

if dmsg == msg and emsg != msg:
    print("Done!")
