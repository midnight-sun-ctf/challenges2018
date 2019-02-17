# hashcash by b0bb

A simple double buffer overflow pwn challenge that hopefully teaches a little trick to people who may be new to memory corruption on RISC processors.

![HashCash Screen Capture](https://github.com/ZetaTwo/midnightsunctf/raw/master/challenges/hashcash/hashcash.png)

### Compiling notes

The binary cannot be statically linked or it will ruin the trick with the stack canary. Obviously to cross compile the target for ARM, the cross compilation packages will be required:

```bash
sudo apt-get install gcc-arm-linux-gnueabi
```

The binary needs `openssl` in order to compile. Here is how to cross compile `openssl`:

```bash
git clone https://github.com/openssl/openssl
cd openssl
git checkout OpenSSL_1_0_2
export CROSS=arm-linux-gnueabi
export AR=${CROSS}-ar
export AS=${CROSS}-as
export CC=${CROSS}-gcc
export CXX=${CROSS}-g++
export LD=${CROSS}-ld
./Configure linux-generic32 --prefix=/usr/${CROSS} --openssldir=/usr/${CROSS}/openssl --cross-compile-prefix=/usr/bin/${CROSS}-
make
sudo make install
```

At that point you can just compile the binary with `make` and the `openssl` dependencies will be statically linked.

### Running

To run the docker container just do `docker-compose up` from the `docker` folder. The service will be on port `24680`.

### Distributing

All the files the player will need are in `challenge/distribute.tar.gz`. The package includes the required libraries (`libcrypto` and `libc`) as well as the binary.

### Flaw

**Spoiler Alert:** I am about the explain the flaw

There are two buffer overflows present:

1. The array of hashes stored on the stack.
2. The input read into the `.data` section.

There is a stack canary present but the idea is to use the second buffer overflow to overwrite the value the canary is checked against (since it is stored in writable memory, `.bss`). Once the attacker is that far, they can just ROP the rest, however, the stack overflow will be md5 hashes to make it a little more interesting.
