import socket
import errno
import sys
import time
import psutil

#for other client enter the same source server
message = ''

Header_length = 10    #header lenght
#IP = socket.gethostbyname(socket.gethostname()) #IP address
IP = '34.73.136.91'
Port = 3306    #TCP port

#my_username = input("username: ").
my_username = 'GS636VR'
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

    
    message = str(psutil.cpu_percent(interval = 2, percpu = True)) #individual core info

    #if message is not empty,sending to the server and other client
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message): < {Header_length}}".encode('utf-8')

        time.sleep(1)
    
        client_init.send(message_header+message)
