#!/usr/bin/env python

# Usage: >> python UDPserver.py

# UDP server example
# lsof -i udp:5006 // use this to test if port 5006 is free
import socket
import sys
import os

# Variables
host = "0.0.0.0"
port = 5006
# buf = 512 # adjustable, try higher
BLOCK_SIZE = 512
INDEX_SIZE = 8
buf = BLOCK_SIZE - INDEX_SIZE

# Connect and bind
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

# Address here is a pair "(host, port), which is used for the AF_INET address family"
address = (host,port)

# Get the filename from buffer
data,address = server_socket.recvfrom(BLOCK_SIZE) # Tuple (name, address)
filename = data.strip()
print "Receive file start:",filename

# Open a file with the name of the transmitted file to write
f = open(filename, 'wb') # 'wb' is for writing binary files

# index calculations - this is tacked to the front of data
size = os.path.getsize(filename)
numBlocks = size / BLOCK_SIZE
if size % BLOCK_SIZE != 0:
    numBlocks += 1

# instead of sending 512, we send 408 so 4 bytes will be the index #
# we start at -1 because the first block of the file has the file name in it
index = -1

# Get the rest of the files
try:
    while(data):
        index += 1

        print "The index is:", index

        # Get the current index from the first few characters in data block
        current_index = data[0:INDEX_SIZE]
        if (index > 0):
            print "The data block index is:", int(current_index)

            # if the current index does not match the one transmitted, then
            # alert the TCP helper!
            if(index != int(current_index)):
               print "uh oh! we got a corruption :D"
               print "enter ANGELA"

        # remove the filename from the header
        data = data.replace(filename, "")

        # replace the header of the blocks.
        data = data.replace(current_index,"")

        f.write(data)
        server_socket.settimeout(2) # Round-trip time
        data,address = server_socket.recvfrom(BLOCK_SIZE)
except socket.timeout:
    f.close()
    server_socket.close()
    print "File download complete! "

print "( " ,address[0], " " , address[1] , " ) received: ", filename

# print "UDPServer Waiting for client on port 5006"

# temp = open('workfile_udp.txt', 'w')

# while 1:
#     data, address = server_socket.recvfrom(256)
#     print "( " ,address[0], " " , address[1] , " ) said : ", data
#     temp.write(data)

# temp.close()
