.global exit
exit:
mov %r7, #1
svc #0
bx %lr
 
.global read
read:
mov %r7, #3
svc #0
bx %lr
 
.global write
write:
mov %r7, #4
svc #0
bx %lr
 
.global open
open:
mov %r7, #5
svc #0
bx %lr
 
.global close
close:
mov %r7, #6
svc #0
bx %lr
 
.global execve
execve:
mov %r7, #11
svc #0
bx %lr
 
.global getuid
getuid:
mov %r7, #24
svc #0
bx %lr

.global mkdir
mkdir:
mov %r7, #39
svc #0
bx %lr

.global pipe
pipe:
mov %r7, #42
svc #0
bx %lr

.global ioctl
ioctl:
mov %r7, #54
svc #0
bx %lr

.global pwn
pwn:
mov %r7, #223
svc #0
bx %lr