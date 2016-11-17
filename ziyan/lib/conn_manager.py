

import threading  


def connect(params):
    print("conn")

class ConnManager(object):    
    
    def __init__(self):
        pass
        self.lock = threading.Lock()  
       
    def init(self):
        pass
        
    def connect(self):
        
        if not self.lock.locked():
            self.lock.acquire()
            connect({})
            self.lock.release()
            
        #print dir(self.lock)
        else:
            print self.lock.locked()    
        
    def reconnect(self):
        self.lock.acquire()  
        self.lock.release()

    def close(self):
        pass        
        
    def status(self):
        pass
        

def main():
    
    mgr = ConnManager()
    
    mgr.connect()
    
    
if __name__ == '__main__':
    
    main()
    