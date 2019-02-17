ROOT_DIR=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
CHALL="flitbip"
KERNEL="linux-4.17"
KERNEL_ARCHIVE="$(KERNEL).tar.xz"
KERNEL_VERSION="4"
BUSYBOX="busybox-1.28.2"
BUSYBOX_ARCHIVE="$(BUSYBOX).tar.bz2"
LIBC="glibc-2.23"
LIBC_ARCHIVE="$(LIBC).tar.xz"
LIBC_BUILD="$(LIBC)_build"

.PHONY: all prepare kernel busybox libc disk clean

all: prepare kernel busybox libc disk
	#
clean:
	if [ -d "./build/$(KERNEL)" ]; then rm -rf "./build/$(KERNEL)"; fi;
	if [ -d "./build/$(BUSYBOX)" ]; then rm -rf "./build/$(BUSYBOX)"; fi;
	if [ -d "./build/$(LIBC)" ]; then rm -rf "./build/$(LIBC)"; fi;
	if [ -d "./build/$(LIBC_BUILD)" ]; then rm -rf "./build/$(LIBC_BUILD)"; fi;
	if [ -d "./build/$(LIBC_BUILD)" ]; then rm -rf "./build/$(LIBC_BUILD)"; fi;
	if [ -d "./build/$(CHALL)" ]; then rm -rf "./build/$(CHALL)"; fi;
kernel:
	if [ ! -d "./build/$(CHALL)" ]; then mkdir "./build/$(CHALL)"; fi;
	if [ ! -d "./build/$(KERNEL)" ]; then tar -C "./build/" -xJvf "./build/$(KERNEL_ARCHIVE)"; fi;
	cp -R "./src/kernel/." "./build/$(KERNEL)/"
	$(MAKE) -C "./build/$(KERNEL)" clean
	$(MAKE) -C "./build/$(KERNEL)" -j8
	cp "./build/"$(KERNEL)"/arch/x86/boot/bzImage" "./build/"$(CHALL)"/kernel"
busybox:
	if [ ! -d "./build/$(BUSYBOX)" ]; then tar -C "./build/" -xjvf "./build/$(BUSYBOX_ARCHIVE)"; fi;
	cp -R "./src/busybox/." "./build/$(BUSYBOX)/"
	$(MAKE) -C "./build/$(BUSYBOX)" clean
	$(MAKE) -C "./build/$(BUSYBOX)" -j8
	$(MAKE) -C "./build/$(BUSYBOX)" install
libc:
	if [ ! -d "./build/$(LIBC)" ]; then tar -C "./build/" -xJvf "./build/$(LIBC_ARCHIVE)"; fi;
	if [ ! -d "./build/$(LIBC_BUILD)" ]; then mkdir "./build/$(LIBC_BUILD)"; fi;
	cd "./build/$(LIBC_BUILD)" && ../$(LIBC)/configure --prefix=
	$(MAKE) -C "./build/$(LIBC_BUILD)" -j8
	$(MAKE) -C "./build/$(LIBC_BUILD)" install install_root=$(ROOT_DIR)"build/"$(BUSYBOX)"/_install"
	cp /lib/x86_64-linux-gnu/libgcc_s.so.1 $(ROOT_DIR)"build/"$(BUSYBOX)"/_install/lib"

	rm -rf ./build/$(BUSYBOX)/_install/lib/libBroken*
	rm -rf ./build/$(BUSYBOX)/_install/lib/libn*
	rm -rf ./build/$(BUSYBOX)/_install/lib/libm*
	rm -rf ./build/$(BUSYBOX)/_install/lib/libcrypt*
	rm -rf ./build/$(BUSYBOX)/_install/lib/audit*
	rm -rf ./build/$(BUSYBOX)/_install/lib/gconv*
	rm -rf ./build/$(BUSYBOX)/_install/lib/*.a
	rm -rf ./build/$(BUSYBOX)/_install/lib/M*
	rm -rf ./build/$(BUSYBOX)/_install/lib/S*
	rm -rf ./build/$(BUSYBOX)/_install/lib/c*
	rm -rf ./build/$(BUSYBOX)/_install/lib/g*
	rm -rf ./build/$(BUSYBOX)/_install/include

	if [ ! -d $(ROOT_DIR)"build/"$(BUSYBOX)"/_install/lib64" ]; then mkdir $(ROOT_DIR)"build/"$(BUSYBOX)"/_install/lib64"; fi;
	cd $(ROOT_DIR)"build/"$(BUSYBOX)"/_install/lib64" && ln -s ../lib/ld-2.23.so ld-linux-x86-64.so.2
disk:
	if [ ! -d "./build/$(CHALL)" ]; then mkdir "./build/$(CHALL)"; fi;
	cd "./build/"$(BUSYBOX)"/_install/" && mkdir -p proc sys usr/lib
	cp -R "./src/rootfs/main/." "./build/"$(BUSYBOX)"/_install/"
	#cp -R "./src/rootfs/dist/." "./build/"$(BUSYBOX)"/_install/"
	cp "./build/"$(KERNEL)"/System.map" "./build/"$(BUSYBOX)"/_install/boot/."
	cp "./src/kernel/chall/flitbip.c" "./build/"$(BUSYBOX)"/_install/src/"

	chmod +x "./build/"$(BUSYBOX)"/_install/init"

	chmod 440 ./build/$(BUSYBOX)/_install/root/*
	chmod 700 ./build/$(BUSYBOX)/_install/root

	cd "./build/"$(BUSYBOX)"/_install/" && find . -print0 | cpio --null -ov --format=newc | gzip -9 > "../../"$(CHALL)"/initrd"
	cp "./src/run.sh" "./build/$(CHALL)/run.sh"
prepare:
	if [ ! -d "./build" ]; then mkdir "./build"; fi;
	if [ ! -f "./build/$(KERNEL_ARCHIVE)" ]; then wget -P "./build/" "https://cdn.kernel.org/pub/linux/kernel/v$(KERNEL_VERSION).x/$(KERNEL_ARCHIVE)"; fi;
	if [ ! -f "./build/$(BUSYBOX_ARCHIVE)" ]; then wget -P "./build/" "https://busybox.net/downloads/$(BUSYBOX_ARCHIVE)"; fi;
	if [ ! -f "./build/$(LIBC_ARCHIVE)" ]; then wget -P "./build/" "https://ftp.gnu.org/gnu/libc/$(LIBC_ARCHIVE)"; fi;
