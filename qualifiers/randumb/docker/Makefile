containername := randumb
dockeropts := -p 13579:13579

install:
	docker build -t $(containername) .

uninstall:
	docker rmi $(containername)

run:
	docker run --rm -ti $(dockeropts) $(containername)
