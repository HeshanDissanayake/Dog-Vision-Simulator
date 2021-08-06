import numpy as np
import json
import cv2
import ipcamera
import Stitching_v2
import devices
import numpy
import time
from datetime import datetime


from flask import Flask, render_template, Response, request

app = Flask(__name__)
ip1 = "http://192.168.1.25:8080/video"
ip2 = "http://192.168.1.5:8081/video"

# cam1 = ipcamera.IpCamera(ip2)
# cam2 = ipcamera.IpCamera(ip1)

# cam1.start()
# cam2.start()

k = 5
IPCAMS = False
cams = []
recorder = None
isRecording = False
frameRate = 1



def gen_frames():
    global recorder, isRecording
    imgs = []

    while True:
        if len(cams) != 0:
            # if cam1.available and cam2.available:
            if not IPCAMS:
                imgs = [cam.read()[1] for cam in cams]
            # else:
            # 	imgs = [cam1.frame, cam2.frame]
            img = Stitching_v2.get(imgs)
            img = cv2.blur(img, (k, k))
            img = img[:, :, :3]

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img[:, :, 1] = gray
            img[:, :, 2] = gray

            if recorder is not None:
                recorder.write(np.array(img).astype(np.uint8))

            if isRecording and (recorder is None):
                fileName = datetime.now().strftime("records/%m-%d-%Y::%H:%M:%S.avi")
                print("recoding started ",fileName)
                recorder = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc(*"MJPG"), 25, (img.shape[1], img.shape[0]))

            if (not isRecording) and (recorder is not None):
                print("recoding stoped")
                recorder.release()
                recorder = None

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            time.sleep(0.01)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


#--------------Static serving--------------#

@app.route('/')
def index():
    return render_template('index.html', record=isRecording)


@app.route('/style.css')
def style():
    return render_template('style.css')


@app.route('/app.js')
def js():
    return render_template('app.js')

#-----------------------------------------#


@app.route('/submit_data', methods=['GET', 'POST'])
def post():
    global k
    if request.method == 'POST':
        data = json.loads(request.data)
        if "blur" in data.keys():
            k = int(int(data["blur"])/2)+1

        return request.data

    if request.method == 'GET':
        return "get"


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/record')
def refresh():
    global recorder, isRecording
    if isRecording:
        isRecording = False
        return "recording stoped"
    else:
        isRecording = True
        return "recording started"


def search():
    return devices.search()
    # return json.dumps({"devices":cams})


if __name__ == "__main__":
    camsIds = search()
    print("cameras found: ", camsIds)
    if not IPCAMS:
        for camId in camsIds:
            try:
                print("initiating cam:%d" % camId)
                cams.append(cv2.VideoCapture(camId))
            except Exception as e:
                print("cam%d init Fail" % camId, e)

    app.run("0.0.0.0", 3001, debug=False)
