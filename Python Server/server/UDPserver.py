#!/usr/bin/env python

# Usage: >> python UDPserver.py

# UDP server example
# lsof -i udp:5006 // use this to test if port 5006 is free
import socket

# Variables
host = "0.0.0.0"
port = 5006
buf = 512 # adjustable, try higher

# Connect and bind
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

# Address here is a pair "(host, port), which is used for the AF_INET address family"
address = (host,port)

# Get the data from buffer
data,address = server_socket.recvfrom(buf) # Tuple (name, address)
filename = data.strip()
print "Receive file start:",filename

# Open a file with the name of the transmitted file to write
f = open(filename, 'wb') # 'wb' is for writing binary files

# Get the rest of the files
try:
    while(data):
        f.write(data)
        server_socket.settimeout(2) # Round-trip time
        data,address = server_socket.recvfrom(buf)
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
