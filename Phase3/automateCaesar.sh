#!/bin/bash

echo working...
counter=0
for filename in finalProcessedDataPackets/user*Output/decriptedMessageOne/*; do
	python decipherCaesar.py $counter $filename
	counter=$((counter+1)) 
done
grep jgcastel  cipherResultsCaesar/* >AAAourCaesarMessages
grep ceneri  cipherResultsCaesar/* >>AAAourCaesarMessages
echo done