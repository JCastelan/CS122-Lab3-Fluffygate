/*This program decrypts a message
 * usage: 
 *	messageDecryption [encrypted message] [ivFile] [file containing list of possible keys]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "crypto.h"

int main(int argc, char const *argv[])
{
	//CHECKING FOR VALID USAGE
	if (argc < 3)
	{
		printf("%s\n", "Not enough args");
		printf("%s:\n%s %s\n", "usage", argv[0], "[encryptedMsgFile] [ivFile] [keyListFile]");
		exit(1);
	}

	//USING THE ARGS
	FILE* eMsgFile;
	eMsgFile=fopen(argv[1], "r");
	FILE* ivFile;
	ivFile=fopen(argv[2], "r");
	FILE* keyListFile;
	keyListFile=fopen(argv[3], "r");

	//PREPARING ITEMS FOR CRYPTO.H FUNCTIONS
	int bufSize=2048;
	int eMsgLength; //we need to keep track of the length of the encrypted message
	fseek( eMsgFile, 0L, SEEK_END);
	eMsgLength = ftell(eMsgFile);
	rewind(eMsgFile);
	int counter = eMsgLength;
	printf("%d\n", counter);
	char *eMsg = calloc(1, eMsgLength);
	char IV[bufSize];
	char keyListLine[bufSize];


	//FILLING THOSE ITEMS	
	//fgets( eMsgLine, bufSize, eMsgFile); //NEED TO LOOP AND COLLECT ENTIRE FILE
	//printf("eMsgFile (line1): [%s]\n", eMsgLine);
	int bytesRead = fread( eMsg, 1, eMsgLength, eMsgFile);
	printf("%d\n", bytesRead);
	printf("[%s]\n", eMsg);

	fgets( IV, bufSize, ivFile);
	//printf("ivFile (line1): [%s]\n", IV);
	IV[strcspn(IV, "\n")] = 0; //https://stackoverflow.com/questions/2693776/removing-trailing-newline-character-from-fgets-input
	printf("ivFile (w/out newline): \t[%s]\n", IV);

	fgets( keyListLine, bufSize, keyListFile);
	//printf("keyListFile (line1): [%s]\n", keyListLine);
	keyListLine[strcspn(keyListLine, "\n")] = 0;
	printf("keyListFile (w/out newline): \t[%s]\n", keyListLine);


	//TRYING EVERY SUBSTRING OF OBFUSCATED KEY (PROVIDED BY FILE)
	char* result=calloc(1,2048);
	int bytesWritten = decrypt(eMsg, eMsgLength, keyListLine, IV, result);
	printf("[%s] written in %d bytes\n", result, bytesWritten);

	//CLEANING UP
	fclose(eMsgFile);
	fclose(ivFile);
	fclose(keyListFile);
	free(eMsg);
	return 0;
}