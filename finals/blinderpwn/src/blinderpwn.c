#include <stdio.h>


void welcome() {
	char name[64];
	char message[1024];
	printf("Welcome! What is your name? ");
	fgets(name, 64, stdin);
	printf("Hello ");
	printf(name);
	printf("\nWhat can we help you with today? ");
	fgets(message, 2*1014, stdin);
}

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);

	welcome();
	return 0;
}