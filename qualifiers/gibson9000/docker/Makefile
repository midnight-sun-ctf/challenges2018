containername := gibson9000
cmd := /bin/bash
cmd := /usr/sbin/xinetd -dontfork

dockeropts := -p 9000:9000

install:
	docker build -t $(containername) .

uninstall:
	docker rmi $(containername)

run:
	docker run --rm -ti $(dockeropts) $(containername) $(cmd)

