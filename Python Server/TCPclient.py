# TCP client example
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5005))
sendFile = open('sample.txt', 'r')
while 1:
    data = client_socket.recv(512)
    if ( data == 'q' or data == 'Q'):
        client_socket.close()
        break;
    else:
        print "RECIEVED:" , data
        dataServer = raw_input ( "SEND( TYPE q or Q to Quit):" )
        dataServer = sendFile.read(512)
        if (dataServer == 'Q' and dataServer == 'q'):
            client_socket.send(dataServer)
            client_socket.close()
            print "Closing"
            break;        
        else:
            client_socket.send(dataServer)
            print "Data sent."


