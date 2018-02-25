#!/usr/bin/env python3

#this program tries to implement the following command using python:
#echo $encrpytedPass 128.114.59.29 $portNum | nc 128.114.59.42 2001

"""Sources Used:
	https://docs.python.org/2/library/socket.html
"""
import socket
import sys

TARGET_HOST='128.114.59.42'
TARGET_PORT=2001
LOCAL_HOST='128.114.59.29 '
LOCAL_PORT='56798 ' #make sure this matches the listner

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TARGET_HOST, TARGET_PORT))

cryptFile = open("passwd.crypt", "r")
cryptedPass=cryptFile.readline().strip()

message=cryptedPass+' '+LOCAL_HOST+LOCAL_PORT
#print message

s.sendall(message)
response = s.recv(1024)
print response

s.close()