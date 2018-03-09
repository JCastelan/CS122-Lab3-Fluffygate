#!/bin/bash

echo working...
counter=0
for filename in processedDataPackets/user*Output/decriptedMessageThree/*; do
	python decipherAffine.py $counter $filename
	counter=$((counter+1)) 
done
grep jgcastel  cipherResultsAffine/* >AAAourAffineMessages
grep ceneri  cipherResultsAffine/* >>AAAourAffineMessages
echo done