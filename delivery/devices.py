import cv2

def search():

    devices = []

    for i in range(10):
        
        cap = cv2.VideoCapture(i)
        stat, _ = cap.read()
        
        if stat:
            devices.append(i)
            cap.release()

    return devices

