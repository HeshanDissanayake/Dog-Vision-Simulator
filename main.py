import numpy as np
import cv2
import ipcamera
import Stiching

from flask import Flask, render_template, Response



app = Flask(__name__)
ip1 = 0#"http://192.168.1.5:8081/video"
ip2 = 0#"http://192.168.1.5:8081/video"

cam1 = ipcamera.IpCamera(ip1)
cam2 = ipcamera.IpCamera(ip2)

cam1.start()
cam2.start()

sticher = Stiching.Sticher()


def gen_frames():

	while True:
		if cam1.available and cam2.available:
			images = [cam2.frame, cam1.frame]
			img = sticher.stitch(images)
			img = cv2.resize(img, (cam1.frame.shape[1], int(cam1.frame.shape[0]/2)))

			ret, buffer = cv2.imencode('.jpg', img)
			frame = buffer.tobytes()
			yield (b'--frame\r\n' 
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
	