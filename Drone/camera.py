#connect cam
def connect_cam():
	import cv2
	cam = cv2.VideoCapture(0)
	return cam

#capture image
def capture(cam):
    ret, frame = cam.read()
	if ret:
		cv2.imwrite("/home/mx/Desktop/a.png", frame)
