#! /usr/bin/python
from socket import *

host = 'localhost'
port = 1234
bufsize = 2048

#creating a client socket
clientSocket = socket(AF_INET, SOCK_STREAM) 
clientSocket.connect((host,port))
    
continu = 'y'
try:
    while continu=='y': 
        query = raw_input(' Enter the query : \n')
        #sending query to server
        if not query :
            break
        clientSocket.send(query)
                    
        #receiving result from server
        recdMessage = clientSocket.recv(bufsize) 
                
        #printing the received message
        print 'query result : \n',recdMessage
        continu = raw_input(' do you want to continue (y/n) :')
		
except error,msg:
    print "socket error :",msg	

finally: 
    clientSocket.close()
    print 'closing client'
