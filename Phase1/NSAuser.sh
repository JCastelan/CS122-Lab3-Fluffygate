#!/bin/bash

#port# must be >=55443
portNum=55543

./NSAlistener.sh $portNum &

while read encryptedPass
do
	#echo $encryptedPass
	#echo setting up listener at $startPort to decrypt $encryptedPass
	#nc -l 128.114.59.29 $startPort & >> resultsFromNSA.txt

	echo sending request to NSA
	echo $encrpytedPass 128.114.59.29 $portNum | nc 128.114.59.42 2001
	#((portNum+=1))
done < passwd.crypt

echo DONE


