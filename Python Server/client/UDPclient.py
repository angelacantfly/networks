#!/usr/bin/env python

# Usage: >> python UDPclient.py localhost filename.txt

# UDP client example
import socket
import sys
import os
import convertIndex

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.connect(("localhost", 5006))
# Comment 1: We don't want the above line because unlike TCP, which needs to maintain a solid connection, we don't need to do that with UDP.  UDP is meant to be used as opening a connection and sending stuff over, then closing the connection when done.  Don't need to keep it open
# to create a binary file use: dd if=/dev/random of=file2.bin bs=1m count=200

host = sys.argv[1]
port = 5006
address = (host,port)
# buf = 512
BLOCK_SIZE = 512
INDEX_SIZE = 8
buf = BLOCK_SIZE - INDEX_SIZE

filename = sys.argv[2]

client_socket.sendto(filename, address)

# Open a file with the name of the transmitted file to read
f = open(filename, "rb") # read binary

# Read an initial amount data to buffer
data = f.read(buf)
print data
# index calculations - this is tacked to the front of data
size = os.path.getsize(filename)
numBlocks = size / BLOCK_SIZE
if size % BLOCK_SIZE != 0:
    numBlocks += 1

# TODO: Attach a number to each
# instead of sending 512, we send 408 so 4 bytes will be the index #
index = 0

while(data):
    index += 1
    if(client_socket.sendto(convertIndex.convertIndexToStr(index, INDEX_SIZE) + data,address)):
        print "Sending:",filename, "... index:", convertIndex.convertIndexToStr(index, INDEX_SIZE)
        data = f.read(buf)


print "index is:",index
print "total number of blocks is:", numBlocks

client_socket.close()
f.close()
