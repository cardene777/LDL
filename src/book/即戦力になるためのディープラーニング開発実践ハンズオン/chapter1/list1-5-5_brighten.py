import cv2
import numpy as np

image = cv2.imread('face.jpg')

image = image.astype(np.uint16)
image += 100
image = image.clip(0, 255).astype(np.uint8)

cv2.imshow('preview', image)
cv2.waitKey()
