#!/usr/bin/env python3

#this program tries to capture packets using a socket

"""Sources Used:
	https://docs.python.org/2/library/socket.html
"""

import socket
import sys
import os

HOST='128.114.59.42'
PORT=5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

if not os.path.exists("captpcap"):
	os.makedirs("captpcap")

fileName="captpcap/pcapData"
fileNo='0'
fileEnding=".pcap"
pcapOut = open( fileName+fileNo+fileEnding, 'w')

pcapData=s.recv(2048)
pcapOut.write(pcapData)
print "done"


s.close()