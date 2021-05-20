#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void menu()
{
	void *secret_printf = printf;
	char identification[64];
	printf("--- SECTOR 13 IDENTIFICATION START ---\n");
	printf("IDENTIFY YOURSELF: ");
	fgets(identification, sizeof(identification), stdin);
	printf(identification);
	printf("IDENTIFICATION COMPLETE. REQUESTING INSTRUCTIONS...\n");
}

void get_instructions()
{
	char instructions[32];
	printf("=== REQUEST INSTRUCTIONS ===\n");
	printf("SEND INSTRUCTIONS: ");
	gets(instructions);
	printf("INSTRUCTIONS: %s\n", instructions);
	printf("THANK YOU. ENDING TRANSMISSION.\n");
}

int main()
{
	menu();
	get_instructions();
	printf("--- SECTOR 13 TRANSMISSION END ---\n");
	return 0;
}