#!/usr/bin/env python3

#this program tries to capture packets using a socket

"""Sources Used:
    https://docs.python.org/2/library/socket.html
"""

###TODO### (last updated 3/6)
# Filter out pcaps that don't have a payload with at least one byte 
# Optimize code
# Use multiple threads to guarantee we get every packet

### How to test ### (last updated 2/28)
# On one terminal, run ./backgroundCapture.sh
# On a different terminal, run this: 
#   while true; do nc 128.114.59.42 5001 | tshark -i - 2>/dev/null; done
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
packetCaptNumber="Phase4"	 ##TODO change this so that we could maybe have this set by user input
if not os.path.exists("captpcap"+packetCaptNumber): 
    os.makedirs("captpcap"+packetCaptNumber)

fileName="captpcap"+packetCaptNumber+"/pcapData"
fileEnding=".pcap"
fileNo=0

#######debug stuff 
startTime = time.localtime(time.time()) ##for debugging
print "Local current start time :", startTime


##variables to control the time period in which we capture packets
startH=22
startM=58

stopH=23
stopM=59


localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "This program was started at ",currHour,":",currMin

print"waiting for right time"
if currMin < startM: #sleep until the right minute
	timespan = startM-currMin
	sleepTimeM=(timespan)*60
	print "\tSleeping for ", startM-currMin, " minutes... (until minute ", currMin+timespan,")" 
	time.sleep(sleepTimeM) 

localtime = time.localtime(time.time())
currHour=localtime.tm_hour
if currHour < startH: #sleep until the right hour
	timespan = startH-currHour
	sleepTimeH=(timespan)*3600
	print "\tSleeping for ", startH-currHour, " hours... (until hour ", currHour+timespan, ")"
	time.sleepTimeH 


localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "Stopped waiting at ",currHour,":",currMin

print "Entering capture loop"
"""Continuous loop of pcap capturing"""
while (((currHour==startH) and (currMin >= startM)) or ((currHour==stopH) and (currMin <= stopM))) : 
    try:
        localtime = time.localtime(time.time())
        currHour=localtime.tm_hour
        currMin=localtime.tm_min
        #print "Local current time :", localtime
        print "[fileNo=", fileNo, "] [localtime=", localtime,"]"
        #print "ClockTime is ", localtime.tm_hour,":",localtime.tm_min
        pcapOut = open( fileName+str(fileNo)+fileEnding, 'w')
        pcapData=s.recv(4096)
        #print pcapData #debug
        pcapOut.write(pcapData)
        pcapOut.close()
        fileNo+= 1
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message
        try:
        	s.connect((HOST,PORT))
    	except:
    		print "It wasn't a connection error"
"""Program End"""
localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "Finished capturing at ",currHour,":",currMin
print "done"
s.close()
