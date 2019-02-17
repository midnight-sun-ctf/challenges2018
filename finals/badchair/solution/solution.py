import json
import base64

from point import Point
from challenge import KeySplitter

splits = list()
splitter = KeySplitter(9, 5)

with open("shares.txt", "r") as f:
    shares = f.read().split("\n")

for share in shares:
    z = json.loads(share)
    x = base64.b64decode(z.get("split")[0])
    y = base64.b64decode(z.get("split")[1])
    splits.append([x,y])

print splits

# to find polynomial, you need to pick any symbol and extract coords (x,y) from all four chars. then you can guess the last, interpolate.
# then run the following code for each guess:
out = ''
for x, y in zip(splits[0][0], splits[0][1]):
    x = Point(ord(x[0]))
    y = Point(ord(y[0]))
    poly = [219, 111, 173, 31] # i cheated here and did not perform interpolation. this is a trivial task, but a bit work consuming.
    secret = y + x * Point(poly[0]) + x * x * Point(poly[1]) + x * x * x * Point(poly[2]) + x * x * x * x * Point(poly[3])
    out += chr(secret.value)
print [out]
# since a share is the constant term i.e., f(0), we have that f(0) = f(x) + ax + bx^2 + cx^3.
# so once the base_poly has been guessed, we only need one share.