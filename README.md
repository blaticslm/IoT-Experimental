# Socket-chatroom experience
 This project is to demo how the user can interact with the server. 
 
## Python package installation
using python [pip](https://pip.pypa.io/en/stable/) to install sockets
 ```Bash
 pip install sockets
 ```
## Attentions
- The IP address of server is ephmeral, so the client's IP address should also be changed constantly
- The [Computing Engine](https://cloud.google.com/compute) from [Google Cloud Platform](https://cloud.google.com/) is used as the server


## Basic Code
- Before doing data transmitting, the basic chatroom should be created. 
- The codes are listed in the Basic Chatroom folder:
>new_server.py

>new_msgwindow.py

>chat-client.py


## Extension
When sending the data to server, the chat client should be modified in one place. 
> the example is sending the computer cpu running status

>The require package is installed via [pip](https://pip.pypa.io/en/stable/)
```Bash
pip install psutil
```


in chat-client.py, the following lines should be added
 ```python
 import psutil 
