#!/usr/bin/env python

import socket
import os, sys, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind(("0.0.0.0", 8000)) #0.0.0.0 means every address on this machine
serverSocket.listen(5) #keep up to 5 incoming connection in a queue

while True:
    (incomingSocket, address) = serverSocket.accept()
    print "We got a connection from %s" % (str(address))
    
    if os.fork() == 0:

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.AF_INET indicates that we want an IPv4 socket
        # socket.SOCK_STREAM indicates that we want a TCP socket

        clientSocket.connect(("www.google.com", 80)) 
        # note that there is no http:// because such a low level that the protocol does not matter. 
        # port 80 is the standart http port

        incomingSocket.setblocking(0)
        clientSocket.setblocking(0)

        while True:

            request = bytearray()
            while True:
                try:
                    part = incomingSocket.recv(1024) # try to recieve 1 kb from the server
                except IOError, e:
                    if e.errno == socket.errno.EAGAIN:
                        part = None
                    else:
                        raise

                if (part):
                    clientSocket.sendall(part) # when read incoming send it to the client socket.
                    request.extend(part)
                elif part is None:
                    break
                else:
                    exit(0)

               

            if len(request) > 0:
                print request

            response = bytearray()
            while True:
                try:
                    part = clientSocket.recv(1024)
                except IOError, e:
                    if e.errno == socket.errno.EAGAIN:
                        part = None
                    else:
                        raise
                if (part):
                    incomingSocket.sendall(part)
                    response.extend(part)
                elif part is None:
                    break
                else:
                    exit(0)
            if len(response) > 0:
                print response

           	select.select(
			    [incomingSocket, clientSocket], #read
			    [],                             #write
			    [incomingSocket, clientSocket], #except
            1.0) # timeout



