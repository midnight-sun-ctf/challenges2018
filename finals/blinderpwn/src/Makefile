CC=gcc
CFLAGS=-m32 -pie

blinderpwn: blinderpwn.c
	$(CC) -o blinderpwn blinderpwn.c $(CFLAGS)

run:
	socat TCP-LISTEN:31337,reuseaddr,fork EXEC:./blinderpwn