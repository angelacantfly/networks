import socket
import sys
import os
'''
    The serve receives a file from a client.
'''
BLOCK_SIZE = 512
METADATA_SIZE = 5
INDEX_SIZE = 8

portNumber = sys.argv[1]
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind(("", int(portNumber)))
tcp_server_socket.listen(5)

print "TCPServer Waiting for client on port ", portNumber

packets = []
filename = None
filesize = None
checksum = None
numPackets = None
packetSize = None


###################################################################
# TCP Metadata Transfer 
###################################################################
tcp_client_socket, address = tcp_server_socket.accept()
print "I got a connection from ", address
# +++ Confirmation 1: established TCP connection. +++ #
tcp_client_socket.send("Connection initialized.")

needsMetaData = 1
array = []
while needsMetaData:
	# Hacky processing :)
	metadata = tcp_client_socket.recv(BLOCK_SIZE)
	metadata = metadata.replace("\'", "")
	metadata = metadata[1:-1]
	array = metadata.split(', ')
	needsMetaData = 0
	# +++ Confirmation 2: complete metadata transfer. +++ #
	tcp_client_socket.send(str(needsMetaData))

print 'Metadata : ', array 

for data in array:
	data = data.split(':')
	if 'file size' in data[0]:
		filesize = int(data[1])
		print 'filesize: ', filesize
	if 'name' in data[0]:
		filename = data[1]
		print 'filename: ', filename
	if 'checksum' in data[0]:
		checksum = data[1]
		print 'checksum: ', checksum
	if 'number of blocks' in data[0]:
		numPackets = int(data[1])
		print 'numPackets: ', numPackets
	if 'block size' in data[0]:
		packetSize = int(data[1])
		print 'packetSize: ',packetSize

# Confirmation for client that the metadata transfer is complete
tcp_client_socket.send('0')
# tcp_server_socket.close()
print 'Done with metadata.'
###################################################################


###################################################################
# UDP file transfer
###################################################################
# Variables
host = "0.0.0.0"
port = 5006
# buf = 512 # adjustable, try higher
# BLOCK_SIZE = 512
buf = BLOCK_SIZE - INDEX_SIZE

# Connect and bind
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((host, port))

# Address here is a pair "(host, port), which is used for the AF_INET address family"
address = (host,port)

# Get the filename from buffer
data,address = udp_socket.recvfrom(BLOCK_SIZE) # Tuple (name, address)
filename = data.strip()
print "Receive file start:",filename


# Open a file with the name of the transmitted file to write
# f = open(filename, 'wb') # 'wb' is for writing binary files
f = open(filename, 'w')
# index calculations - this is tacked to the front of data
size = os.path.getsize(filename)
numBlocks = size / BLOCK_SIZE
if size % BLOCK_SIZE != 0:
    numBlocks += 1

# instead of sending 512, we send 408 so 4 bytes will be the index #
# we start at -1 because the first block of the file has the file name in it
index = -1
lostPackets = []
successPackets = []
# Get the rest of the files
error = 0
resendPackets = []
try:
    while data:
        index += 1
        if (index % 100 == 0):
	        print "The index is:", index

        # Get the current index from the first few characters in data block
        current_index = data[0:INDEX_SIZE]
        if (index > 0):
			print "The data block index is:", current_index
			print 'Trying to conver to int, ', int(current_index)
			successPackets.append(int(current_index))


        # remove the filename from the header

        # if (index == 0):
        data = data.replace(filename, "")

        # replace the header of the blocks.
        data = data.replace(current_index,"")
        # print data

        f.write(data)
        f.flush()
        udp_socket.settimeout(2) # Round-trip time

        if index >= numPackets:
        	break;

        data,address = udp_socket.recvfrom(BLOCK_SIZE)
        # print 'numPackets',numPackets

    print 'Done transfering data through udp first.'


    for x in xrange(1, numPackets):
    	if x not in successPackets:
    		resendPackets.append(x)
    print 'resend the following packets: ', resendPackets

    #resendPackets = [123,125,69]
    while resendPackets:
		print 'lost packets: ', resendPackets
		# if len(resendPackets) < 1: 
		# 	tcp_client_socket.send(str(resendPackets)) # FIXME: resendPackets can be too big
		# else:
		# 	tcp_client_socket.send(str(resendPackets[0:1]))
		tcp_client_socket.send(str(resendPackets))
		data,address = udp_socket.recvfrom(BLOCK_SIZE)

		while data:
			# if filename in data:
			# 	continue
			current_index = data[0:INDEX_SIZE]
			index = int(current_index)
			if index in resendPackets:
				print "The data block index is:", current_index
				data = data.replace(current_index,"")
				resendPackets.remove(int(current_index))
				print 'lost packet after update :', resendPackets

				# Go seek the file at the appropriate place
				# and write data to the file
				f.seek(index * buf)
				f.write(data)
			if len(resendPackets) == 0:
				print 'waitingToComplete = 0'
				tcp_client_socket.send('waitingToComplete = 0')
				break;
			data,address = udp_socket.recvfrom(BLOCK_SIZE)
except socket.timeout:
	f.close()
	udp_socket.close()
	print "File download complete! "




print "( " ,address[0], " " , address[1] , " ) received: ", filename
print "missing packets: ", resendPackets

f.close()

print "The file we have written is: ", filename
# Change file name
try:
	tcp_client_socket.send('waitingToComplete = 0')
except socket.error:
	tcp_client_socket.close()

tcp_server_socket.close()