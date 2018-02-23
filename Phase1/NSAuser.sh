#!/bin/bash

startPort=12000

while read encryptedPass
do
	echo $encryptedPass
	echo setting up listener at $startPort
	nc -l 128.114.59.29 $startPort & >> resultsFromNSA2.txt

	echo sending request 
	echo $encrpytedPass 128.114.59.29 $startPort | nc 128.114.59.42 2001
	((startPort+=1))
done < passwords.6.crypt

echo DONE


