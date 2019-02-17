containername := passwordmeter
cmd := /bin/bash
#cmd := /home/ctf/server.py

dockeropts := -p 8000:8000 -v $$PWD:/data

install:
	docker build -t $(containername) .

uninstall:
	docker rmi $(containername)

run:
	docker run --rm -ti $(dockeropts) $(containername) $(cmd)

