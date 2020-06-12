import socket
import errno
import sys


#for other client enter the same source server
message = ''

Header_length = 10    #header lenght
#IP = socket.gethostbyname(socket.gethostname()) #IP address
IP = '34.75.51.43'
Port = 3306    #TCP port

#username input
my_username = input("username: ")
username = my_username.encode('utf-8')

#Internet transmission initialized
client_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the server by parameter
client_init.connect((IP,Port))

#allow the receive
client_init.setblocking(False)

#need to double check header thing
username_header = f"{len(username): <{Header_length}}".encode('utf-8')

#username to the server
client_init.send(username_header + username)


#the client message handling
while(True):

    message = input(f"{my_username}:")

    #if message is not empty,sending to the server and other client
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message): < {Header_length}}".encode('utf-8')
    
        client_init.send(message_header+message)

