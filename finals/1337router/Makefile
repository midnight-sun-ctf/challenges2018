CHALL_PORT=31337
CHALL_NAME=router
CHALL_FLAG="sctf{pUts_0n_sh4d3s_w3r3_1n}"
CHALL_DEPS=""

.PHONY: all init

all:
	#gcc -fno-stack-protector $(CHALL_NAME).c zlib.c -static -o $(CHALL_NAME)
	arm-linux-gnueabi-gcc -fno-stack-protector $(CHALL_NAME).c zlib.c -static -o $(CHALL_NAME)
	cp router ~/chall
init:
	mkdir build
	mkdir dist