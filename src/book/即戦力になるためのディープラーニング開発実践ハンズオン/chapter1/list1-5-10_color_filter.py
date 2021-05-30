import cv2
import numpy as np

image = cv2.imread('face.jpg')

image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(image, np.array([100, 100, 0]), np.array([120, 255, 255]))
image[mask == 0, 2] = 0
image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

cv2.imshow('preview', image)
cv2.waitKey()
