# Socket-chatroom experience
 This project is to demo how the user can interact with the server. 
 
## python pack install
using python [pip](https://pip.pypa.io/en/stable/) to install sockets
 ```Bash
 pip install sockets
 ```

## Code
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
IP = socket.gethostbyname(socket.gethostname()) #IP address
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
