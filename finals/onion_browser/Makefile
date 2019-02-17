
.PHONY: duktape

all:
	gcc -g -O0 -m32 -Wl,-z,norelro -std=c99 -no-pie -o main -L/usr/local/lib -Iduktape/src-custom -Isrc duktape/src-custom/duktape.c -Isrc duktape/extras/console/duk_console.c main.c -lm -lcurl

duktape:
	python duktape/tools/configure.py \
      --source-directory duktape/src-input \
      --output-directory duktape/src-custom \
      --config-metadata duktape/config \
      -DDUK_USE_FASTINT