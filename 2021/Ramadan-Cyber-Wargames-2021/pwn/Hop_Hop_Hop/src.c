#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

// Global counter
int *COUNTER;

// Helper functions
void add_500() { printf("Adding 500...\n"); *COUNTER += 500; return; }
void add_20() { printf("Adding 20...\n"); *COUNTER += 20; return; }
void add_2() { printf("Adding 2...\n"); *COUNTER += 2; return; }
void sub_100() { printf("Subtracting 100...\n"); *COUNTER -= 100; return; }
void sub_10() { printf("Subtracting 10...\n"); *COUNTER -= 10; return; }
void sub_5() { printf("Subtracting 5...\n"); *COUNTER -= 5; return; }
void sub_1() { printf("Subtracting 1...\n"); *COUNTER -= 1; return; }


// Flag Checker function
void check_flag()
{
	if (*COUNTER == 1337)
	{
		//Congratulations!
		printf("Congratulations, you earned the flag!\n");
		printf("%s\n", "NotTheRealFlag");
	} else {
		printf("COUNTER is not equal to 1337! It is equal to %d\n", *COUNTER);
	}
}

void get_input()
{
	char buffer[30];
	printf("Are you ready to dive into the rabbit hole?\nSay your purpose: ");
	gets(buffer);
	printf("\nYou claim your purpose is: %s\n", buffer);
}

int main()
{
	COUNTER = malloc(sizeof(int));
	*COUNTER = 0;
	get_input();
	printf("After you spoke your purpose, the COUNTER variable is now equal to: %i\n", COUNTER);
	printf("May the stack be with you.");
	return 0;
}