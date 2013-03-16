#! /usr/bin/python

from socket import *
import select
import sys
import threading
from folder import unit1main
import logs

class Server:
    def __init__(self):
        self.host = 'localhost' 
        self.port = 1234
        self.backlog = 5
     
        self.server = None
        self.threads = []
        self.doc = None
        
    def open_socket(self):
	'''creates the server socket,binds it to the (host,port) and listens\nlog object is created'''
        try:
            self.server = socket(AF_INET,SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(self.backlog)
        except error,(value,message):
            if self.server:
                self.server.close()
            print "Could not open socket :",message
            sys.exit(1)
        self.doc = logs.datalog('qlog.txt')

    def run(self):
	'''calls open_socket()\nin a loop each time a request comes from a new client a new Client object (subclass of threading.Thread) is created to handle that client\nif input is from stdin it exits the loop\nit waits till all threads complete execution, then closes the server socket and the log file'''
        self.open_socket()
        input = [self.server,sys.stdin] #unix only
        print 'server ready'
        running = True
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])
            for s in inputready :
                if s == self.server :
                    ct = Client(self.server.accept(),self.doc)
                    ct.start()
                    self.threads.append(ct)

                elif s==sys.stdin:
                    running = False
        for ct in self.threads:
            ct.join()
        print 'closing server'
        self.server.close()
        self.doc.close()

class Client(threading.Thread):
    '''thread that should handle client requests'''
    def __init__(self,(client,addr),log):
        threading.Thread.__init__(self)
        self.clientSocket = client
        self.addr = addr
        self.size = 1024
        self.doc = log
        
        self.doc.enterclient(self.addr)
        
    def run(self):
	'''receives queries from client, processes them and sends result to the '''
        running = True
        while running :
            # Receive the client packet(i.e query)
            querymsg = self.clientSocket.recv(self.size)
            #print querymsg
            if querymsg :
                self.doc.enterquery(self.addr,querymsg)
                respMsg = str(unit1main.query(querymsg))
                self.clientSocket.send(respMsg)
            else :
                self.doc.exitclient(self.addr)
                self.clientSocket.close()
                running = False

if __name__ == "__main__" :
    s = Server()
    s.run()

