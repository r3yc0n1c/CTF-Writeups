#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void jump_here()
{
	printf("You made it! Your reward is: %s\n", getenv("FLAG"));
}

void get_input()
{
	char buffer[64];
	printf("Hey there! Can you jump to needed function?\nGive it a shot! Send your input: ");
	gets(buffer);
	printf("Your input was: %s\n", buffer);
}

int main()
{
	get_input();
	return 0;
}
