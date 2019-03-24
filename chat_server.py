import socket
import select
from thread import *
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = '127.0.0.1'
Port = 8086
server.bind((IP_address, Port)) 
server.listen(100)
list_of_clients=[]
list_of_ports=[]
my_dict = {}

def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!")
    #sends a message to the client whose user object is conn
    while True:
            try:     
                message = conn.recv(2048)    
                if message:
		    str1 = message[:5]
		    int_str = int(str1);
                    print "[From PORT: " + str(addr[1]) + "] :: [To " + message[:5] + "] " + message[5:]
                    message_to_send = "[From PORT: " + str(addr[1]) + "] :: " + message[5:]
		    for client in my_dict:
        		if my_dict[client] == int_str:
            		    client.send(message_to_send)
                    #prints the message and address of the user who just sent the message on the server terminal
                else:
                    remove(conn)
            except:
                continue


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

print "This is the Chatroom server. Waiting for connections...\n"

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    list_of_clients.append(conn)
    my_dict[conn] = addr[1]

    initialmsg = "\nYour PORT is " + str(addr[1]) + "\nAvailable ports:::\n"
    conn.send(initialmsg)

    for ports in list_of_ports:
    	initialmsg = str(ports) + "\n"
	conn.send(initialmsg)

    list_of_ports.append(addr[1])
    msg1 = "----New Port:" + str(addr[1]) + " connected----\n"
    print msg1
    for clients in list_of_clients:
        if clients!=conn:
            try:
                clients.send(msg1)
            except:
		clients.close()
		remove(clients)
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))
    #creates and individual thread for every user that connects

conn.close()
server.close()
