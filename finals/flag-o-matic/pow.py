from hashlib import sha512
import concurrent.futures

#Hey, this is klondike here!
#I'd like to apologize for asking you to solve a proof of work.
#Sadly generating the requests is taking a bit more CPU than I wanted hence this requirement.
#The PoW is quite simple anyways so you should be able to solve it quite fast.
#You may also want to consider using a processExecutor to speed up the search of a valid i :D

#Here is some simple code to solve the proof of work, just send i followed by a new line :D
def solve_proof(c1,c2,i=0):
    while b"RSA" not in sha512(b"%d%d%d"%(c1,i,c2)).digest():
        i = i + 1
    return i

#If you have multiple processors you may want to use this one instead :D
def parallel_solve_proof(c1,c2):
    with concurrent.futures.ProcessPoolExecutor() as e:
        i = next(concurrent.futures.as_completed((e.submit(solve_proof,c1,c2,i=i) for i in range(0,(e._max_workers or 1)*1000000,1000000)))).result()
        e.shutdown(wait=False)
        return i
