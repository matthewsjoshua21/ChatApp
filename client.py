from socket import *
import threading, pickle
import time
import sys

from _thread import *

HEADER_SIZE = 10
headerMessage = "default"
global hMessageToSend
hMessageToSend = '{:<10}'.format(headerMessage)

def thread(connectionSocket):
    while (connectionSocket):
        #print("Trying active listening")
        try:
            fullMessage = connectionSocket.recv(1024).decode()
            header = fullMessage[:10]
            buffer = fullMessage[10:]
            #print(header)
            print(buffer)
            if header.strip() == "validation":
                temp = input("> ")
                connectionSocket.send(temp.encode())
                temp2 = connectionSocket.recv(1024).decode()
                print(temp2)
                hMessageToSend = '{:<10}'.format(temp2)
        except:
            break


serverName = '127.0.0.1'
serverSocket = socket()
port = 123
serverSocket.connect((serverName, port))

validationSuccess = True
successMessage = "Welcome"

while validationSuccess:
	name = input("Enter your unique screen-name: ")
	serverSocket.send(name.encode())
	aMessage = serverSocket.recv(1024).decode()
	print(aMessage)
	if successMessage == aMessage:
		validationSuccess = False

#The server welcome message
buffer = serverSocket.recv(1024).decode() + "\n> "
print(buffer)

serverSocket.send((hMessageToSend + "> " + name + " has joined.").encode())

print("Enter (1): List Users (2): Chat (3): Exit (4): Group Chat")

start_new_thread(thread, (serverSocket,))

while True:
    buffer = input("> ")

    if buffer == "1":
        fullMessage = hMessageToSend + "1"
        #print(fullMessage)
        serverSocket.send(fullMessage.encode())

    elif buffer == "2":
        serverSocket.send((hMessageToSend + buffer).encode())
        temp = input("Enter User: ")
        serverSocket.send(temp.encode())
        print("waiting for reply....")
        reply = serverSocket.recv(1024).decode()
        print(reply)
        if reply == "Success":
            hMessageToSend = '{:<10}'.format(temp)


    elif buffer == "3":
        serverSocket.send((hMessageToSend + buffer).encode())
        break
    elif buffer == "4":
        hMessageToSend = '{:<10}'.format("group")

    else:
        serverSocket.send((hMessageToSend + buffer).encode())


serverSocket.close()
print("Closing chatApp")
