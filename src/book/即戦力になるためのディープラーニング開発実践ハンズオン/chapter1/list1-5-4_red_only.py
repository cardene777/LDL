import cv2

image = cv2.imread('face.jpg')

image[:, :, [0, 1]] = 0

cv2.imshow('preview', image)
cv2.waitKey()
