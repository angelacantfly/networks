# TCP client example
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
<<<<<<< HEAD
client_socket.connect(("localhost", 5005))
sendFile = open('sample.txt', 'r')
=======
client_socket.connect(("nodea", 5005))
>>>>>>> 5b2d058b89bad84f653751c595a1d1d9b16b71e2
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
<<<<<<< HEAD
            print "Closing"
            break;        
        else:
            client_socket.send(dataServer)
            print "Data sent."

=======
            break;
>>>>>>> 5b2d058b89bad84f653751c595a1d1d9b16b71e2

