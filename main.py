import cv2
import numpy as np
import math

cam = cv2.VideoCapture(2)

frame_width = 6  # in mm
frame_height = 4.5 # in mm

pixel_count_x = 640
pixel_count_y = 480

pixel_width_x = frame_width / pixel_count_x
pixel_width_y = frame_height / pixel_count_y

magic = 0.009375

def nothing(x):
	pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("LCH", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LCL", "Trackbars", 0, 255, nothing)
	
cv2.createTrackbar("RCH", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("RCL", "Trackbars", 0, 255, nothing)

cv2.createTrackbar("Hough", "Trackbars", 0, 255, nothing)

def random_color():
	return (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

def getMidPoint(aX, aY, bX, bY):
	return int((aX+bX)/2), int((aY+bY)/2)

def getPerpCoord(aX, aY, bX, bY, length):
    vX = bX-aX
    vY = bY-aY
    #print(str(vX)+" "+str(vY))
    # if(vX == 0 or vY == 0):
    #     return 0, 0, 0, 0
    mag = math.sqrt(vX*vX + vY*vY)
    vX = vX / mag
    vY = vY / mag
    temp = vX
    vX = 0-vY
    vY = temp
    cX = bX + vX * length
    cY = bY + vY * length
    dX = bX - vX * length
    dY = bY - vY * length
    return int(cX), int(cY), int(dX), int(dY)

def mcfromrth(r,t):
	slope = -(math.cos(t)/math.sin(t))
	c = r/math.sin(t)
	return slope, c

def getpointnearcenter(slope, c,y):
	x = int((y-c)/slope)
	# y = int(slope*x + c)
	return x, y

while 1:
	_, img = cam.read()

	# left_roi = np.copy(img[:, 100:300])
	# right_roi = np.copy(img[:, 340:500])

	left_roi = img[:, 100:300]
	right_roi = img[:, 340:500]

	#Get edges	
	lh = cv2.getTrackbarPos("LCH", "Trackbars")
	ll = cv2.getTrackbarPos("LCL", "Trackbars")
	rh = cv2.getTrackbarPos("RCH", "Trackbars")
	rl = cv2.getTrackbarPos("RCL", "Trackbars")

	blur_left = cv2.GaussianBlur(left_roi, (5, 5), 0)
	blur_right = cv2.GaussianBlur(right_roi, (5, 5), 0)

	# left_edges = cv2.Canny(blur_left, ll, lh)
	# right_edges = cv2.Canny(blur_right, rl, rh)

	left_edges = cv2.Canny(left_roi, 100, 180)
	right_edges = cv2.Canny(right_roi, 100, 180)

	hough_threshold = cv2.getTrackbarPos("Hough", "Trackbars") 

	# Get Hough Lines
	left_lines = cv2.HoughLines(left_edges, 1, np.pi/180, 180)
	right_lines = cv2.HoughLines(right_edges, 1, np.pi/180, 180)

	print("Left", left_lines)
	print("Right", right_lines)

	#Plot points
	if left_lines is not None and right_lines is not None:
		rho_l , theta_l = left_lines[0][0]
		rho_r , theta_r = right_lines[0][0]
		# print("Left", mcfromrth(rho_l, theta_l))
		# print("Right",mcfromrth(rho_r, theta_r))
		slope_l, c_l = mcfromrth(rho_l, theta_l)
		slope_r, c_r = mcfromrth(rho_r, theta_r)
		x_l, y_l = getpointnearcenter(slope_l, c_l,240)
		x_r, y_r = getpointnearcenter(slope_r, c_r,240)
		print("Left", x_l + 100, y_l)
		print("Right", x_r + 340, y_r)
		cv2.circle(left_roi, (x_l, y_l), 5, (0, 0, 255), -1)
		cv2.circle(right_roi, (x_r, y_r), 5, (0, 0, 255), -1)

	# Draw lines
	if left_lines is not None:
		for l in left_lines:
			for rho, theta in l:
				a = np.cos(theta)
				b = np.sin(theta)
				x0 = a*rho
				y0 = b*rho
				x1 = int(x0 + 1000*(-b))
				y1 = int(y0 + 1000*(a))
				x2 = int(x0 - 1000*(-b))
				y2 = int(y0 - 1000*(a))

				# cv2.circle(left_roi, (int(x0), int(y0)), 5, (0, 0, 255), 30)
				cv2.line(left_roi, (x1, y1), (x2, y2), (0, 0, 255), 1)
				# print("Left Line::", x0, y0, x1, y1, x2, y2)

	if right_lines is not None:
		for l in right_lines:
			for rho, theta in l:
				a = np.cos(theta)
				b = np.sin(theta)
				x0 = a*rho
				y0 = b*rho
				x1 = int(x0 + 1000*(-b))
				y1 = int(y0 + 1000*(a))
				x2 = int(x0 - 1000*(-b))
				y2 = int(y0 - 1000*(a))

				# cv2.circle(right_roi, (int(x0), int(y0)), 5, (255, 0, 255), 30)
				cv2.line(right_roi, (x1, y1), (x2, y2), (0, 0, 255), 1)
				# nx1,ny1, nx2, ny2 = getPerpCoord(x1, y1, x2, y2, 1000)
				# cv2.line(right_roi, (nx1, ny1), (nx2, ny2), (0, 255, 255), 2)

	#Get Longest line

	cv2.line(img, (0,0),(640,480), (255,0,0), 1)
	cv2.line(img, (0,480),(640,0), (255,0,0), 1)
	cv2.imshow("left_edges", left_edges)
	cv2.imshow("right_edges", right_edges)
	cv2.imshow("s", img)
	cv2.imshow("LEFT", left_roi)
	cv2.imshow("Right", right_roi)
	if cv2.waitKey(1)&0XFF == ord('q'):
		break
