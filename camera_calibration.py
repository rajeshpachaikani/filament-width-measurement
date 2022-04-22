import cv2

print("Initializing camera")

camera = cv2.VideoCapture(2)
print("Setting camera mode")

exp_val = -3

#codec = 0x47504A4D # MJPG
#camera.set(cv2.CAP_PROP_FPS, 30.0)
#camera.set(cv2.CAP_PROP_FOURCC, codec)
#camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
camera.set(cv2.CAP_PROP_EXPOSURE, exp_val)

print("Starting capture")
while(1):
	camera.grab()
	retval, im = camera.retrieve(0)
	cv2.imshow("image", im)

	k = cv2.waitKey(1) & 0xff
	if k == 27:
		print("exit")
		break

camera.release()
cv2.destroyAllWindows()
