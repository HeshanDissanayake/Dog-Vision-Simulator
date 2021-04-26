import threading

class ipcamera(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.frame = None
    
    def run():
        