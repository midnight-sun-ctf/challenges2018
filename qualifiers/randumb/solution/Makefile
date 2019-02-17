CC=arm-linux-gnueabihf-gcc
CFLAGS=-Os -nostdlib -march=armv7-a -marm
BIN=exploit

all:
	$(MAKE) $(BIN)

$(BIN): exploit.c asm.S
	$(CC) $(CFLAGS) exploit.c asm.S -o $(BIN)

clean:
	rm -f $(BIN)
