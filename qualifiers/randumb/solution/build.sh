#!/bin/sh

make clean > /dev/null 2>&1
make > /dev/null 2>&1

echo ''
echo "Paste the following into the VM:"
echo "---------- BEGIN COPY ----------"
echo "cd /tmp"
cat ./exploit | bzip2 | base64 -w 1000 | while read line; do
	echo "echo '$line'>>ex.b64"
done
echo "cat ex.b64 | base64 -d | bzip2 -d > ./ex; chmod +x ./ex; ./ex"
echo "----------- END COPY -----------"
