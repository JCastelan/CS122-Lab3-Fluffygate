#!/usr/bin/env python3

#this program tries to capture packets using a socket

"""Sources Used:
	https://docs.python.org/2/library/socket.html
"""

###TODO### (last updated 2/25)
# Make a loop that captures all pcaps separately
# Filter out pcaps that don't have a payload with at least one byte 
# Only collect packets around 2AM and 2PM
	# probably best to start capturing a few minutes before 2AM and 2PM
	# and then keep capturing for half an hour
# Optimize code
# run it (probably with NOHUP)

### How to test ### (last updated 2/25)
# On one terminal, run python packetCapt.py
# On a different terminal, run this: 
#	while true; do nc 128.114.59.42 5001 | tshark -i - 2>/dev/null; done
# The second terminal shows the pcaps that this program is trying to capture

### Current bugs ### (last updated 2/25)
# captures more pcaps than are being sent (maybe they are duplicate pcaps?)

import socket
import sys
import os
import time

"""Setting up the socket"""
HOST='128.114.59.42'
PORT=5001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

"""Setting up output files"""
#https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
if not os.path.exists("captpcap"): 
	os.makedirs("captpcap")

fileName="captpcap/pcapData"
fileEnding=".pcap"
fileNo=0


#localtime = time.localtime(time.time())
#print "Local current time :", localtime



"""Continuous loop of pcap capturing"""
for x in xrange(0,9):
	print x
	pcapOut = open( fileName+str(fileNo)+fileEnding, 'w')
	pcapData=s.recv(4096)
	print pcapData
	pcapOut.write(pcapData)
	pcapOut.close()
	fileNo+= 1

"""Program End"""
print "done"
s.close()