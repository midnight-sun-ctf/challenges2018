#!/usr/bin/python
import sys
import base64
import random

from flag import FLAG

PRIME = 108184472840883904401020943518889334424878184717481619406452244785674996533934208874652037233292160135768553190793236167491422557465153941960562983148794682347029641594333936771181300450187692240242131636882060421822576482126965380361049161093445808830044584918661458510768736305779715445518716495639157769783

def _write(msg):
    sys.stdout.write(str(msg) + "\n")
    sys.stdout.flush()

def _read():
    data = sys.stdin.readline().strip()
    return data

class ZK:

    def __init__(self, secret, modulus):
        self.secret = secret
        self.modulus = modulus

    def challenge(self):
        self.challenge = random.randint(
            0, self.modulus
        )
        return self.challenge

    def concat(self, nonce):
        return int(str(self.challenge) + str(nonce))

    def generate(self, nonce, index):
        r = pow(
            self.secret, 
            self.concat(nonce), 
            self.modulus
        )
        return (r >> index) & 0x1

zk = ZK(
    int(FLAG.encode("hex"), 16), 
    PRIME
)

_write("zilch-konstigheter server starting...")

while True:

    _write("Options:")
    _write("1. Request proof")
    _write("2. Quit")

    try:
        choice = int(_read())
    except:
        break

    if choice == 1:
        _write(zk.challenge())
        _write("Enter response:")
        try:
            nonce, index = _read()
            _write(zk.generate(int(nonce), int(index)))
        except Exception as e:
            _write("Is input really two comma-separated integers? I think not...")
    elif choice == 2:
        _write("KBye.")
        break
    else:
        _write("Invalid choice.")
        break

_write("Quitting...")
sys.exit()