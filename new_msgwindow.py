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

