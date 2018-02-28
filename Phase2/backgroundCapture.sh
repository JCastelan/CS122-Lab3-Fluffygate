#!/bin/bash

nohup python -u packetCapt.py &

echo "Periodically check the progress in nohup.out and captpcap/ to make sure it is working correctly"