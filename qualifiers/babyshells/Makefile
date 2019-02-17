#! /bin/bash

#	define per chall
chall_port=7777
chall_name=babyshells
flag=midnight{d0nt_d0_th3_cr1m3_1f_y0u_c4nt_d0_th3_t1m3}

all:
	gcc -z execstack -static -fno-stack-protector -std=c99 -m32 chall.c -o chall
	#arm-linux-gnueabi-gcc -static -fno-stack-protector -std=c99 chall.c -o chall-arm
	#mips-linux-gnu-gcc-5 -static -fno-stack-protector -std=c99 chall.c -o chall-mips
	cp chall ~/chall
debug:
	cp chall ~/chall
deploy:
	#	populate bin folder
	#strip chall
	#cp /lib/x86_64-linux-gnu/libc.so.6 bin/libc.so.6_$(shell md5sum /lib/x86_64-linux-gnu/libc.so.6 | cut -f1 -d ' ')
	cp chall "bin/$(chall_name)_$(shell md5sum chall | cut -f1 -d ' ')"
	tar czvf "$(chall_name).tar.gz" bin/*
	
	#	initialize docker-setup
	#cp -r ../../likvidera/misc-tools/docker-pwn "$(chall_name)_docker"
	#sed -i 's/CTF_PORT/$(chall_port)/g' "$(chall_name)_docker/ctf.xinetd"
	#sed -i 's/CTF_PORT/$(chall_port)/g' "$(chall_name)_docker/docker-compose.yml"
	#sed -i 's/CTF_NAME/$(chall_name)/g' "$(chall_name)_docker/docker-compose.yml"
	
	#	add flag and chall to docker
	#echo "$(flag)" > "$(chall_name)_docker/flag"
	#cp chall "$(chall_name)_docker/chall"
	
	#	compress deploy package
	#tar czvf "$(chall_name)_DEPLOY.tar.gz" "$(chall_name)_docker"
	#rm -rf "$(chall_name)_docker"
clean:
	rm bin/*
	rm chall
	rm "$(chall_name).tar.gz"
	rm "$(chall_name)_DEPLOY.tar.gz"