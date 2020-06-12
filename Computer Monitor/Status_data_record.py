import socket
import errno
import sys
import csv


Header_length = 10    #header lenght
#IP = socket.gethostbyname(socket.gethostname()) #IP address
IP = '34.73.136.91'
Port = 3306    #TCP port

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


def list_convert(string_list):

    #convert the string to the integer list
    string_list = string_list.strip('[]').split(',')

    for i in range(len(string_list)):
        string_list[i] = float(string_list[i])

    return string_list

#for csv row name
time = 0


#csv writing format
with open('test.csv','w',newline = '') as file:

        cpu_names = ['time','cpu0','cpu1','cpu2','cpu3','cpu4','cpu5','cpu6','cpu7']
        writer = csv.DictWriter(file, fieldnames = cpu_names)
        writer.writeheader()
        

        while(True):
      
            #receive the message: most parts are same as new_msgwindow.py except this is writing to file
            try:

                while(True):
                    username_header = client_init.recv(Header_length)

                    if not len(username_header):
                        print("connection is gone")
                        sys.exit()

                    #username with specific length
                    username_length = int(username_header.decode('utf-8').strip())
                    username = client_init.recv(username_length).decode('utf-8')

                    #message
                    message_header = client_init.recv(Header_length)
                    message_length = int(message_header.decode('utf-8').strip())

                    message_after =client_init.recv(message_length).decode('utf-8')
                    

                    float_list = list_convert(message_after)
                    print(float_list)

                    #csv file writing
                    writer.writerow({'time':time,'cpu0':float_list[0],
                                        'cpu1':float_list[1],
                                        'cpu2':float_list[2],
                                        'cpu3':float_list[3],
                                        'cpu4':float_list[4],
                                        'cpu5':float_list[5],
                                        'cpu6':float_list[6],
                                        'cpu7':float_list[7]})

                    print("write_successfully")

                    #row name update
                    time += 1
                    
            #error handling
            except IOError as E:
                if E.errno != errno.EAGAIN and E.errno != errno.EWOULDBLOCK:
                    print("reading error:", str(E))
                    sys.exit()
                    continue

            except Exception as E:
                print("general error:", str(E))
                sys.exit()
                continue

             

