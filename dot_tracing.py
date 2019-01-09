# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import copy
import numpy as np
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(0.1)
 
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array 

# display only red channel
test_img = copy.deepcopy(image)
test_img[:,:,0] = 0
test_img[:,:,1] = 0
# display the image on screen and wait for a keypress
#cv2.imshow("Image", test_img)
#cv2.waitKey(0)

print image.shape
# convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray_image,50,255,cv2.THRESH_BINARY)
#ret,thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("gray image", thresh)
cv2.waitKey(0)

# calculate center of blob in image
num_black = 0
x_pos = 0
y_pos = 0
for i in range(0, thresh.shape[0]):
	for j in range(0, thresh.shape[1]):
		if thresh[i][j] == 0:
			num_black = num_black + 1
			x_pos = x_pos + j
			y_pos = y_pos + i
x_pos = x_pos / num_black
y_pos = y_pos / num_black
print('x: ' + str(x_pos) + ' y: ' + str(y_pos))

# put text and highlight the center
img_dot = copy.deepcopy(image)
#img_dot = np.zeros((image.shape[0], image.shape[1], image.shape[2]), np.uint8)
cv2.circle(img_dot, (x_pos, y_pos), 50, (0, 255, 0), 3)


# display the image on screen and wait for a keypress
cv2.imshow("red center", img_dot)
cv2.waitKey(0)
