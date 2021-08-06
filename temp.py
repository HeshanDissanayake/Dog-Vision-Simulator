import subprocess
import os
import signal
import time
from datetime import datetime
import cv2

cap = cv2.VideoCapture(0)

count = 0
id = 0
recorder = cv2.VideoWriter("%d.avi"%id, cv2.VideoWriter_fourcc(*"MJPG"), 25,(640,480))


while True:
    _, img = cap.read()
    recorder.write(img)
    if count > 200:

        recorder.release()
        id = id + 1
        recorder = cv2.VideoWriter("%d.avi"%id, cv2.VideoWriter_fourcc(*"MJPG"), 25,(640,480))
        print("writing file %d.avi"%id)
        count = 0

    count = count + 1
