#include "VirtualMachine.h"

#include <fcntl.h>
#include <sys/stat.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

/*
VM Reversing Challenge
*/

unsigned char* PROGRAM;

int main(int argc, char** argv) {
	if (argc < 2) {
		printf("Usage: %s <fname>\n", argv[0]);
		return 1;
	}

	int fd = open(argv[1], O_RDONLY);
	if (fd == -1) {
		printf("File %s not found\n", argv[1]);
		return 1;
	}

	struct stat st;
	fstat(fd, &st);
	
	PROGRAM = (unsigned char*)malloc(st.st_size);
	read(fd, PROGRAM, st.st_size);

	VirtualMachine vm = VirtualMachine(PROGRAM, st.st_size);
	vm.run();

	return 0;
}
