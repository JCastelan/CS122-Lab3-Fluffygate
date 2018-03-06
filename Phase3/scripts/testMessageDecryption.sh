#!/bin/bash

#compiling (https://stackoverflow.com/questions/34368804/what-are-the-link-options-lcrypto-and-lssl-in-compiling-programs-with-openss)
gcc -c messageDecryption.c
gcc -c crypto.c
gcc -o messageDecryption crypto.o messageDecryption.o -L /usr/local/ssl/lib -lcrypto -lssl -ldl

#testing
./messageDecryption $1 $2 $3 $4

#removing junk
rm *.o

echo TESTING DONE
