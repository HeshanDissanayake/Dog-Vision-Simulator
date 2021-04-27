import threading
import cv2
class IpCamera(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.frame = None
        self.cap = cv2.VideoCapture(ip)
        self.available = False
    def run(self):

        while True:
            _, self.frame = self.cap.read()
            self.available = True
