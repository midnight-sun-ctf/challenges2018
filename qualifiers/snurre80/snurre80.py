class Snurre80:

    """
        Snurre80 is a proprietary stream cipher designed for
        low-power devices, i.e., in Internet of Things contexts.
        More importantly, it offers an incredibly high security
        level of 2^80 (who would need more?).

        It has the following structure:

                      +--------+----+------+
                      |        |    |      |
                    +---+---+-   -+---+    |
                    |   |   | ... |   | <--+
                    +---+---+-   -+---+
                      |   |
                     +---------------+
                     |       f       | --> c
                     +---------------+

        Snurre80 is resistant to distinguishing attacks, since
        it uses a non-linear(tm) boolean function f as filtering
        output function.

        Snurre80 is quantum resistant and blockchain ready. It 
        is the stream cipher of the future. It is 100 % cyber.
        We charge a reasonble fee of $0.00001 / encrypted bit.

                                            -- The Designers
    """

    def __init__(self, key):
        self.state = key
        self.mask = 1284576224436276739441733
        self.nbits = self.mask.bit_length()-1

    def output(self):
        var = bin(self.state)[2:].zfill(self.nbits)
        v = [int(v) for v in var]
        return v[0] ^ v[1] ^ v[2] ^ v[31] ^ \
               v[1]&v[2]&v[3] ^ \
               v[25]&v[31]&v[32]&v[33]&v[34]
               
    def __str__(self):
        j = 0
        poly = []
        x = self.mask
        while x > 0:
            if x & 1:
                poly = ["x^{}".format(j)] + poly
            x >>= 1
            j += 1
        return " + ".join(poly)

    def keystream(self, n):
        for _ in xrange(n):
            self.state = (self.state << 1)
            xor = self.state >> self.nbits
            if xor != 0:
                self.state ^= self.mask
            yield self.output()


# Generate a sequence of 800 bits, with a random key.
key = int(os.urandom(10).encode('hex'), 16)
cipher = Snurre80(key)
z = [c for c in cipher.keystream(800)]

# Additionally, this may help you solve the CAPTCHA.
def solve_proof_of_work(prefix):
    i = 0
    while True:
        if sha256(prefix+str(i)).digest()[:3] == "\x00\x00\x00":
            return str(i)
        i += 1
