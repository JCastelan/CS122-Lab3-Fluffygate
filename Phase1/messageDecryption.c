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
	char *eMsg = calloc(1, eMsgLength);
	char IV[bufSize];
	char keyListLine[bufSize];

	
	//storing the entire encrypted message in eMsg
	int bytesRead = fread( eMsg, 1, eMsgLength, eMsgFile);
	//printf("%d\n", bytesRead);
	//printf("[%s]\n", eMsg);

	//storing the IV 
	fgets( IV, bufSize, ivFile);
	IV[strcspn(IV, "\n")] = 0; //https://stackoverflow.com/questions/2693776/removing-trailing-newline-character-from-fgets-input
	//printf("IV: \t[%s]\n", IV);


	//finding the number of keys in the list
	int keyListLength=0;
	while( fgets( keyListLine, bufSize, keyListFile) ){ //finding number of lines
			keyListLength++;
	}
	rewind(keyListFile);

	//creating an array of buffers (and also filling it)
	char** keyArray = calloc(keyListLength, sizeof(char*));
	for( int i = 0; i < keyListLength; i++){
		keyArray[i]=calloc(1, bufSize);
		fgets( keyArray[i], bufSize, keyListFile);
		keyArray[i][strcspn(keyArray[i], "\n")] = 0;
	}

	//preparing to write results into files
	char* fileName=calloc(1,1024);

	//trying out each each key 
	for( int i = 0; i < keyListLength; i++){
		sprintf( fileName, "decryptedMessage%d.txt",i);
		printf("%s\n", fileName);
		FILE *output = fopen( fileName , "w");
		char* result=calloc(1, 2048);
		int bytesWritten = decrypt(eMsg, eMsgLength, keyListLine, IV, result);
		printf("[%s] written in %d bytes\n", result, bytesWritten);
		//fwrite( result, 1, bytesWritten, output);
		fputs( result, output);
		free(result);
		free(output);
	}
///////////////////////////////////////////////////////////////////////////////////
//	fgets( keyListLine, bufSize, keyListFile);
	//printf("keyListFile (line1): [%s]\n", keyListLine);
//	keyListLine[strcspn(keyListLine, "\n")] = 0;
	//printf("keyListFile (w/out newline): \t[%s]\n", keyListLine);

	//TRYING EVERY SUBSTRING OF OBFUSCATED KEY (PROVIDED BY FILE)
//	char* result=calloc(1,2048);
//	int bytesWritten = decrypt(eMsg, eMsgLength, keyListLine, IV, result);
//	printf("[%s] written in %d bytes\n", result, bytesWritten);
//////////////////////////////////////////////////////////////////////////////////

	//CLEANING UP
	fclose(eMsgFile);
	fclose(ivFile);
	fclose(keyListFile);
	free(eMsg);
	free(keyArray);
	return 0;
}