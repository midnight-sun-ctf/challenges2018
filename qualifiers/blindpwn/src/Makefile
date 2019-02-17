CC=gcc
CFLAGS=-no-pie -m32

blindpwn: blindpwn.c
	$(CC) -o blindpwn blindpwn.c -static $(CFLAGS)

run:
	socat TCP-LISTEN:31337,reuseaddr,fork EXEC:./blindpwn
