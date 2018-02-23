#!/usr/bin/env python3

#tshark -r passwd.pcap -T fields -e data
#tshark -r passwd.pcap -Vx

import sys
from subprocess import check_output

def get_passwd(pcap_file):
    packet_data = check_output(["tshark", "-r", pcap_file, "-T", "fields", "-e", "data"])

    #https://stackoverflow.com/questions/606191/convert-bytes-to-a-string (Second answer)
    data = "".join(map(chr, packet_data))
    data = data[-29:-3]
    print(data)

def main():

    #Get file name
    pcap_file = sys.argv[1]

    get_passwd(pcap_file)

if __name__ == '__main__':
    main()