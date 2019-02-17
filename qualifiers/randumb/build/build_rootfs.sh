#!/bin/bash

BUSYBOX="busybox-1.28.2"
ARCHIVE="$BUSYBOX.tar.bz2"

if [ ! -d "./randumb" ]
then
	mkdir "./randumb"
fi

if [ ! -f $ARCHIVE ]
then
    wget "https://busybox.net/downloads/$ARCHIVE"
fi

if [ ! -f $ARCHIVE ]
then
    echo "\e[1;31merror:\e[0;0m Cannot download busybox sources"
    exit -1
fi

if [ ! -d "./busybox" ]
then
    tar -xjvf $ARCHIVE
    ln -s $BUSYBOX busybox
fi

cd busybox
if [ ! -d "./_install" ]
then
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
    # -> Settings
    #    -> Build Options
    #       -> Build static binary=y
    # -> Shells
    #    -> Use HISTFILESIZE=n
else
    rm -rf _install
fi

make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- install
cd _install
mkdir -p proc sys tmp
cp -R ../../../rootfs/main/* ./

if [ ! -z "$DIST" ]; then
    cp -R ../../../rootfs/dist/* ./
fi

chmod +x etc/init.d/rcS
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../../randumb/rootfs.img.gz

cp ../../../rootfs/chall ../../randumb/
chmod +x ../../randumb/chall

cd ../../
if [ -z "$DIST" ]; then
    yes | cp -rf ./randumb/* ../docker/
fi

if [ ! -z "$DIST" ]; then
    tar -zcvf ../challenge/distribute.tar.gz ./randumb/
else
    tar -zcvf ../challenge/release.tar.gz ./randumb/
fi