#!/bin/bash

cd ../src
make clean
make

cp randumb.h randumb.c ../rootfs/main/src/
cp randumb.ko ../rootfs/main/
