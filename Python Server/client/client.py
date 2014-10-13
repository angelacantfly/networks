import socket
import TCPhelpers_client
import sys
'''
    The client send a file to the server.
'''
BLOCK_SIZE = 512
METADATA_SIZE = 5


# Initialize connection with host
# serverHostName = raw_input('Enter the server host name: ')
# portNumber = raw_input('Enter the port number: ')
# fileName = raw_input('Enter the file name to transfer: ')
serverHostName = sys.argv[1]
portNumber = int(sys.argv[2])
fileName = sys.argv[3]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((serverHostName, portNumber))
sendFile = open('sample.txt', 'r')
metaData = TCPhelpers_client.generateMetaData(fileName, BLOCK_SIZE)
#sendFile = open(fileName, 'r')

print metaData
# TCP portion
print client_socket.recv(BLOCK_SIZE)
needMetadata = 1
while needMetadata:
    client_socket.send(str(metaData))
    needMetadata = int(client_socket.recv(BLOCK_SIZE))
print 'yolo'

# iterater = 0
# while metaDataTransfer:
#     reaction = client_socket.recv(BLOCK_SIZE)
#     # If there is an error according to server
#     # resend metadata
#     if 'error' in reaction:
#         client_socket.send(metaData[iterater])
#         print "Send line ", iterater, " again."
#     else:
        
# while 1:
#     data = client_socket.recv(512)
#     if ( data == 'q' or data == 'Q'):
#         client_socket.close()
#         break;
#     else:
#         print "RECIEVED:" , data
#         dataServer = raw_input ( "SEND( TYPE q or Q to Quit):" )
#         dataServer = sendFile.read(512)
#         if (dataServer == 'Q' and dataServer == 'q'):
#             client_socket.send(dataServer)
#             client_socket.close()
#             print "Closing"
#             break;
#         else:
#             client_socket.send(dataServer)
#             print "Data sent."

client_socket.close()
print "Terminating."