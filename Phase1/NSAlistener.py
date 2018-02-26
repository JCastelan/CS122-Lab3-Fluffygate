#!/usr/bin/env python3

#this program tries to implement the following command using python:
# nc -l 128.114.59.29 55543 >> listenerOutput

"""Sources Used:
	https://docs.python.org/2/library/socket.html
"""
import socket
import sys

HOST='localhost'#'128.114.59.29'
PORT=54545 #make sure this is the same one used by the NSA requester

s = socket.socket(socket.AF_INET, socket.SOCK_RAW)
#s.connect((HOST, PORT))
s.bind((HOST,PORT))
#s.listen(1)

s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

counter=1
phase=0 # 0->waiting for data; 1->haveStartedReceivingData
outFile = open("resultsFromNSA.txt", "w")

print 'starting loop'
while counter>0:
	if counter==1:
		data, addr = s.recvfrom(1024)
		if not data:
			continue
		else:
			#phase=1
			print 'writing to file'
			outFile.write(data)
			counter=0
s.close()
outFile.close()
print 'Finished'