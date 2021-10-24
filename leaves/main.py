import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread("1.jpg")

kernel = cv .getStructuringElement(cv.MORPH_ELLIPSE, ( 7 , 7 ) )
image_erode = cv.erode(img, kernel)
imgplot = plt.imshow(image_erode)
plt.show()
hsv_img = cv.cvtColor(image_erode, cv.COLOR_BGR2HSV)
markers = np.zeros((img.shape[0], img.shape [1] ), dtype ="int32")
markers[90:140, 90:140] = 255
markers[236:255, 0:20] = 1
markers[0:20, 0:20] = 1
markers[0:20, 236:255] = 1
markers[236:255, 236:255] = 1
leafs_area_BGR = cv.watershed( image_erode , markers )
healthy_part = cv.inRange(hsv_img, (36,25,25) , (86, 255, 255))
ill_part = leafs_area_BGR - healthy_part
mask = np.zeros_like(img, np.uint8)
mask [ leafs_area_BGR > 1 ] = ( 255 , 0 , 255 )
mask[ ill_part > 1] = ( 0, 0, 255)
imgplot = plt.imshow(mask)
plt.show()

