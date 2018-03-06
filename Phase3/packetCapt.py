#!/usr/bin/env python3

#this program tries to capture packets using a socket

"""Sources Used:
	https://docs.python.org/2/library/socket.html
"""

###TODO### (last updated 2/28)
# Make a loop that captures all pcaps separately (probably done but I don't know how to check)
# Filter out pcaps that don't have a payload with at least one byte 
# Only collect packets around 2AM and 2PM (DONE)
	# probably best to start capturing a few minutes before 2AM and 2PM
	# and then keep capturing for half an hour
# Optimize code
# Use multiple threads to guarantee we get every packet
# run it (probably with NOHUP)

### How to test ### (last updated 2/28)
# On one terminal, run ./backgroundCapture.sh
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
packetCaptNumber=1 ##TODO change this so that we could maybe have this set by user input
if not os.path.exists("captpcap"+str(packetCaptNumber)): 
	os.makedirs("captpcap"+str(packetCaptNumber))

fileName="captpcap"+str(packetCaptNumber)+"/pcapData"
fileEnding=".pcap"
fileNo=0

#######debug stuff 
startTime = time.localtime(time.time()) ##for debugging
print "Local current start time :", startTime
#print "ClockTime is ", startTime.tm_hour,":",startTime.tm_min
#stopHour=startTime.tm_hour
#stopMin=startTime.tm_min+2
#debugCounter = 50


##variables to control the time period in which we capture packets
AMstartH=1
AMstopH=2
#PMstartH=13 #we need to remove these
#PMstopH=14 #We need to remove these

startM=57
stopM=15



localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "This program was started at ",currHour,":",currMin

print"waiting for right time"
if not(((currHour==AMstartH) and (currMin > startM)) or ((currHour==AMstopH) and (currMin < stopM))) : 
	localtime = time.localtime(time.time())
	currHour=localtime.tm_hour
	currMin=localtime.tm_min
	if currMin < startM:
		sleepTimeM=(57-currMin)*60
		print "Sleeping for ", 57-currMin, " minutes..."
		time.sleep(sleepTimeM) #sleep until the 57th of the hour
	if currHour==0:
		time.sleep(1*60*60) #sleep for one hour
	elif currHour > AMstartH:
		sleepTimeH=(25-currHour)*3600 #3600=60*60
		print "Sleeping for ", 25-currHour, " hours..."
		time.sleep(sleepTimeH)
"""Continuous loop of pcap capturing"""
print "Entering capture loop"
localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "Stopped waiting at ",currHour,":",currMin
while ((currMin >= startM) or (currMin < stopM) ):#(((currHour==AMstartH) and (currMin >= startM)) or ((currHour==AMstopH) and (currMin <= stopM))) : 
	try:
		localtime = time.localtime(time.time())
		currHour=localtime.tm_hour
		currMin=localtime.tm_min
		print "Local current time :", localtime
		print "[fileNo=", fileNo, "] [currMin=", currMin,"] [currHour=", currHour,"]"
		#print "ClockTime is ", localtime.tm_hour,":",localtime.tm_min
		pcapOut = open( fileName+str(fileNo)+fileEnding, 'w')
		pcapData=s.recv(4096)
		#print pcapData #debug
		pcapOut.write(pcapData)
		pcapOut.close()
		fileNo+= 1
		"""debugCounter-=1
		if debugCounter <=0:
		break"""
	except:
		s.connect((HOST,PORT))

"""Program End"""
localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "Finished capturing at ",currHour,":",currMin
print "done"
s.close()