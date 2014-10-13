#!/usr/bin/env python

# Usage: >> python UDPclient.py localhost filename.txt

# UDP client example
import socket
import sys
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.connect(("localhost", 5006))
# Comment 1: We don't want the above line because unlike TCP, which needs to maintain a solid connection, we don't need to do that with UDP.  UDP is meant to be used as opening a connection and sending stuff over, then closing the connection when done.  Don't need to keep it open
# to create a binary file use: dd if=/dev/random of=file2.bin bs=1m count=200

host = sys.argv[1]
port = 5006
buf = 512
address = (host,port)

filename = sys.argv[2]

client_socket.sendto(filename, address)

# Open a file with the name of the transmitted file to read
f = open(filename, "rb") # read binary

# Read the data to buffer
data = f.read(buf)

# TODO: Attach a number to each
# instead of sending 512, we send 408 so 4 bytes will be the index #
while(data):
    if(client_socket.sendto(data,address)):
        print "Sending:",filename, "..."
        data = f.read(buf)

client_socket.close()
f.close()
