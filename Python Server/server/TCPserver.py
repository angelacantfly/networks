# TCP server example
# lsof -i tcp:5005 // use this to test if port 5006 is free
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5005))
server_socket.listen(5)

print "TCPServer Waiting for client on port 5005"

temp = open('workfile', 'w')

while 1:
	client_socket, address = server_socket.accept()
	print "I got a connection from ", address
	while 1:
		data = raw_input ( "SEND( TYPE q or Q to Quit):" )
	 	if (data == 'Q' or data == 'q'):
			client_socket.send (data)
			client_socket.close()
			break;
		else:
			client_socket.send(data)
		print "Data sent."

		dataClient = client_socket.recv(512)
		if (dataClient == 'q' or dataClient == 'Q'):
			client_socket.close()
			temp.write(dataClient)
			print "Lost connection with ", address
			break;
		else:
			print "recevied: ", dataClient
			temp.write(dataClient)



print "The file we have written is: "
print temp

temp.close()
