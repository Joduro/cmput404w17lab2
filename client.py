#!/usr/bin/env python

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET indicates that we want an IPv4 socket
# socket.SOCK_STREAM indicates that we want a TCP socket

clientSocket.connect(("www.google.com", 80)) 
# note that there is no http:// because such a low level that the protocol does not matter. 
# port 80 is the standart http port

request = "GET / HTTP/1.0\r\n\r\n" #the request is not complete until sending a blank line that seperates header from body

clientSocket.sendall(request)

response = bytearray()
while True:
    part = clientSocket.recv(1024) # try to recieve 1 kb from the server
    if (part):
        response.extend(part)
    else:
        break

print response
