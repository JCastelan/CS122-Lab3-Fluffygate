#!/bin/bash

echo working...
counter=0
for filename in processedDataPackets/user*Output/decriptedMessageTwo/*; do
	python decipherChainRot.py $counter $filename
	counter=$((counter+1)) 
done
grep jgcastel  cipherResultsChainRot/* >AAAourChainRotMessages
grep ceneri  cipherResultsChainRot/* >>AAAourChainRotMessages
echo done