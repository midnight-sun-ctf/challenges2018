# VP-CHALLENGE
## Description
The Virtual Program challenge will consist of a virtual machine and a
custom binary format which is executed by said virtual machine. The
custom binary may ask the user for a password of some sort, and print
a message if the aswer is correct.

The files that will be provided to the contestants are;
`chall.o vm`

## Intended Solution
The intended solution is to reverse-engineer the opcode handlers in the
binary, writing a disassembler and then statically reversing the disassembly.

## Components
### cpp-src/Main.cpp
Sets up and executes the Virtual Machine. Execute a program by specifying a
filename like so; `./vm <filename.o>`

### cpp-src/VirtualMachine.cpp
Contains the source code for the VM. It is fairly simple, and can perform
conditional jumps, arithmetic, moving data, etc. The VM has 5 registers
and two memory segments, one for data and one for code. All arithmetic
operations as well as move operations operate on 32-bit integers, there
are no other variable sizes.

### cpp-src/VirtualMachine.h
Contains header for `VirtualMachine.cpp`, and more interestingly a description
of the instruction set that has been implemented. If you find any bugs with
regards to some instruction, this may be a useful resource. There is also
a debug switch here.

### assembler.py
Used to compile/assemble programs for the virtual machine. Usage is as follows;
`Usage: ./assembler.py <source.vp>`. The assembler starts out by calculating
offsets to labels and declaring variables, and then encodes the assembly 
instructions.

The assembler will generate a file named `<filename.o>`, and to execute it, supply
the VM with that output file.

### test.vp
Demostrates some features of the virtual machine. We begin by declaring
three variables, w, i and n. We then read two characters from
stdin, and if those two characters are equal we go to the win label.
The win label prints out the message "WIN" to stdout. The fail label
is simply an infinite loop.

## TODO
* Testing the challenge
