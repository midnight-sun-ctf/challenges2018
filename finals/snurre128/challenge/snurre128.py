import os

class Snurre128:

    """
        Snurre128 is a proprietary stream cipher designed for
        high-sensitive applications such as top-secret classified
        government data. It is recommended by top cryptographers
        along the world.

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

        Snurre128 is resistant to *all* attacks, since it uses
        a perfect boolean function f as output function.

        Snurre128 is quantum secure and blockchain ready. It 
        is the stream cipher of the future. It is 100 % cyber.
        We charge a reasonable fee of $0.00001 / encrypted bit.


                                            -- The Designers
    """

    def __init__(self, key):
        self.state = key
        self.mask = 528457622443627673964173138273112871261
        self.nbits = self.mask.bit_length()-1

    def output(self):
        var = bin(self.state)[2:].zfill(self.nbits)
        v = [int(v) for v in var]
        return v[0] ^ v[1] ^ v[2] ^ v[31] ^ \
               v[1]&v[2]&v[3]&v[64]&v[123] ^ \
               v[25]&v[31]&v[32]&v[126]
               
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
