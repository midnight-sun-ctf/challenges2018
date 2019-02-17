from log import logTable, expTable

class Point:
        
    def __init__(self, value):
        self.value = value % 256
    
    def __add__(self, point):
        return Point(self.value ^ point.value)
    
    def __iadd__(self, point):
        self.value ^= point.value
        return self

    def __mul__(self, point):
        if point.value == 0 or self.value == 0: 
            return Point(0)
        return Point(expTable[(logTable[self.value] + logTable[point.value]) % 255])
    
    def __imul__(self, point):
        if point.value == 0 or self.value == 0: 
            self.value = 0
        else:
            self.value = expTable[(logTable[self.value] + logTable[point.value]) % 255] 
        return self

    def __div__(self, point):
        if point.value == 0: 
            raise ArithmeticError('Division by zero')
        return Point(expTable[(255 + logTable[self.value] - logTable[point.value]) % 255])
    
    def __idiv__(self, point):
        if point.value == 0: 
            raise ArithmeticError('Division by zero')
        self.value = expTable[(255 + logTable[self.value] - logTable[point.value]) % 255]
        return self