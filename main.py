import numpy as np
import json
import cv2
import ipcamera
import Stiching
import devices

from flask import Flask, render_template, Response, request



app = Flask(__name__)
ip1 = "http://192.168.1.5:8081/video"
ip2 = "http://192.168.1.5:8081/video"

cam1 = ipcamera.IpCamera(ip1)
cam2 = ipcamera.IpCamera(ip2)

# cam1.start()
# cam2.start()
# cam1 =None
# cam2 =None

sticher = Stiching.Sticher()


def gen_frames():
	return "lol"
	# while True:
	# 	if cam1.available and cam2.available:
	# 		images = [cam2.frame, cam1.frame]
	# 		img = sticher.stitch(images)
	# 		img = cv2.resize(img, (cam1.frame.shape[1], int(cam1.frame.shape[0]/2)))

	# 		ret, buffer = cv2.imencode('.jpg', img)
	# 		frame = buffer.tobytes()
	# 		yield (b'--frame\r\n' 
	# 				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  



#--------------Static serving--------------#

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/style.css')
def style():
	return render_template('style.css')

@app.route('/app.js')
def js():
	return render_template('app.js')

#-----------------------------------------#


@app.route('/submit_data', methods = ['GET', 'POST'])
def post():
	if request.method == 'POST':
		return request.data

	if request.method == 'GET':
		return "get"


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/search')
def search():
	return json.dumps(devices.search())

if __name__ == "__main__":
    app.run(debug=True)
	