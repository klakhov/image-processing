import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def find_ill_parts(img):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
    image_erode = cv.erode(img, kernel)
    hsv_img = cv.cvtColor(image_erode, cv.COLOR_BGR2HSV)
    markers = np.zeros((img.shape[0], img.shape[1]), dtype="int32")
    markers[90:140, 90:140] = 255
    markers[236:255, 0:20] = 1
    markers[0:20, 0:20] = 1
    markers[0:20, 236:255] = 1
    markers[236:255, 236:255] = 1
    leafs_area_BGR = cv.watershed(image_erode, markers)
    healthy_part = cv.inRange(hsv_img, (36,25,25), (86, 255, 255))
    ill_part = leafs_area_BGR - healthy_part
    mask = np.zeros_like(img, np.uint8)
    mask [leafs_area_BGR > 1] = (255 , 0, 255)
    mask[ill_part > 1] = (0, 0, 255)
    return mask

def change_shadows(img):
    black_pixels = np.where(
        (img[:, :, 0] < 40) & 
        (img[:, :, 1] < 40) & 
        (img[:, :, 2] < 40)
    )
    img[black_pixels] = [170, 150, 160]
    return img


columns = 3
rows = 1
fig =  plt.figure(figsize=(10, 7))
img = cv.imread("1.jpg")

wihout_shadows = change_shadows(img)

gauss = cv.GaussianBlur(wihout_shadows, (7,7), cv.BORDER_DEFAULT)
result = find_ill_parts(gauss)
fig.add_subplot(rows, columns, 1)
plt.imshow(result)
plt.title("Gaussian")

bilateral = cv.bilateralFilter(wihout_shadows, 15, 125, 75)
result = find_ill_parts(bilateral)
fig.add_subplot(rows, columns, 2)
plt.imshow(result)
plt.title("Bilateral")

non_local = cv.fastNlMeansDenoisingColored(img, None, 15, 15, 7, 21)
result = find_ill_parts(non_local)
fig.add_subplot(rows, columns, 3)
plt.imshow(result)
plt.title("Non-Local means")

plt.show()

