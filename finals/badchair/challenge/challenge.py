import os
import json 
import base64

from flag import FLAG
from point import Point
from shamir import Shamir

class KeySplitter:
    
    def __init__(self, numshares, threshold):
        self.splitter = Shamir(numshares, threshold)
        self.numshares = numshares
        self.threshold = threshold

    def split(self, key):
        xshares = [''] * self.numshares
        yshares = [''] * self.numshares
        for char in key:
            xcords, ycords = self.splitter.split(ord(char))
            for idx in range(self.numshares):
                xshares[idx] += chr(xcords[idx])
                yshares[idx] += chr(ycords[idx])
        return zip(xshares, yshares)
    
    def jsonify(self, shares, threshold, split):
        data = {
            'shares': shares, 
            'threshold': threshold, 
            'split': [
                base64.b64encode(split[0]),
                base64.b64encode(split[1])
            ]
        }
        return json.dumps(data)

if __name__ == "__main__":
    splitter = KeySplitter(9, 5)
    splits = splitter.split(FLAG)
    for i in range(0, 4):
        print splitter.jsonify(9, 5, splits[i])


