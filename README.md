# Socket-chatroom experience
 This project is to demo how the user can interact with the server. 
 
## python pack install
using python [pip](https://pip.pypa.io/en/stable/) to install sockets
 ```Bash
 pip install sockets
 ```
## attentions
- The IP address of server is ephmeral, so the client's IP address should also be changed constantly
- The [Computing Engine](https://cloud.google.com/compute) from [Google Cloud Platform](https://cloud.google.com/) is used as the server


## Basic Code
Before doing data transmitting, the basic chatroom functions are shown below. 
- socket server: 
 ```python
########################
# The main code is studied from @sentdex from Youtube.
# Socket is Low-level networking interface
# Some places are hard to understand such as the header, client list,
# setsockopt, and the select.select part
#
# The function of this server is
# - receving connections from clients
# - receving clients' messages
# - send to other clients
########################


import socket
import select

Header_length = 10    #message header lenght
IP = socket.gethostbyname(socket.gethostname()) #get server local IP address.
Port = 3306    #TCP port

#Internet transmission initialized: IPv4 (AF_INET), TCP(SOCK_STEAM)
server_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#socket setup: socket level, allow reuse local addr, and I dont know why is 1
server_init.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#binding the server parameters together
server_init.bind((IP,Port))

#papare for receiving the the client info
server_init.listen(12)

#the cilents exist in the internet_init
client_list = [server_init]

#client infomation key and data
client_lib = {}

#client iP address
IP_address={}


def receive_message(client_socket):

    #client info receive
    try:
        #header is name
        message_header = client_socket.recv(Header_length)

        #if there is no incoming data
        if not len(message_header):
            return False

        #decode and get actual message length
        message_length = int(message_header.decode('utf-8').strip())

        #raw data and the decoded data put into the dictionary
        return {"header":message_header, "data": client_socket.recv(message_length)}
        

    except:
        return False


while(True):

    read,_,exception = select.select(client_list,[], client_list)

    for notified in read:

        if notified == server_init:
            client_socket, address = server_init.accept() #allow connection

            #return {"data": client.recv( message_len)}
            user = receive_message(client_socket)    

            if user is False: #someone is gone
                continue

            #client infomation
            
            client_list.append(client_socket)    #add to client list
            
            client_lib[client_socket] = user    #'client':'user_header: + user data:'

            IP_address[client_socket] = address[0]    #store the user IP

            #print(f"accept: {address[0]}:{address[1]}, user:{user['data'].decode('utf-8')}")
            print('{}:{}, user: {}'.format(address[0],address[1],user['data'].decode('utf-8')))
            
        else:

            message = receive_message(notified)

            if message is False:
                print("{} disconnected".format(client_lib[notified]['data'].decode('utf-8')))
                client_list.remove(notified)    #remove the disconnected user
                del client_lib[notified]
                continue

            #user infomation and the message 
            user = client_lib[notified]
            #print(f"message from {user['data'].decode('unicode')}:{message['data'].decode('unicode')}")
            print("{}---{}:    {}".format(IP_address[notified],user['data'].decode('utf-8'),message['data'].decode('utf-8')))

            #share message to other than myself
            for client_socket in client_lib:
                if client_socket != notified:
                     client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    #if something wrong with the cilent, remove the client
    for notified in exception:
        client_list.remove(notified)
        del client_lib[notified]
```
- Message Window:
> To achieve one client sends the message, and other clients will see the message simultaneously , the message window will be used as the listening client.

```python
import socket
import errno
import sys

Header_length = 10    #header lenght
#IP = socket.gethostbyname(socket.gethostname()) #IP address
IP = '34.75.51.43'
Port = 3306  #TCP port

#Treating the message window as the listening client
my_username = "msg_screen"
username = my_username.encode('utf-8')

#Internet transmission initialized
client_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the server by parameter
client_init.connect((IP,Port))

#allow the receive
client_init.setblocking(False)

username_header = f"{len(username): <{Header_length}}".encode('utf-8')

client_init.send(username_header + username)

while(True):

    #receive the message must be using try and except format
    #Error will occur if the format is not in try-except: Errno 10035
    try:    
        while(True):
            username_header = client_init.recv(Header_length)

            #connection is gone
            if not len(username_header):
                print("connection is gone")
                sys.exit()

            #username with specific length
            username_length = int(username_header.decode('utf-8').strip())
            username = client_init.recv(username_length).decode('utf-8')

            #message
            message_header = client_init.recv(Header_length)
            message_length = int(message_header.decode('utf-8').strip())

            #message integration
            message_after = client_init.recv(message_length).decode('utf-8')
            
            print(f"{username}:    {message_after}")

    #error handling
    except IOError as E:
        if E.errno != errno.EAGAIN and E.errno != errno.EWOULDBLOCK:
            print("reading error:", str(E))
            sys.exit()
            continue

    except Exception as E:
        print("general error:", str(E))
        continue
```
- input client:
>This is the real client that sends the message to the server. 

```python
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
```
