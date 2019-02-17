#!/bin/bash

VERSION="3"
KERNEL="linux-3.18.102"
ARCHIVE="$KERNEL.tar.xz"

if [ ! -f $ARCHIVE ]
then
    wget "https://cdn.kernel.org/pub/linux/kernel/v$VERSION.x/$ARCHIVE"
fi

if [ ! -f $ARCHIVE ]
then
    echo "\e[1;31merror:\e[0;0m Cannot download kernel sources"
    exit -1
fi

if [ ! -d "./kernel" ]
then
    tar -xJvf $ARCHIVE
    ln -s $KERNEL "./kernel"
fi

if [ ! -d "./randumb" ]
then
    mkdir "./randumb"
fi

if [ ! -f "randumb/zImage" ]
then
    cd "./kernel"
    make clean
    make mrproper
    make ARCH=arm CROSS_COMPILE=arm-none-linux-gnueabihf- vexpress_defconfig
    make ARCH=arm CROSS_COMPILE=arm-none-linux-gnueabihf- menuconfig
    # -> Networking support=n
    # -> Device Drivers
    #    -> Serial ATA and Parallel ATA drivers (libata)=n
    #    -> Hardware Monitoring support=n
    #    -> Voltage and Current Regulator Support=n
    #    -> Sound card support=n
    #    -> USB support=n
    #    -> MMC/SD/SDIO card support=n
    #    -> LED Support=n
    #    -> IOMMU Hardware Support=n
    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- all
    cp "./arch/arm/boot/zImage" "../randumb/"
fi
