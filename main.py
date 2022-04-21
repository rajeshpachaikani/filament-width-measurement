import cv2
import FilaMeasure as FM

fm = FM.FilaMeasure()
FM.FilaMeasure.nothing()

# print("Starting FilaMeasure", fm.get_measure_str())

cam = cv2.VideoCapture(2)

frame_width = 6  # in mm
frame_height = 4.5 # in mm

pixel_count_x = 640
pixel_count_y = 480

pixel_width_x = frame_width / pixel_count_x
pixel_width_y = frame_height / pixel_count_y

magic = 0.009375


#IOT Trap statement
def iot_callback(iot_data):
	print("IOT data: " + str(iot_data))

while 1:
	_, img = cam.read()
	# img_cln = img[:, 80:80+480]

	#Draw X in image
	cv2.line(img, (0, 0), (pixel_count_x, pixel_count_y), (0, 0, 255), 2)
	cv2.line(img, (0, pixel_count_y), (pixel_count_x, 0), (0, 0, 255), 2)

	fil_width = int(1.75/magic)
	h_fil = int(fil_width/2)
	print(h_fil)
	#Draw line on image in the center
	cv2.line(img, (320-h_fil,240), (320-h_fil+fil_width,240), (0, 255, 0), 2)
	# cv2.line(img, (320, 240-int(fil_width/2)),(320, 240+int(fil_width/2)), (0, 255, 0), 2)
	print(img.shape)
	# print(img_cln.shape)
	cv2.imshow("s",img)
	cv2.waitKey(1)
