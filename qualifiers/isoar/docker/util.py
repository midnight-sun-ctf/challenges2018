from werkzeug.routing import BaseConverter
from flask import abort, make_response
from functools import wraps


import hashlib, string

class AlphanumConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(AlphanumConverter, self).__init__(url_map)
        self.regex = "[a-zA-Z0-9]+"

def verify_hash(prefix=None, suffix=None):
    def check_hash_decorator(fn):
        @wraps(fn)
        def wrapper(password, proof):
            fullstr = "{}{}".format(password, proof)
            h = hashlib.sha256(fullstr.encode("utf8")).hexdigest()
            if (prefix == None or h.startswith(prefix.lower())) and (suffix == None or h.endswith(suffix.lower())):
                return fn(password, proof, h)
            else:
                abort(make_response(("ERROR: Invalid proof of work", 400, [])))
        return wrapper
    return check_hash_decorator

# well... it's not random()
def calculate_score(word):
    out = (sum([ord(x) for x in word]) % 50) + (len(word) * 3)
    if out > 100:
        out = 100
    
    return out

def calculate_hints(wordlist, word):
    out = []
    wordcount = len(wordlist)
    wordlen = len(word)

    def numlc(s):
        return len([c for c in s if c in string.ascii_lowercase])
    def numuc(s):
        return len([c for c in s if c in string.ascii_uppercase])
    def numdigits(s):
        return len([c for c in s if c in string.digits])

    out += ["The given password has {} characters".format(wordlen)]
    out += ["The given password has {} lowercase characters".format(numlc(word))]
    out += ["The given password has {} uppercase characters".format(numuc(word))]
    out += ["The given password has {} digits".format(numdigits(word))]
    
    out += ["The length of the given password equals {} out of {} known passwords".format(len([x for x in wordlist if len(x) == wordlen]), wordcount)]
    out += ["The given password is longer than {} out of {} known passwords".format(len([x for x in wordlist if len(x) < wordlen]), wordcount)]
    out += ["The given password is shorter than {} out of {} known passwords".format(len([x for x in wordlist if len(x) > wordlen]), wordcount)]

    ranks = ["first", "second", "third", "fourth", "fifth"]

    for i in range(len(ranks)):
        if wordlen > i:
            out += ["The {} character of the given password occurs in {} out of {} known passwords".format(ranks[i], len([x for x in wordlist if word[i] in x]), wordcount)]

    out += ["The last character of the given password occurs in {} out of {} known passwords".format(len([x for x in wordlist if word[-1] in x]), wordcount)]
    out += ["The given password occurs as part of {} out of {} known passwords".format(len([x for x in wordlist if word in x]), wordcount)]
    out += ["{} out of {} known passwords are suffixed with the given password".format(len([x for x in wordlist if x.endswith(word)]), wordcount)]
    out += ["The given password has the same amount of lowercase characters as {} out of {} known passwords".format(len([x for x in wordlist if numlc(word) == numlc(x)]), wordcount)]
    out += ["The given password has the same amount of uppercase characters as {} out of {} known passwords".format(len([x for x in wordlist if numuc(word) == numuc(x)]), wordcount)]
    out += ["The given password has the same amount of digits as {} out of {} known passwords".format(len([x for x in wordlist if numdigits(word) == numdigits(x)]), wordcount)]

    return out
