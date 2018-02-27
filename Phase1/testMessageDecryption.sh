#!/bin/bash

#compiling
gcc -c messageDecryption.c
gcc -c crypto.c
gcc -lssl -lcrypto -o messageDecryption crypto.o messageDecryption.o 

#testing
./messageDecryption message.cipher iv.plain key.plain

echo TESTING DONE
