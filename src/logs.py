import time

class datalog :
    '''class to log clients accepted, their queries, etc into a file\n'''
    def __init__(self,filename):
        self.logfile = open(filename,'a')
        
    def enterlog(self,str):
	'''enter a general log'''
        self.logfile.write('TIME:'+time.ctime()+'\nINFO:'+str+'\n')
        self.logfile.write('\n')
        
    def enterquery(self,addr,query):
        '''enter log of query : time of query, client making query, query itself\n'''
        self.logfile.write('TIME:'+time.ctime()+'\n')
        self.logfile.write('CLIENT:'+str(addr)+'\n')
        self.logfile.write('QUERY:'+query+'\n')
        self.logfile.write('\n')

    def enterclient(self,addr):
	'''enter log of client being accepted by server'''
        self.logfile.write('TIME:'+time.ctime()+'\n')
        self.logfile.write('ACCEPT:'+str(addr)+'\n')
        self.logfile.write('\n')

    def exitclient(self,addr) :
	'''enter log of client which completes execution and exits'''
        self.logfile.write('TIME:'+time.ctime()+'\n')
        self.logfile.write('CLOSE:'+str(addr)+'\n')
        self.logfile.write('\n')

    def close(self):
        self.logfile.close()
