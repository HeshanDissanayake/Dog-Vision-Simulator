import cv2

cap = cv2.VideoCapture(2)

while True:
    _, img = cap.read()
    cv2.imshow("asd", img)
    cv2.waitKey(10)