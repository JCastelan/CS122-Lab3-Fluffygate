#!/usr/bin/env python3

#this program tries to implement the following command using python:
# nc -l 128.114.59.29 55543 >> listenerOutput

"""Sources Used:
	https://docs.python.org/2/library/socket.html
"""
import socket
import sys

HOST='128.114.59.29'
PORT=54545 #make sure this is the same one used by the NSA requester

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

counter=1000
phase=0 # 0->waiting for data; 1->haveStartedReceivingData
outFile = open("resultsFromNSA.txt", "w")
while counter>0:
	data = s.recv(1024)
	if phase==1:
		counter-=counter
	if not data:
		continue
	else:
		phase=1
		outFile.write(data)
s.close()
outFile.close()
print 'Received'