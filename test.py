import numpy as np
import cv2
from flask import Flask, render_template, Response
from camera import Camera


app = Flask(__name__)

cam = Camera()


def gen_frames():

	while True:
		success, frame = cam.video.read()  # read the camera frame
		if not success:
			break
		else:
			ret, buffer = cv2.imencode('.jpg', frame)
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