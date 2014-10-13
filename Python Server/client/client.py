import socket
import TCPhelpers_client
import sys
import os
import convertIndex
'''
    The client send a file to the server.
'''
BLOCK_SIZE = 512
METADATA_SIZE = 5
INDEX_SIZE = 8
buf = BLOCK_SIZE - INDEX_SIZE

# system arguments: python programName serverHostName portNumber fileName
serverHostName = sys.argv[1]
portNumber = int(sys.argv[2])
fileName = sys.argv[3]

# Initialize connection with host using TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((serverHostName, portNumber))
metaData = TCPhelpers_client.generateMetaData(fileName, buf)

###################################################################
# TCP Metadata Transfer 
###################################################################
# +++ Confirmation 1: established TCP connection. +++ #
message = client_socket.recv(BLOCK_SIZE)
print message
if 'initialized' not in message:
    print 'Having error initializing connection.'

# +++ Confirmation 2: complete metadata transfer. +++ #
needMetadata = 1

while needMetadata:
    client_socket.send(str(metaData))
    needMetadata = int(client_socket.recv(BLOCK_SIZE))
    print 'needMetadata is ', needMetadata
###################################################################


###################################################################
# UDP file transfer
###################################################################
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udp_client_socket.connect(("localhost", 5006))
# Comment 1: We don't want the above line because unlike TCP, which needs to maintain a solid connection, we don't need to do that with UDP.  UDP is meant to be used as opening a connection and sending stuff over, then closing the connection when done.  Don't need to keep it open
# to create a binary file use: dd if=/dev/random of=file2.bin bs=1m count=200

host = sys.argv[1]
port = 5006
address = (host,port)
# buf = 512


filename = sys.argv[3]

udp_client_socket.sendto(filename, address)

# Open a file with the name of the transmitted file to read
f = open(filename, "rb") # read binary

# Read an initial amount data to buffer
data = f.read(buf)
# print data
# index calculations - this is tacked to the front of data
size = os.path.getsize(filename)
numBlocks = size / BLOCK_SIZE
if size % BLOCK_SIZE != 0:
    numBlocks += 1

# TODO: Attach a number to each
# instead of sending 512, we send 508 so 4 bytes will be the index #
index = 0

while(data):
    index += 1
    if(udp_client_socket.sendto(convertIndex.convertIndexToStr(index, INDEX_SIZE) + data,address)):
        print "Sending:",filename, "... index:", convertIndex.convertIndexToStr(index, INDEX_SIZE)
        data = f.read(buf)

udp_client_socket.close()
###################################################################

###################################################################
# Retransfering lost packets
###################################################################
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client_socket.sendto(filename, address)

waitingToComplete = 1
listString = client_socket.recv(BLOCK_SIZE)
while waitingToComplete:
    
    # print 'received list: ', listString
    # Test if the transfer is actually complete
    if 'waitingToComplete' in listString and '0' in listString:
        print 'Transfer complete, no more lost packets.'
        waitingToComplete = 0
        break;
    
    # Parse list of lost packets being transfered
    listString = listString.replace("\'", "")
    listString = listString[1:-1]
    lostPackets = listString.split(',')
    if '' in lostPackets:
        lostPackets.remove('')
    if lostPackets:
        print 'Lost packets: ', lostPackets
        for index in lostPackets:
            index = int(index)
            f.seek(buf * index)
            data = f.read(buf)
            if (udp_client_socket.sendto(convertIndex.convertIndexToStr(index, INDEX_SIZE) + data,address)):
                print "Resending:",filename, "... index:", convertIndex.convertIndexToStr(index, INDEX_SIZE)
    listString = client_socket.recv(BLOCK_SIZE)

###################################################################



###################################################################
# Cleaning up
###################################################################

udp_client_socket.close()
f.close()

client_socket.close()
print "Terminating."