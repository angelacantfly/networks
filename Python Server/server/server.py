import socket
import sys
'''
    The serve receives a file from a client.
'''
BLOCK_SIZE = 512
METADATA_SIZE = 5

portNumber = sys.argv[1]
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", int(portNumber)))
server_socket.listen(5)

print "TCPServer Waiting for client on port ", portNumber

temp = open('workfile', 'w')
packets = []
filename = None
filesize = None
checksum = None
numPackets = None
packetSize = None


# TCP portion
while 1:
	client_socket, address = server_socket.accept()
	print "I got a connection from ", address
	client_socket.send("Connection initialized.")

	needsMetaData = 1
	array = []
	while needsMetaData:
		# Hacky processing :)
		metadata = client_socket.recv(BLOCK_SIZE)
		metadata = metadata.replace("\'", "")
		metadata = metadata[1:-1]
		arrayData = metadata.split(', ')
		for data in arrayData:
			print array.append(data.split(':'))
		print arrayData
		needsMetaData = 0
		client_socket.send(str(needsMetaData))


	for data in array:
		if 'file size' in data[0]:
			filesize = int(data[1])
		if 'name' in data[0]:
			filename = data[1]
		if 'checksum' in data[0]:
			checksum = data[1]
		if 'number of blocks' in data[0]:
			numPackets = int(data[1])
		if 'block size' in data[0]:
			packetSize = int(data[1])

	client_socket.send('0')
	print 'Done.'
	# print 'filename ', filename
	# print 'filesize ', filesize
	# print 'checksum ',checksum
	# print 'numPackets ',numPackets
	# print 'packetSize ',packetSize


	# while 1:
	# 	dataClient = client_socket.recv(BLOCK_SIZE)
	# 	if (dataClient == 'q' or dataClient == 'Q'):
	# 		client_socket.close()
	# 		temp.write(dataClient)
	# 		print "Lost connection with ", address
	# 		break;
	# 	else:
	# 		print "recevied: ", dataClient
	# 		temp.write(dataClient)


	# 	data = raw_input ( "SEND( TYPE q or Q to Quit):" )
	# 	if (!data):
	# 		client_socket.send("Failed")

	#  	if (data == 'Q' or data == 'q'):
	# 		client_socket.send(data)
	# 		client_socket.close()
	# 		break;
	# 	else:
	# 		client_socket.send(data)
	# 	print "Data sent."





print "The file we have written is: "
print temp
# Change file name

temp.close()
server_socket.close()