import threading
import cv2

class IpCamera(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.frame = None
        self.cap = cv2.VideoCapture(ip)
        self.available = False
        self.close = False
    
    def run(self):
        while not self.close:
            _, frame = self.cap.read()
            self.frame = cv2.resize(frame, (640, 480))
            self.available = True
            # cv2.waitKey(10)

    def close(self):
        self.close = True