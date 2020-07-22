from socket import *
import threading, pickle
from _thread import *

connections = []
clients = []
list = {}
connect = socket(AF_INET, SOCK_STREAM)

HEADER_SIZE = 10
#headerMessage = "Default"
#hMessageToSend = f'{"Default":<10}'

def thread(connectionSocket):
	validate(connectionSocket)

	while True:
		try:
			fullMessage = connectionSocket.recv(1024)
			#header + msg
			decodedMsg = fullMessage.decode()

			header = decodedMsg[:10]
			theMessage = decodedMsg[10:]

			scanner = theMessage
			buffer = fullMessage

		except:
			break

		if scanner == "1":
			theList = header
			for index in list:
				theList += f'{index}' + " " + f'{list[index]["available"]}' + '\n'
			connectionSocket.send(theList.encode())

		if scanner == "2":
			tempHeader = "validation"
			user = connectionSocket.recv(1024).decode()
			if user in clients:
				if list[user]["available"] == "Available":
					connect = list[user][socket]

					mssg = "A user is requesting a private chat\n Type y/n"
					connect.send((tempHeader + mssg).encode())
					reply = connect.recv(1024).decode()
					if reply == "y":
						#list[user]["available"]
						#connectionSocket.send(("Success").encode())

						for client in clients:
							if list[client][socket] == connectionSocket:
								temp = client

						connectionSocket.send(("Success").encode())
						connect.send((temp).encode())
					else:
						connectionSocket.send(("User denied your chat").encode())
				else:
					connectionSocket.send(("User is not Available").encode())
			else:
				connectionSocket.send(("User does not exist").encode())

		if scanner == "3":
			connectionSocket.close()
			temp = -1
			for index in list:
				if list[index][socket] == connectionSocket:
					temp = index
			del list[index]
			break

		print(buffer)
		check = header.strip()
		if check == "group":
			for connection in connections:
				if connection != connectionSocket:
					try:
						connection.send(buffer)
					except:
						connections.remove(connection)
		else:
			if check in clients:
				connect = list[check][socket]
				connect.send(buffer)
'''
		for connection in connections:
			if connection != connectionSocket:
				try:
					connection.send(buffer)
				except:
					connections.remove(connection)
'''

def validate(connectionSocket):
	userAccepted = True
	while userAccepted:
		client = connectionSocket.recv(1024).decode()
		if client in clients:
			connectionSocket.send(("Username taken... Please try again...").encode())
		else:
			connectionSocket.send(("Welcome").encode())
			print('Connected to: ' f'{client}')
			clients.append(client)
			connections.append(connectionSocket)
			list[client] = {}
			list[client][socket] = connectionSocket
			list[client]["available"] = "Available"
			userAccepted = False
	connectionSocket.send((client).encode())

#This is the begining of MAIN
host = ""
port = 123
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen()
print("'The server is ready to receive'")

while True:

    connectionSocket, addr = serverSocket.accept()
    #user = connectionSocket.recv(1024).decode()
    start_new_thread(thread, (connectionSocket,))

    #print('Connected to :' f'{user}')
    #clients.append(user)
    #connections.append(connectionSocket)

serverSocket.close()
