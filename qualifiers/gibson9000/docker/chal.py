#!/usr/bin/env python

import sys, pprint, time
from hexdump import hexdump as hexprint

data = [0]*128
ip = 0 
dp = 0
heat = 0
debug = False

maxheat = 100

instructions = {
        "+": ("CHANGE-DP", 4),      # add to dp
        "*": ("CHANGE-DPV", 7),     # add to data[dp]
        "_": ("MAYBE-JUMP", 2),     # jump if data == 0, otherwise skip
        "X": ("PRINT", 9),          # print string
        "M": ("MEDITATE", -1),      # decrease heat
        "D": ("DEBUG", 5),          # turn on debugging
}

def toNumber(x):
    pos = "01234567"
    neg = "89ABCDEF"

    if x in pos:
        return pos.find(x)

    if x in neg:
        return -neg.find(x)

    print "ERROR: Invalid number %s" % x
    sys.exit(1)


def dostep():
    global program, data, ip, dp, heat, debug

    while heat > maxheat:
        if debug:
            print "WARNING: CPU overheating! Idling to reduce temperature..."
        time.sleep(3)
        heat -= 1

    if ip < 0:
        print "ERROR: IP underflow (%d)" % (ip,)
        sys.exit(1)

    if ip + 1 >= len(program):
        print "ERROR: IP overflow (%d)" % (ip,)
        sys.exit(1)

    opcode = program[ip]
    parameter = toNumber(program[ip+1])

    if opcode not in instructions:
        print "Invalid instruction at %d: %s" % (ip, opcode)
        sys.exit(1)

    (instruction, instrheat) = instructions[opcode]

    if debug:
        print "------------------------------------------------"
        print "IP: %d, DP: %d" % (ip, dp)
        print "Instruction: [%s%s] %s %d" % (program[ip], program[ip+1], instruction, parameter)
        print "Heat: %d/%d" % (heat, maxheat)
        print "Data:"
        hexprint("".join([chr(x) for x in data]))
        print "------------------------------------------------"

    ip += 2

    if instruction == "CHANGE-DP":
        dp += parameter

        while dp < 0:
            dp += len(data)

        dp %= len(data)
        #print "Setting dp to %d" % (dp)
    elif instruction == "CHANGE-DPV":
        val = data[dp]
        val += parameter

        while val < 0:
            val += 256

        val %= 256
        #print "Writing %d to dp=%d" % (val, dp)
        data[dp] = val
    elif instruction == "MAYBE-JUMP":
        val = data[dp]
        #print "Maybe Jump, with val == %d" % (val,)

        if val == 0:
            pass
        else:
            ip += 2 * parameter
            #print "Jumping %d instructions" % (parameter,)
    elif instruction == "PRINT":
        s = "".join([chr(x) for x in data if x > 0])
        print "Result:"
        print eval('"' + s + '"')
        print "Done."
        sys.exit(0)
    elif instruction == "MEDITATE":
        time.sleep(0.01)
        if debug:
            print "<<< Heat decreased by %d through meditation, was at %d >>>" % (instrheat, heat)
    elif instruction == "DEBUG":
        if not debug:
            print "Enabling debug mode"
            debug = True
        else:
            print "Disabling debug mode"
            debug = False

    heat += instrheat
    if heat < 0:
        heat = 0


if __name__ == "__main__":
    global program
    program = sys.stdin.readline().strip()

    while True:
        dostep()
