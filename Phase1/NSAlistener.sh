#!/bin/bash

#port# must be >=4000
startPort=54545

#mkfifo testFifo

#while read encryptedPass
#do
#may need -k
echo listening at port $startPort
nc  -l 128.114.59.29 $startPort >listenerOutput

#done < passwd.crypt

echo DONE
